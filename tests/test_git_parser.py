"""
Git 解析器测试
"""

import unittest
import tempfile
import os
import subprocess
from impactforge.git_parser import GitParser, ChangeType


class TestGitParser(unittest.TestCase):
    """测试 GitParser 类"""

    def setUp(self):
        """创建临时 Git 仓库"""
        self.temp_dir = tempfile.mkdtemp()
        self.parser = GitParser(self.temp_dir)
        
        # 初始化 Git 仓库
        self._run_git(["init"])
        self._run_git(["config", "user.email", "test@test.com"])
        self._run_git(["config", "user.name", "Test User"])

    def tearDown(self):
        """清理临时目录"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def _run_git(self, args):
        """运行 Git 命令"""
        cmd = ["git", "-C", self.temp_dir] + args
        subprocess.run(cmd, capture_output=True, check=True)

    def _create_file(self, path, content=""):
        """创建文件"""
        full_path = os.path.join(self.temp_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)

    def test_is_git_repo(self):
        """测试仓库检测"""
        self.assertTrue(self.parser.is_git_repo())
        
        # 非 Git 目录
        non_git = GitParser(tempfile.mkdtemp())
        self.assertFalse(non_git.is_git_repo())

    def test_get_changed_files_empty(self):
        """测试空仓库变更检测"""
        changes = self.parser.get_staged_changes()
        self.assertEqual(len(changes), 0)

    def test_get_staged_changes(self):
        """测试暂存区变更"""
        # 创建并暂存文件
        self._create_file("test.py", "print('hello')")
        self._run_git(["add", "test.py"])
        
        changes = self.parser.get_staged_changes()
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].path, "test.py")
        self.assertEqual(changes[0].change_type, ChangeType.ADDED)

    def test_get_working_changes(self):
        """测试工作区变更"""
        # 创建文件并提交
        self._create_file("test.py", "print('hello')")
        self._run_git(["add", "test.py"])
        self._run_git(["commit", "-m", "initial"])
        
        # 修改文件
        self._create_file("test.py", "print('world')")
        
        changes = self.parser.get_working_changes()
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].change_type, ChangeType.MODIFIED)

    def test_change_type_enum(self):
        """测试变更类型枚举"""
        self.assertEqual(ChangeType.ADDED.value, "A")
        self.assertEqual(ChangeType.MODIFIED.value, "M")
        self.assertEqual(ChangeType.DELETED.value, "D")


if __name__ == "__main__":
    unittest.main()
