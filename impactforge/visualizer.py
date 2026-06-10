"""
可视化模块
生成 Mermaid 图表、影响图谱等可视化输出
"""

from typing import List, Dict
from .impact_analyzer import ImpactResult, RiskLevel


class Visualizer:
    """影响可视化器"""

    def __init__(self):
        pass

    def generate_mermaid_graph(self, results: List[ImpactResult]) -> str:
        """生成 Mermaid 流程图"""
        lines = ["graph TD"]
        
        # 添加节点
        for i, result in enumerate(results):
            node_id = f"F{i}"
            risk_emoji = self._get_risk_emoji(result.risk_level)
            label = f"{risk_emoji} {result.file_path}"
            # 转义特殊字符
            label = label.replace('"', '#quot;')
            lines.append(f'    {node_id}["{label}"]')
        
        # 添加风险等级分组
        lines.append("")
        lines.append("    subgraph 风险等级")
        
        risk_nodes = {"critical": [], "high": [], "medium": [], "low": []}
        for i, result in enumerate(results):
            risk_nodes[result.risk_level.value].append(f"F{i}")
        
        for level, nodes in risk_nodes.items():
            if nodes:
                lines.append(f"        subgraph {level.upper()}")
                for node in nodes:
                    lines.append(f"            {node}")
                lines.append("        end")
        
        lines.append("    end")
        
        return "\n".join(lines)

    def generate_mermaid_pie(self, results: List[ImpactResult]) -> str:
        """生成 Mermaid 饼图"""
        lines = ["pie title 风险分布"]
        
        risk_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for result in results:
            risk_counts[result.risk_level.value] += 1
        
        for level, count in risk_counts.items():
            if count > 0:
                lines.append(f'    "{level.upper()}" : {count}')
        
        return "\n".join(lines)

    def generate_impact_table(self, results: List[ImpactResult]) -> str:
        """生成 Markdown 影响表格"""
        lines = [
            "| 文件 | 变更类型 | 风险等级 | 影响范围 | 评分 |",
            "|------|----------|----------|----------|------|",
        ]
        
        for result in results:
            risk_badge = self._get_risk_badge(result.risk_level)
            lines.append(
                f"| `{result.file_path}` | {result.change_type.value} | {risk_badge} | "
                f"{result.impact_scope.value} | {result.score} |"
            )
        
        return "\n".join(lines)

    def generate_html_report(self, results: List[ImpactResult], summary: Dict) -> str:
        """生成 HTML 报告"""
        # 风险颜色映射
        risk_colors = {
            "critical": "#dc3545",
            "high": "#fd7e14",
            "medium": "#ffc107",
            "low": "#28a745",
        }

        # 构建文件列表 HTML
        files_html = []
        for result in results:
            color = risk_colors.get(result.risk_level.value, "#6c757d")
            factors = "<br>".join(f"• {f}" for f in result.risk_factors) or "无"
            recs = "<br>".join(f"• {r}" for r in result.recommendations) or "无"
            
            files_html.append(f"""
            <div class="file-card" style="border-left: 4px solid {color};">
                <div class="file-header">
                    <span class="file-path">{result.file_path}</span>
                    <span class="risk-badge" style="background: {color};">{result.risk_level.value.upper()}</span>
                </div>
                <div class="file-details">
                    <p><strong>变更类型:</strong> {result.change_type.value} | 
                       <strong>影响范围:</strong> {result.impact_scope.value} | 
                       <strong>评分:</strong> {result.score}/100</p>
                    <div class="risk-factors">
                        <h4>风险因素:</h4>
                        <p>{factors}</p>
                    </div>
                    <div class="recommendations">
                        <h4>建议:</h4>
                        <p>{recs}</p>
                    </div>
                </div>
            </div>
            """)

        # 构建风险分布条形图
        risk_dist = summary.get("risk_distribution", {})
        total = summary.get("total_files", 1)
        
        bars_html = []
        for level, color in risk_colors.items():
            count = risk_dist.get(level, 0)
            pct = (count / total * 100) if total > 0 else 0
            bars_html.append(f"""
                <div class="bar-item">
                    <span class="bar-label">{level.upper()}</span>
                    <div class="bar-track">
                        <div class="bar-fill" style="width: {pct}%; background: {color};"></div>
                    </div>
                    <span class="bar-value">{count}</span>
                </div>
            """)

        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ImpactForge - 代码变更影响分析报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                background: #f5f7fa; color: #333; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   color: white; padding: 40px; border-radius: 12px; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; font-size: 1.1em; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                         gap: 20px; margin-bottom: 30px; }}
        .summary-card {{ background: white; padding: 24px; border-radius: 12px; 
                         box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; }}
        .summary-card .number {{ font-size: 2.5em; font-weight: bold; color: #667eea; }}
        .summary-card .label {{ color: #666; margin-top: 8px; }}
        .section {{ background: white; padding: 30px; border-radius: 12px; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 20px; }}
        .section h2 {{ margin-bottom: 20px; color: #333; border-bottom: 2px solid #667eea; 
                       padding-bottom: 10px; }}
        .file-card {{ background: #fafbfc; padding: 20px; border-radius: 8px; margin-bottom: 16px; }}
        .file-header {{ display: flex; justify-content: space-between; align-items: center; 
                        margin-bottom: 12px; }}
        .file-path {{ font-family: 'Courier New', monospace; font-size: 0.95em; color: #0366d6; }}
        .risk-badge {{ color: white; padding: 4px 12px; border-radius: 20px; 
                       font-size: 0.8em; font-weight: bold; }}
        .bar-item {{ display: flex; align-items: center; margin-bottom: 12px; }}
        .bar-label {{ width: 80px; font-weight: 500; }}
        .bar-track {{ flex: 1; height: 24px; background: #e9ecef; border-radius: 12px; 
                      overflow: hidden; margin: 0 12px; }}
        .bar-fill {{ height: 100%; border-radius: 12px; transition: width 0.5s ease; }}
        .bar-value {{ width: 40px; text-align: right; font-weight: bold; }}
        .risk-factors, .recommendations {{ margin-top: 12px; padding: 12px; 
                                           background: white; border-radius: 6px; }}
        .risk-factors h4, .recommendations h4 {{ color: #667eea; margin-bottom: 8px; }}
        footer {{ text-align: center; padding: 30px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>ImpactForge</h1>
            <p>智能代码变更影响分析报告</p>
        </div>
        
        <div class="summary-grid">
            <div class="summary-card">
                <div class="number">{summary.get('total_files', 0)}</div>
                <div class="label">变更文件数</div>
            </div>
            <div class="summary-card">
                <div class="number">{summary.get('average_score', 0)}</div>
                <div class="label">平均风险评分</div>
            </div>
            <div class="summary-card">
                <div class="number">{len(summary.get('critical_files', []))}</div>
                <div class="label">严重风险文件</div>
            </div>
            <div class="summary-card">
                <div class="number">{summary.get('overall_risk', 'LOW')}</div>
                <div class="label">整体风险等级</div>
            </div>
        </div>
        
        <div class="section">
            <h2>风险分布</h2>
            {''.join(bars_html)}
        </div>
        
        <div class="section">
            <h2>详细分析</h2>
            {''.join(files_html)}
        </div>
    </div>
    
    <footer>
        <p>Generated by ImpactForge v1.0.0</p>
    </footer>
</body>
</html>"""

    def _get_risk_emoji(self, risk_level: RiskLevel) -> str:
        """获取风险等级表情"""
        emojis = {
            RiskLevel.LOW: "🟢",
            RiskLevel.MEDIUM: "🟡",
            RiskLevel.HIGH: "🟠",
            RiskLevel.CRITICAL: "🔴",
        }
        return emojis.get(risk_level, "⚪")

    def _get_risk_badge(self, risk_level: RiskLevel) -> str:
        """获取风险等级徽章"""
        badges = {
            RiskLevel.LOW: "🟢 LOW",
            RiskLevel.MEDIUM: "🟡 MEDIUM",
            RiskLevel.HIGH: "🟠 HIGH",
            RiskLevel.CRITICAL: "🔴 CRITICAL",
        }
        return badges.get(risk_level, "⚪ UNKNOWN")
