"""
TUI 终端用户界面模块
提供交互式终端操作界面
"""

import sys
import os


class TUI:
    """终端用户界面"""

    # ANSI 颜色代码
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "bg_red": "\033[41m",
        "bg_green": "\033[42m",
        "bg_yellow": "\033[43m",
        "bg_blue": "\033[44m",
    }

    # 风险等级颜色
    RISK_COLORS = {
        "low": "green",
        "medium": "yellow",
        "high": "red",
        "critical": "bg_red",
    }

    def __init__(self):
        self.use_color = self._supports_color()

    def _supports_color(self) -> bool:
        """检查终端是否支持颜色"""
        if os.environ.get("NO_COLOR"):
            return False
        if os.environ.get("FORCE_COLOR"):
            return True
        return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

    def color(self, text: str, color_name: str) -> str:
        """给文本添加颜色"""
        if not self.use_color:
            return text
        code = self.COLORS.get(color_name, "")
        return f"{code}{text}{self.COLORS['reset']}"

    def bold(self, text: str) -> str:
        """加粗文本"""
        return self.color(text, "bold")

    def print_header(self, title: str) -> None:
        """打印标题"""
        width = 60
        print()
        print(self.color("=" * width, "cyan"))
        print(self.color(f"  {title}", "bold"))
        print(self.color("=" * width, "cyan"))
        print()

    def print_subheader(self, title: str) -> None:
        """打印子标题"""
        print()
        print(self.color(f"▶ {title}", "bold"))
        print(self.color("─" * 50, "dim"))

    def print_success(self, message: str) -> None:
        """打印成功消息"""
        print(f"{self.color('✓', 'green')} {message}")

    def print_error(self, message: str) -> None:
        """打印错误消息"""
        print(f"{self.color('✗', 'red')} {message}", file=sys.stderr)

    def print_warning(self, message: str) -> None:
        """打印警告消息"""
        print(f"{self.color('⚠', 'yellow')} {message}")

    def print_info(self, message: str) -> None:
        """打印信息消息"""
        print(f"{self.color('ℹ', 'blue')} {message}")

    def print_risk_badge(self, risk_level: str) -> str:
        """打印风险等级徽章"""
        color = self.RISK_COLORS.get(risk_level.lower(), "white")
        if risk_level.lower() == "critical":
            return self.color(f" {risk_level.upper()} ", color)
        return self.color(risk_level.upper(), color)

    def print_summary(self, summary: dict) -> None:
        """打印分析摘要"""
        self.print_header("ImpactForge - 分析摘要")
        
        print(f"  {self.bold('变更文件总数:')} {summary.get('total_files', 0)}")
        print(f"  {self.bold('平均风险评分:')} {summary.get('average_score', 0)}/100")
        print(f"  {self.bold('最高评分:')} {summary.get('max_score', 0)}/100")
        
        overall = summary.get('overall_risk', 'LOW')
        overall_color = self.RISK_COLORS.get(overall.lower(), 'white')
        print(f"  {self.bold('整体风险等级:')} {self.color(overall, overall_color)}")
        
        print()
        self.print_subheader("风险分布")
        
        risk_dist = summary.get('risk_distribution', {})
        total = summary.get('total_files', 1)
        
        for level in ['critical', 'high', 'medium', 'low']:
            count = risk_dist.get(level, 0)
            pct = (count / total * 100) if total > 0 else 0
            bar = '█' * int(pct / 5)
            color = self.RISK_COLORS.get(level, 'white')
            print(f"  {self.color(level.upper().ljust(8), color)} {bar:<20} {count:>3} ({pct:.1f}%)")

    def print_file_analysis(self, result) -> None:
        """打印单个文件分析结果"""
        risk_color = self.RISK_COLORS.get(result.risk_level.value, 'white')
        
        print()
        print(f"  {self.color('┌', 'dim')}{self.color('─' * 56, 'dim')}{self.color('┐', 'dim')}")
        print(f"  {self.color('│', 'dim')} {self.bold(result.file_path):<54}{self.color('│', 'dim')}")
        print(f"  {self.color('├', 'dim')}{self.color('─' * 56, 'dim')}{self.color('┤', 'dim')}")
        print(f"  {self.color('│', 'dim')} 风险等级: {self.print_risk_badge(result.risk_level.value):<45}{self.color('│', 'dim')}")
        print(f"  {self.color('│', 'dim')} 影响范围: {result.impact_scope.value.upper():<45}{self.color('│', 'dim')}")
        print(f"  {self.color('│', 'dim')} 评分: {str(result.score) + '/100':<49}{self.color('│', 'dim')}")
        print(f"  {self.color('│', 'dim')} 变更类型: {result.change_type.value:<45}{self.color('│', 'dim')}")
        print(f"  {self.color('└', 'dim')}{self.color('─' * 56, 'dim')}{self.color('┘', 'dim')}")
        
        if result.risk_factors:
            print(f"\n  {self.bold('风险因素:')}")
            for factor in result.risk_factors:
                print(f"    {self.color('•', 'yellow')} {factor}")
        
        if result.recommendations:
            print(f"\n  {self.bold('建议:')}")
            for rec in result.recommendations:
                print(f"    {self.color('→', 'green')} {rec}")

    def print_progress(self, current: int, total: int, message: str = "") -> None:
        """打印进度条"""
        width = 30
        pct = current / total if total > 0 else 0
        filled = int(width * pct)
        bar = self.color('█' * filled, 'cyan') + self.color('░' * (width - filled), 'dim')
        print(f"\r  [{bar}] {current}/{total} {message}", end='', flush=True)
        if current >= total:
            print()

    def print_table(self, headers: list, rows: list) -> None:
        """打印表格"""
        if not rows:
            return
        
        # 计算列宽
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # 打印表头
        header_line = "  " + " | ".join(
            self.bold(h.ljust(col_widths[i])) for i, h in enumerate(headers)
        )
        print(header_line)
        print("  " + "-+-".join("-" * w for w in col_widths))
        
        # 打印数据行
        for row in rows:
            print("  " + " | ".join(
                str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)
            ))

    def ask_yes_no(self, question: str, default: bool = True) -> bool:
        """询问是/否"""
        suffix = " [Y/n] " if default else " [y/N] "
        response = input(self.color(question + suffix, "yellow")).strip().lower()
        if not response:
            return default
        return response in ('y', 'yes')

    def ask_choice(self, question: str, choices: list) -> int:
        """询问选择"""
        print(self.color(question, "yellow"))
        for i, choice in enumerate(choices, 1):
            print(f"  {self.color(str(i), 'cyan')}. {choice}")
        while True:
            try:
                response = input(self.color("请选择 (1-{}): ".format(len(choices)), "yellow"))
                idx = int(response) - 1
                if 0 <= idx < len(choices):
                    return idx
            except ValueError:
                pass
            self.print_error("无效选择，请重试")
