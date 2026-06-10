"""
报告生成模块
支持多种格式报告输出
"""

import json
from datetime import datetime
from typing import List, Dict
from .impact_analyzer import ImpactResult
from .visualizer import Visualizer


class Reporter:
    """报告生成器"""

    def __init__(self):
        self.visualizer = Visualizer()

    def generate_json(self, results: List[ImpactResult], summary: Dict) -> str:
        """生成 JSON 报告"""
        report = {
            "meta": {
                "tool": "ImpactForge",
                "version": "1.0.0",
                "generated_at": datetime.now().isoformat(),
            },
            "summary": summary,
            "results": [
                {
                    "file_path": r.file_path,
                    "change_type": r.change_type.value,
                    "risk_level": r.risk_level.value,
                    "impact_scope": r.impact_scope.value,
                    "score": r.score,
                    "risk_factors": r.risk_factors,
                    "recommendations": r.recommendations,
                }
                for r in results
            ],
        }
        return json.dumps(report, indent=2, ensure_ascii=False)

    def generate_markdown(self, results: List[ImpactResult], summary: Dict) -> str:
        """生成 Markdown 报告"""
        lines = [
            "# ImpactForge - 代码变更影响分析报告",
            "",
            f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 摘要",
            "",
            f"- **变更文件总数**: {summary.get('total_files', 0)}",
            f"- **平均风险评分**: {summary.get('average_score', 0)}/100",
            f"- **最高评分**: {summary.get('max_score', 0)}/100",
            f"- **整体风险等级**: {summary.get('overall_risk', 'LOW')}",
            "",
            "### 风险分布",
            "",
        ]

        risk_dist = summary.get("risk_distribution", {})
        for level, count in risk_dist.items():
            if count > 0:
                lines.append(f"- {level.upper()}: {count} 个文件")

        # 严重风险文件
        critical_files = summary.get("critical_files", [])
        if critical_files:
            lines.extend([
                "",
                "### ⚠️ 严重风险文件",
                "",
            ])
            for f in critical_files:
                lines.append(f"- `{f}`")

        # 高风险文件
        high_risk_files = summary.get("high_risk_files", [])
        if high_risk_files:
            lines.extend([
                "",
                "### 🔶 高风险文件",
                "",
            ])
            for f in high_risk_files:
                lines.append(f"- `{f}`")

        # 影响表格
        lines.extend([
            "",
            "## 详细分析",
            "",
            self.visualizer.generate_impact_table(results),
            "",
        ])

        # 每个文件的详细分析
        for result in results:
            lines.extend([
                f"### {result.file_path}",
                "",
                f"- **风险等级**: {result.risk_level.value.upper()}",
                f"- **影响范围**: {result.impact_scope.value}",
                f"- **评分**: {result.score}/100",
                "",
                "**风险因素**:",
                "",
            ])
            for factor in result.risk_factors:
                lines.append(f"- {factor}")

            lines.extend([
                "",
                "**建议**:",
                "",
            ])
            for rec in result.recommendations:
                lines.append(f"- {rec}")
            lines.append("")

        # Mermaid 图表
        lines.extend([
            "## 可视化",
            "",
            "### 风险分布图",
            "",
            "```mermaid",
            self.visualizer.generate_mermaid_pie(results),
            "```",
            "",
            "### 影响关系图",
            "",
            "```mermaid",
            self.visualizer.generate_mermaid_graph(results),
            "```",
            "",
        ])

        return "\n".join(lines)

    def generate_html(self, results: List[ImpactResult], summary: Dict) -> str:
        """生成 HTML 报告"""
        return self.visualizer.generate_html_report(results, summary)

    def generate_sarif(self, results: List[ImpactResult], summary: Dict) -> str:
        """生成 SARIF 格式报告"""
        sarif = {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "ImpactForge",
                            "version": "1.0.0",
                            "informationUri": "https://github.com/impactforge/impactforge",
                        }
                    },
                    "results": [],
                }
            ],
        }

        for result in results:
            if result.risk_level.value in ["high", "critical"]:
                sarif_result = {
                    "ruleId": f"impactforge.{result.risk_level.value}",
                    "level": "warning" if result.risk_level.value == "high" else "error",
                    "message": {
                        "text": f"{result.file_path}: {', '.join(result.risk_factors)}",
                    },
                    "locations": [
                        {
                            "physicalLocation": {
                                "artifactLocation": {"uri": result.file_path}
                            }
                        }
                    ],
                }
                sarif["runs"][0]["results"].append(sarif_result)

        return json.dumps(sarif, indent=2, ensure_ascii=False)
