"""
Git 变更解析模块
解析 Git diff、commit、branch 等变更信息
"""

import subprocess
import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from enum import Enum


class ChangeType(Enum):
    """变更类型枚举"""
    ADDED = "A"           # 新增文件
    MODIFIED = "M"        # 修改文件
    DELETED = "D"         # 删除文件
    RENAMED = "R"         # 重命名文件
    COPIED = "C"          # 复制文件
    TYPE_CHANGED = "T"    # 类型变更
    UNMERGED = "U"        # 未合并
    UNKNOWN = "X"         # 未知


@dataclass
class FileChange:
    """单个文件变更信息"""
    path: str
    change_type: ChangeType
    old_path: Optional[str] = None
    additions: int = 0
    deletions: int = 0
    diff_content: str = ""
    functions_changed: List[str] = field(default_factory=list)
    classes_changed: List[str] = field(default_factory=list)


@dataclass
class CommitInfo:
    """Commit 信息"""
    hash: str
    author: str
    email: str
    date: str
    message: str
    files: List[FileChange] = field(default_factory=list)


class GitParser:
    """Git 变更解析器"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def _run_git(self, args: List[str]) -> Tuple[str, str, int]:
        """运行 Git 命令"""
        cmd = ["git", "-C", self.repo_path] + args
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "Git command timeout", 1
        except FileNotFoundError:
            return "", "Git not found", 127

    def is_git_repo(self) -> bool:
        """检查是否为 Git 仓库"""
        _, _, code = self._run_git(["rev-parse", "--git-dir"])
        return code == 0

    def get_changed_files(self, ref: str = "HEAD", target_ref: Optional[str] = None) -> List[FileChange]:
        """
        获取变更文件列表
        
        Args:
            ref: 源引用 (默认 HEAD)
            target_ref: 目标引用 (默认工作目录)
        
        Returns:
            文件变更列表
        """
        if target_ref:
            diff_args = ["diff", "--name-status", target_ref, ref]
        else:
            diff_args = ["diff", "--name-status", ref]

        stdout, stderr, code = self._run_git(diff_args)
        if code != 0:
            raise RuntimeError(f"Git diff failed: {stderr}")

        changes = []
        for line in stdout.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                change_type = self._parse_change_type(parts[0][0])
                path = parts[-1]
                old_path = parts[1] if len(parts) > 2 and change_type == ChangeType.RENAMED else None
                
                # 获取详细 diff 统计
                stats = self._get_file_stats(ref, target_ref, path)
                
                changes.append(FileChange(
                    path=path,
                    change_type=change_type,
                    old_path=old_path,
                    additions=stats[0],
                    deletions=stats[1]
                ))

        return changes

    def _parse_change_type(self, char: str) -> ChangeType:
        """解析变更类型字符"""
        mapping = {
            "A": ChangeType.ADDED,
            "M": ChangeType.MODIFIED,
            "D": ChangeType.DELETED,
            "R": ChangeType.RENAMED,
            "C": ChangeType.COPIED,
            "T": ChangeType.TYPE_CHANGED,
            "U": ChangeType.UNMERGED,
        }
        return mapping.get(char, ChangeType.UNKNOWN)

    def _get_file_stats(self, ref: str, target_ref: Optional[str], path: str) -> Tuple[int, int]:
        """获取文件变更统计"""
        if target_ref:
            args = ["diff", "--numstat", target_ref, ref, "--", path]
        else:
            args = ["diff", "--numstat", ref, "--", path]

        stdout, _, code = self._run_git(args)
        if code == 0 and stdout.strip():
            parts = stdout.strip().split("\t")
            if len(parts) >= 2:
                try:
                    additions = int(parts[0]) if parts[0] != "-" else 0
                    deletions = int(parts[1]) if parts[1] != "-" else 0
                    return additions, deletions
                except ValueError:
                    pass
        return 0, 0

    def get_file_diff(self, path: str, ref: str = "HEAD", target_ref: Optional[str] = None) -> str:
        """获取单个文件的 diff 内容"""
        if target_ref:
            args = ["diff", target_ref, ref, "--", path]
        else:
            args = ["diff", ref, "--", path]

        stdout, stderr, code = self._run_git(args)
        if code != 0:
            return ""
        return stdout

    def get_commit_info(self, commit_hash: str) -> Optional[CommitInfo]:
        """获取 Commit 详细信息"""
        format_str = "%H|%an|%ae|%ad|%s"
        stdout, stderr, code = self._run_git([
            "show", "--format=" + format_str, "--no-patch",
            commit_hash
        ])
        if code != 0:
            return None

        parts = stdout.strip().split("|", 4)
        if len(parts) < 5:
            return None

        commit = CommitInfo(
            hash=parts[0],
            author=parts[1],
            email=parts[2],
            date=parts[3],
            message=parts[4]
        )

        # 获取该 commit 的变更文件
        commit.files = self.get_changed_files(f"{commit_hash}^", commit_hash)
        return commit

    def get_commit_range(self, from_ref: str, to_ref: str = "HEAD") -> List[CommitInfo]:
        """获取一段 commit 范围"""
        stdout, stderr, code = self._run_git([
            "log", "--format=%H", f"{from_ref}..{to_ref}"
        ])
        if code != 0:
            return []

        commits = []
        for line in stdout.strip().split("\n"):
            if line.strip():
                commit = self.get_commit_info(line.strip())
                if commit:
                    commits.append(commit)
        return commits

    def get_branch_commits(self, branch: str, base_branch: str = "main") -> List[CommitInfo]:
        """获取分支相对于基分支的 commits"""
        return self.get_commit_range(base_branch, branch)

    def get_staged_changes(self) -> List[FileChange]:
        """获取暂存区变更"""
        stdout, stderr, code = self._run_git([
            "diff", "--cached", "--name-status"
        ])
        if code != 0:
            return []

        changes = []
        for line in stdout.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                change_type = self._parse_change_type(parts[0][0])
                path = parts[-1]
                stats = self._get_file_stats("HEAD", None, path)
                changes.append(FileChange(
                    path=path,
                    change_type=change_type,
                    additions=stats[0],
                    deletions=stats[1]
                ))
        return changes

    def get_working_changes(self) -> List[FileChange]:
        """获取工作区未暂存的变更"""
        stdout, stderr, code = self._run_git([
            "diff", "--name-status"
        ])
        if code != 0:
            return []

        changes = []
        for line in stdout.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                change_type = self._parse_change_type(parts[0][0])
                path = parts[-1]
                stats = self._get_file_stats("HEAD", None, path)
                changes.append(FileChange(
                    path=path,
                    change_type=change_type,
                    additions=stats[0],
                    deletions=stats[1]
                ))
        return changes

    def get_all_changes(self) -> List[FileChange]:
        """获取所有变更（暂存区 + 工作区）"""
        staged = self.get_staged_changes()
        working = self.get_working_changes()
        
        # 合并，暂存区优先
        paths = {c.path for c in staged}
        result = staged.copy()
        for w in working:
            if w.path not in paths:
                result.append(w)
        return result
