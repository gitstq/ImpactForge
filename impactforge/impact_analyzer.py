"""
影响分析引擎
分析代码变更对项目的影响范围和风险等级
"""

import re
import os
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple
from enum import Enum
from .git_parser import FileChange, ChangeType


class RiskLevel(Enum):
    """风险等级枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ImpactScope(Enum):
    """影响范围枚举"""
    LOCAL = "local"           # 仅影响当前文件
    MODULE = "module"         # 影响当前模块
    PROJECT = "project"       # 影响整个项目
    EXTERNAL = "external"     # 影响外部依赖


@dataclass
class ImpactResult:
    """影响分析结果"""
    file_path: str
    change_type: ChangeType
    risk_level: RiskLevel
    impact_scope: ImpactScope
    affected_functions: List[str] = field(default_factory=list)
    affected_modules: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    score: int = 0  # 0-100


class ImpactAnalyzer:
    """影响分析器"""

    # 高风险文件模式
    HIGH_RISK_PATTERNS = [
        r"config\.(py|json|yaml|yml|toml)$",
        r"settings\.(py|json|yaml|yml)$",
        r".*\.env.*$",
        r"Dockerfile$",
        r"docker-compose.*$",
        r"\.github/.*$",
        r"ci/.*$",
        r"\.gitlab-ci.*$",
        r"requirements.*\.txt$",
        r"package\.json$",
        r"setup\.py$",
        r"pyproject\.toml$",
        r"Makefile$",
        r".*test.*\.py$",
        r"test_.*\.py$",
        r".*_test\.py$",
        r"tests?/.*$",
    ]

    # 关键函数/类模式
    CRITICAL_PATTERNS = [
        r"def\s+(__init__|main|run|start|stop|connect|close|commit|rollback)",
        r"class\s+.*(Manager|Controller|Service|Handler|Provider|Factory)",
        r"def\s+.*(auth|login|logout|verify|validate|encrypt|decrypt|hash)",
        r"def\s+.*(save|delete|update|create|insert|remove|drop)",
    ]

    # 风险关键词
    RISK_KEYWORDS = [
        "password", "secret", "token", "key", "credential",
        "auth", "permission", "role", "admin", "root",
        "sql", "query", "inject", "xss", "csrf",
        "eval", "exec", "compile", "subprocess", "os.system",
        "delete", "drop", "truncate", "remove", "rm -rf",
        "chmod", "chown", "sudo",
    ]

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def analyze(self, changes: List[FileChange]) -> List[ImpactResult]:
        """
        分析变更列表的影响
        
        Args:
            changes: 文件变更列表
        
        Returns:
            影响分析结果列表
        """
        results = []
        for change in changes:
            result = self._analyze_single(change)
            results.append(result)
        return results

    def _analyze_single(self, change: FileChange) -> ImpactResult:
        """分析单个文件变更"""
        result = ImpactResult(
            file_path=change.path,
            change_type=change.change_type,
            risk_level=RiskLevel.LOW,
            impact_scope=ImpactScope.LOCAL,
        )

        # 1. 基于文件路径评估风险
        self._assess_file_path_risk(result)

        # 2. 基于变更类型评估风险
        self._assess_change_type_risk(result, change)

        # 3. 基于变更量评估风险
        self._assess_change_size_risk(result, change)

        # 4. 基于内容关键词评估风险
        self._assess_content_risk(result, change)

        # 5. 计算综合评分
        result.score = self._calculate_score(result)

        # 6. 生成建议
        self._generate_recommendations(result)

        return result

    def _assess_file_path_risk(self, result: ImpactResult) -> None:
        """基于文件路径评估风险"""
        path = result.file_path.lower()

        for pattern in self.HIGH_RISK_PATTERNS:
            if re.search(pattern, path, re.IGNORECASE):
                result.risk_factors.append(f"高风险文件: {result.file_path}")
                result.risk_level = RiskLevel.HIGH
                result.impact_scope = ImpactScope.PROJECT
                break

        # 检查是否在核心目录
        core_dirs = ["src/", "lib/", "core/", "app/", "models/", "controllers/", "services/"]
        for core_dir in core_dirs:
            if core_dir in path or path.startswith(core_dir.rstrip("/")):
                if result.risk_level == RiskLevel.LOW:
                    result.risk_level = RiskLevel.MEDIUM
                    result.impact_scope = ImpactScope.MODULE
                break

    def _assess_change_type_risk(self, result: ImpactResult, change: FileChange) -> None:
        """基于变更类型评估风险"""
        if change.change_type == ChangeType.DELETED:
            result.risk_factors.append("文件删除操作")
            result.risk_level = RiskLevel.HIGH
            result.impact_scope = ImpactScope.PROJECT
        elif change.change_type == ChangeType.RENAMED:
            result.risk_factors.append("文件重命名可能影响导入路径")
            result.risk_level = RiskLevel.MEDIUM
        elif change.change_type == ChangeType.ADDED:
            # 新增文件通常是低到中风险
            if result.risk_level == RiskLevel.LOW:
                result.risk_factors.append("新增文件")

    def _assess_change_size_risk(self, result: ImpactResult, change: FileChange) -> None:
        """基于变更量评估风险"""
        total_lines = change.additions + change.deletions

        if total_lines > 500:
            result.risk_factors.append(f"大规模变更 ({total_lines} 行)")
            if result.risk_level.value in ["low", "medium"]:
                result.risk_level = RiskLevel.HIGH
        elif total_lines > 200:
            result.risk_factors.append(f"中等规模变更 ({total_lines} 行)")
            if result.risk_level == RiskLevel.LOW:
                result.risk_level = RiskLevel.MEDIUM
        elif total_lines > 50:
            result.risk_factors.append(f"小规模变更 ({total_lines} 行)")

        # 删除比例过高
        if change.deletions > 0 and change.additions == 0:
            result.risk_factors.append("纯删除操作")
            if result.risk_level.value in ["low", "medium"]:
                result.risk_level = RiskLevel.HIGH

    def _assess_content_risk(self, result: ImpactResult, change: FileChange) -> None:
        """基于内容评估风险"""
        if not change.diff_content:
            return

        diff_lower = change.diff_content.lower()

        # 检查风险关键词
        found_keywords = []
        for keyword in self.RISK_KEYWORDS:
            if keyword in diff_lower:
                found_keywords.append(keyword)

        if found_keywords:
            result.risk_factors.append(f"包含敏感关键词: {', '.join(found_keywords[:5])}")
            if result.risk_level.value in ["low", "medium"]:
                result.risk_level = RiskLevel.HIGH
            elif result.risk_level == RiskLevel.HIGH:
                result.risk_level = RiskLevel.CRITICAL

        # 检查关键函数变更
        for pattern in self.CRITICAL_PATTERNS:
            matches = re.findall(pattern, change.diff_content)
            if matches:
                result.affected_functions.extend(matches)
                result.risk_factors.append(f"关键函数变更: {', '.join(set(matches))}")
                if result.risk_level == RiskLevel.LOW:
                    result.risk_level = RiskLevel.MEDIUM

    def _calculate_score(self, result: ImpactResult) -> int:
        """计算综合风险评分 (0-100)"""
        score = 0

        # 基础分
        risk_scores = {
            RiskLevel.LOW: 10,
            RiskLevel.MEDIUM: 35,
            RiskLevel.HIGH: 65,
            RiskLevel.CRITICAL: 90,
        }
        score += risk_scores.get(result.risk_level, 0)

        # 影响范围加分
        scope_scores = {
            ImpactScope.LOCAL: 0,
            ImpactScope.MODULE: 10,
            ImpactScope.PROJECT: 20,
            ImpactScope.EXTERNAL: 30,
        }
        score += scope_scores.get(result.impact_scope, 0)

        # 风险因素加分
        score += min(len(result.risk_factors) * 5, 20)

        return min(score, 100)

    def _generate_recommendations(self, result: ImpactResult) -> None:
        """生成建议"""
        if result.risk_level == RiskLevel.CRITICAL:
            result.recommendations.append("⚠️ 严重风险：建议进行代码审查和安全审计")
            result.recommendations.append("建议分阶段部署，先在小范围环境测试")
        elif result.risk_level == RiskLevel.HIGH:
            result.recommendations.append("⚠️ 高风险：建议进行同行代码审查")
            result.recommendations.append("确保有完整的测试覆盖")
        elif result.risk_level == RiskLevel.MEDIUM:
            result.recommendations.append("建议进行基本的代码审查")
            result.recommendations.append("验证相关功能是否正常工作")
        else:
            result.recommendations.append("低风险变更，可按正常流程合并")

        if result.change_type == ChangeType.DELETED:
            result.recommendations.append("检查是否有其他文件依赖被删除的内容")

        if result.change_type == ChangeType.RENAMED:
            result.recommendations.append("更新所有引用该文件的导入路径")

    def generate_summary(self, results: List[ImpactResult]) -> Dict:
        """生成分析摘要"""
        total_files = len(results)
        risk_distribution = {
            "low": 0,
            "medium": 0,
            "high": 0,
            "critical": 0,
        }
        total_score = 0
        critical_files = []
        high_risk_files = []

        for r in results:
            risk_distribution[r.risk_level.value] += 1
            total_score += r.score
            if r.risk_level == RiskLevel.CRITICAL:
                critical_files.append(r.file_path)
            elif r.risk_level == RiskLevel.HIGH:
                high_risk_files.append(r.file_path)

        avg_score = total_score / total_files if total_files > 0 else 0

        return {
            "total_files": total_files,
            "risk_distribution": risk_distribution,
            "average_score": round(avg_score, 1),
            "max_score": max((r.score for r in results), default=0),
            "critical_files": critical_files,
            "high_risk_files": high_risk_files,
            "overall_risk": self._determine_overall_risk(avg_score),
        }

    def _determine_overall_risk(self, avg_score: float) -> str:
        """确定整体风险等级"""
        if avg_score >= 80:
            return "CRITICAL"
        elif avg_score >= 60:
            return "HIGH"
        elif avg_score >= 30:
            return "MEDIUM"
        else:
            return "LOW"
