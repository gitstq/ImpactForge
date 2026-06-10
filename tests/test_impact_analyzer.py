"""
影响分析器测试
"""

import unittest
from impactforge.impact_analyzer import ImpactAnalyzer, ImpactResult, RiskLevel, ImpactScope
from impactforge.git_parser import FileChange, ChangeType


class TestImpactAnalyzer(unittest.TestCase):
    """测试 ImpactAnalyzer 类"""

    def setUp(self):
        self.analyzer = ImpactAnalyzer()

    def test_analyze_low_risk(self):
        """测试低风险分析"""
        change = FileChange(
            path="src/utils/helper.py",
            change_type=ChangeType.MODIFIED,
            additions=10,
            deletions=5,
        )
        
        result = self.analyzer._analyze_single(change)
        self.assertEqual(result.file_path, "src/utils/helper.py")
        self.assertIn(result.risk_level, [RiskLevel.LOW, RiskLevel.MEDIUM])

    def test_analyze_high_risk_config(self):
        """测试配置文件高风险"""
        change = FileChange(
            path="config/settings.py",
            change_type=ChangeType.MODIFIED,
            additions=50,
            deletions=10,
        )
        
        result = self.analyzer._analyze_single(change)
        self.assertEqual(result.risk_level, RiskLevel.HIGH)

    def test_analyze_critical_delete(self):
        """测试删除操作风险"""
        change = FileChange(
            path="src/core/engine.py",
            change_type=ChangeType.DELETED,
            additions=0,
            deletions=100,
        )
        
        result = self.analyzer._analyze_single(change)
        self.assertEqual(result.risk_level, RiskLevel.HIGH)
        self.assertIn("文件删除操作", result.risk_factors)

    def test_analyze_sensitive_keywords(self):
        """测试敏感关键词检测"""
        change = FileChange(
            path="src/auth/login.py",
            change_type=ChangeType.MODIFIED,
            additions=20,
            deletions=5,
            diff_content="""
+ def verify_password(password, hash):
+     return bcrypt.checkpw(password.encode(), hash)
+ def generate_token(secret_key):
+     return jwt.encode({}, secret_key)
            """
        )
        
        result = self.analyzer._analyze_single(change)
        self.assertEqual(result.risk_level, RiskLevel.HIGH)
        self.assertTrue(any("密码" in f or "secret" in f.lower() for f in result.risk_factors))

    def test_score_calculation(self):
        """测试评分计算"""
        result = ImpactResult(
            file_path="test.py",
            change_type=ChangeType.MODIFIED,
            risk_level=RiskLevel.HIGH,
            impact_scope=ImpactScope.PROJECT,
            risk_factors=["factor1", "factor2"],
        )
        
        score = self.analyzer._calculate_score(result)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        self.assertGreater(score, 50)  # HIGH + PROJECT 应该高分

    def test_summary_generation(self):
        """测试摘要生成"""
        results = [
            ImpactResult("a.py", ChangeType.MODIFIED, RiskLevel.LOW, ImpactScope.LOCAL, score=10),
            ImpactResult("b.py", ChangeType.MODIFIED, RiskLevel.MEDIUM, ImpactScope.MODULE, score=40),
            ImpactResult("c.py", ChangeType.MODIFIED, RiskLevel.HIGH, ImpactScope.PROJECT, score=80),
        ]
        
        summary = self.analyzer.generate_summary(results)
        self.assertEqual(summary["total_files"], 3)
        self.assertEqual(summary["risk_distribution"]["low"], 1)
        self.assertEqual(summary["risk_distribution"]["medium"], 1)
        self.assertEqual(summary["risk_distribution"]["high"], 1)
        self.assertEqual(len(summary["high_risk_files"]), 1)

    def test_recommendations(self):
        """测试建议生成"""
        result = ImpactResult(
            file_path="test.py",
            change_type=ChangeType.MODIFIED,
            risk_level=RiskLevel.CRITICAL,
            impact_scope=ImpactScope.PROJECT,
        )
        
        self.analyzer._generate_recommendations(result)
        self.assertTrue(len(result.recommendations) > 0)
        self.assertTrue(any("严重" in r or "CRITICAL" in r for r in result.recommendations))


if __name__ == "__main__":
    unittest.main()
