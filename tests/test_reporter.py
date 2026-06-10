"""
报告生成模块测试
"""

import unittest
import json
from impactforge.reporter import Reporter
from impactforge.impact_analyzer import ImpactResult, RiskLevel, ImpactScope
from impactforge.git_parser import ChangeType


class TestReporter(unittest.TestCase):
    """测试 Reporter 类"""

    def setUp(self):
        self.reporter = Reporter()
        self.sample_results = [
            ImpactResult("src/main.py", ChangeType.MODIFIED, RiskLevel.LOW, ImpactScope.LOCAL, score=15),
            ImpactResult("config/settings.py", ChangeType.MODIFIED, RiskLevel.HIGH, ImpactScope.PROJECT, score=75),
        ]
        self.summary = {
            "total_files": 2,
            "risk_distribution": {"low": 1, "medium": 0, "high": 1, "critical": 0},
            "average_score": 45,
            "max_score": 75,
            "overall_risk": "MEDIUM",
            "critical_files": [],
            "high_risk_files": ["config/settings.py"],
        }

    def test_generate_json(self):
        """测试 JSON 报告生成"""
        output = self.reporter.generate_json(self.sample_results, self.summary)
        data = json.loads(output)
        self.assertEqual(data["meta"]["tool"], "ImpactForge")
        self.assertEqual(data["summary"]["total_files"], 2)
        self.assertEqual(len(data["results"]), 2)

    def test_generate_markdown(self):
        """测试 Markdown 报告生成"""
        output = self.reporter.generate_markdown(self.sample_results, self.summary)
        self.assertIn("# ImpactForge", output)
        self.assertIn("src/main.py", output)
        self.assertIn("config/settings.py", output)
        self.assertIn("```mermaid", output)

    def test_generate_html(self):
        """测试 HTML 报告生成"""
        output = self.reporter.generate_html(self.sample_results, self.summary)
        self.assertIn("<!DOCTYPE html>", output)
        self.assertIn("ImpactForge", output)

    def test_generate_sarif(self):
        """测试 SARIF 报告生成"""
        output = self.reporter.generate_sarif(self.sample_results, self.summary)
        data = json.loads(output)
        self.assertEqual(data["version"], "2.1.0")
        self.assertEqual(data["runs"][0]["tool"]["driver"]["name"], "ImpactForge")
        # 应该只包含 high 和 critical 的结果
        self.assertTrue(len(data["runs"][0]["results"]) >= 1)


if __name__ == "__main__":
    unittest.main()
