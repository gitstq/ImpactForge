#!/usr/bin/env python3
"""
ImpactForge CLI - 智能代码变更影响分析引擎
"""

import sys
import os
import argparse
from pathlib import Path

from .git_parser import GitParser
from .impact_analyzer import ImpactAnalyzer
from .reporter import Reporter
from .tui import TUI


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="impactforge",
        description="ImpactForge - 智能代码变更影响分析引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  impactforge                          # 分析工作目录的变更
  impactforge --staged                 # 分析暂存区变更
  impactforge --commit HEAD~3..HEAD    # 分析最近3个commit
  impactforge --branch feature/main    # 分析分支变更
  impactforge --format html -o report.html  # 输出HTML报告
        """
    )

    parser.add_argument(
        "--version", "-v",
        action="version",
        version="%(prog)s 1.0.0"
    )

    parser.add_argument(
        "--path", "-p",
        default=".",
        help="Git 仓库路径 (默认: 当前目录)"
    )

    # 分析范围选项
    scope_group = parser.add_mutually_exclusive_group()
    scope_group.add_argument(
        "--staged", "-s",
        action="store_true",
        help="分析暂存区变更"
    )
    scope_group.add_argument(
        "--working", "-w",
        action="store_true",
        help="分析工作区未暂存变更"
    )
    scope_group.add_argument(
        "--commit", "-c",
        metavar="REF",
        help="分析指定 commit 或 commit 范围 (如: HEAD~3..HEAD)"
    )
    scope_group.add_argument(
        "--branch", "-b",
        metavar="BRANCH",
        help="分析分支相对于 main 的变更"
    )

    # 输出选项
    parser.add_argument(
        "--format", "-f",
        choices=["json", "markdown", "html", "sarif", "table"],
        default="table",
        help="输出格式 (默认: table)"
    )
    parser.add_argument(
        "--output", "-o",
        metavar="FILE",
        help="输出文件路径 (默认: 输出到终端)"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="禁用颜色输出"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示详细输出"
    )

    return parser


def main() -> int:
    """主入口函数"""
    parser = create_parser()
    args = parser.parse_args()

    # 初始化 TUI
    tui = TUI()
    if args.no_color:
        tui.use_color = False

    # 打印欢迎信息
    tui.print_header("ImpactForge v1.0.0")
    tui.print_info("智能代码变更影响分析引擎")

    # 检查路径
    repo_path = Path(args.path).resolve()
    if not repo_path.exists():
        tui.print_error(f"路径不存在: {repo_path}")
        return 1

    # 初始化解析器
    git_parser = GitParser(str(repo_path))

    # 检查是否为 Git 仓库
    if not git_parser.is_git_repo():
        tui.print_error(f"不是 Git 仓库: {repo_path}")
        return 1

    tui.print_success(f"Git 仓库: {repo_path}")

    # 获取变更列表
    try:
        if args.staged:
            tui.print_info("分析暂存区变更...")
            changes = git_parser.get_staged_changes()
        elif args.working:
            tui.print_info("分析工作区变更...")
            changes = git_parser.get_working_changes()
        elif args.commit:
            tui.print_info(f"分析 commit: {args.commit}")
            if ".." in args.commit:
                from_ref, to_ref = args.commit.split("..", 1)
                changes = git_parser.get_changed_files(to_ref or "HEAD", from_ref)
            else:
                changes = git_parser.get_changed_files(args.commit)
        elif args.branch:
            tui.print_info(f"分析分支: {args.branch}")
            changes = git_parser.get_changed_files(args.branch, "main")
        else:
            tui.print_info("分析所有变更 (暂存区 + 工作区)...")
            changes = git_parser.get_all_changes()

    except RuntimeError as e:
        tui.print_error(str(e))
        return 1

    if not changes:
        tui.print_warning("未检测到代码变更")
        return 0

    tui.print_success(f"检测到 {len(changes)} 个文件变更")

    # 获取 diff 内容
    if args.verbose:
        tui.print_info("获取 diff 内容...")
        for i, change in enumerate(changes):
            tui.print_progress(i + 1, len(changes), f"解析 {change.path}")
            change.diff_content = git_parser.get_file_diff(change.path)

    # 影响分析
    tui.print_info("进行影响分析...")
    analyzer = ImpactAnalyzer(str(repo_path))
    results = analyzer.analyze(changes)

    # 生成摘要
    summary = analyzer.generate_summary(results)

    # 显示摘要
    tui.print_summary(summary)

    # 显示详细结果
    if args.verbose or args.format == "table":
        tui.print_subheader("详细分析")
        for result in results:
            tui.print_file_analysis(result)

    # 生成报告
    reporter = Reporter()
    
    if args.format == "json":
        output = reporter.generate_json(results, summary)
    elif args.format == "markdown":
        output = reporter.generate_markdown(results, summary)
    elif args.format == "html":
        output = reporter.generate_html(results, summary)
    elif args.format == "sarif":
        output = reporter.generate_sarif(results, summary)
    else:
        # table 格式已在上面显示
        return 0

    # 输出报告
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            tui.print_success(f"报告已保存: {args.output}")
        except IOError as e:
            tui.print_error(f"保存文件失败: {e}")
            return 1
    else:
        print()
        print(output)

    # 返回退出码
    overall_risk = summary.get("overall_risk", "LOW")
    if overall_risk == "CRITICAL":
        return 3
    elif overall_risk == "HIGH":
        return 2
    elif overall_risk == "MEDIUM":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
