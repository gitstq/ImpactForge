"""
可视化模块测试
"""

import unittest
from impactforge.visualizer import Visualizer
from impactforge.impact_analyzer import ImpactResult, RiskLevel, ImpactScope
from impactforge.git_parser import ChangeType


class TestVisualizer(unittest.TestCase):
    """测试 Visualizer 类"""

    def setUp(self):
        self.visualizer = Visualizer()
        self.sample_results = [
            ImpactResult("src/main.py", ChangeType.MODIFIED, RiskLevel.LOW, ImpactScope.LOCAL, score=15),
            ImpactResult("config/settings.py", ChangeType.MODIFIED, RiskLevel.HIGH, ImpactScope.PROJECT, score=75),
            ImpactResult("tests/test_main.py", ChangeType.ADDED, RiskLevel.MEDIUM, ImpactScope.MODULE, score=40),
        ]

    def test_generate_mermaid_graph(self):
        """测试 Mermaid 流程图生成"""
        graph = self.visualizer.generate_mermaid_graph(self.sample_results)
        self.assertIn("graph TD", graph)
        self.assertIn("src/main.py", graph)
        self.assertIn("config/settings.py", graph)

    def test_generate_mermaid_pie(self):
        """测试 Mermaid 饼图生成"""
        pie = self.visualizer.generate_mermaid_pie(self.sample_results)
        self.assertIn("pie title 风险分布", pie)
        self.assertIn("LOW", pie)
        self.assertIn("HIGH", pie)

    def test_generate_impact_table(self):
        """测试 Markdown 表格生成"""
        table = self.visualizer.generate_impact_table(self.sample_results)
        self.assertIn("| 文件 |", table)
        self.assertIn("src/main.py", table)
        self.assertIn("config/settings.py", table)

    def test_generate_html_report(self):
        """测试 HTML 报告生成"""
        summary = {
            "total_files": 3,
            "risk_distribution": {"low": 1, "medium": 1, "high": 1, "critical": 0},
            "average_score": 43.3,
            "max_score": 75,
            "overall_risk": "MEDIUM",
            "critical_files": [],
            "high_risk_files": ["config/settings.py"],
        }
        html = self.visualizer.generate_html_report(self.sample_results, summary)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("ImpactForge", html)
        self.assertIn("config/settings.py", html)

    def test_get_risk_emoji(self):
        """测试风险表情"""
        self.assertEqual(self.visualizer._get_risk_emoji(RiskLevel.LOW), "🟢")
        self.assertEqual(self.visualizer._get_risk_emoji(RiskLevel.MEDIUM), "🟡")
        self.assertEqual(self.visualizer._get_risk_emoji(RiskLevel.HIGH), "🟠")
        self.assertEqual(self.visualizer._get_risk_emoji(RiskLevel.CRITICAL), "🔴")


if __name__ == "__main__":
    unittest.main()
