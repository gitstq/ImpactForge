<div align="center">

# 🔥 ImpactForge

**智能代码变更影响分析引擎**

*Smart Code Change Impact Analysis Engine*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-0-orange)](setup.py)
[![GitHub Stars](https://img.shields.io/github/stars/gitstq/ImpactForge?style=social)](https://github.com/gitstq/ImpactForge)

</div>

---

## 🎉 项目介绍

**ImpactForge** 是一款轻量级、零依赖的终端 CLI 工具，专为开发者打造，用于智能分析 Git 代码变更的影响范围和风险等级。在代码审查、发布前检查、CI/CD 流程中，帮助团队快速识别潜在风险，提升代码质量。

### 为什么选择 ImpactForge？

- 🚀 **零依赖** - 纯 Python 标准库实现，无需安装任何第三方包
- 🎯 **智能分析** - 基于文件路径、变更类型、代码内容多维度风险评估
- 📊 **可视化报告** - 支持 Mermaid 图表、HTML 报告、SARIF 格式
- 🔧 **多场景支持** - 暂存区、工作区、Commit 范围、分支对比
- 🌈 **彩色终端** - 美观的 TUI 界面，直观展示分析结果

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🔍 **Git 智能解析** | 自动解析 diff、commit、branch 等变更信息 |
| 🧠 **影响范围分析** | 识别变更对模块/项目/外部的影响范围 |
| ⚠️ **风险评估引擎** | 智能评估风险等级（低/中/高/严重） |
| 📈 **可视化图谱** | 生成 Mermaid/PlantUML 影响关系图 |
| 📄 **多格式报告** | JSON / Markdown / HTML / SARIF |
| 🖥️ **TUI 交互界面** | 终端图形化操作，美观易用 |

---

## 🚀 快速开始

### 安装

```bash
# 从 PyPI 安装 (即将发布)
pip install impactforge

# 或从源码安装
git clone https://github.com/gitstq/ImpactForge.git
cd ImpactForge
pip install -e .
```

### 基本使用

```bash
# 分析当前目录的所有变更
impactforge

# 分析暂存区变更
impactforge --staged

# 分析最近 3 个 commit
impactforge --commit HEAD~3..HEAD

# 分析分支相对于 main 的变更
impactforge --branch feature/new-feature

# 生成 HTML 报告
impactforge --format html -o report.html

# 生成 SARIF 报告（用于 CI/CD）
impactforge --format sarif -o results.sarif
```

### 示例输出

```
============================================================
  ImpactForge v1.0.0
============================================================

ℹ Git 仓库: /path/to/your/repo
✓ 检测到 3 个文件变更

▶ 分析摘要
──────────────────────────────────────────────────
  变更文件总数: 3
  平均风险评分: 45.0/100
  最高评分: 75/100
  整体风险等级: MEDIUM

▶ 风险分布
──────────────────────────────────────────────────
  LOW      ░░░░░░░░░░░░░░░░░░░░   1 (33.3%)
  MEDIUM   ██████░░░░░░░░░░░░░░   1 (33.3%)
  HIGH     ███████████░░░░░░░░░   1 (33.3%)
```

---

## 📖 详细使用指南

### 命令行参数

```
impactforge [-h] [--version] [--path PATH]
            [--staged | --working | --commit REF | --branch BRANCH]
            [--format {json,markdown,html,sarif,table}] [--output FILE]
            [--no-color] [--verbose]
```

| 参数 | 说明 |
|------|------|
| `--path PATH` | 指定 Git 仓库路径 |
| `--staged, -s` | 分析暂存区变更 |
| `--working, -w` | 分析工作区未暂存变更 |
| `--commit REF` | 分析指定 commit 或范围 |
| `--branch BRANCH` | 分析分支变更 |
| `--format FORMAT` | 输出格式 |
| `--output FILE` | 输出文件路径 |
| `--no-color` | 禁用颜色输出 |
| `--verbose` | 显示详细输出 |

### 风险等级说明

| 等级 | 评分 | 说明 |
|------|------|------|
| 🟢 LOW | 0-30 | 低风险，可按正常流程合并 |
| 🟡 MEDIUM | 31-60 | 中等风险，建议代码审查 |
| 🟠 HIGH | 61-80 | 高风险，必须进行审查和测试 |
| 🔴 CRITICAL | 81-100 | 严重风险，需要安全审计 |

---

## 💡 设计思路与迭代规划

### 架构设计

```
┌─────────────────────────────────────────┐
│              ImpactForge CLI             │
├─────────────────────────────────────────┤
│  Git Parser → Impact Analyzer → Reporter │
├─────────────────────────────────────────┤
│  Visualizer → TUI → Multi-Format Output  │
└─────────────────────────────────────────┘
```

### 迭代路线图

- [x] v1.0.0 - 核心功能：Git 解析、影响分析、风险评估
- [ ] v1.1.0 - 支持更多语言（JavaScript、Go、Rust）
- [ ] v1.2.0 - AI 增强分析（集成 LLM 进行深度代码审查）
- [ ] v1.3.0 - CI/CD 插件（GitHub Actions、GitLab CI）
- [ ] v2.0.0 - Web 仪表盘和团队协作功能

---

## 📦 打包与部署指南

### 本地构建

```bash
# 安装构建依赖
pip install build

# 构建分发包
python -m build

# 生成的文件在 dist/ 目录
dist/
  ├── impactforge-1.0.0-py3-none-any.whl
  └── impactforge-1.0.0.tar.gz
```

### 运行测试

```bash
# 安装测试依赖
pip install pytest

# 运行测试
pytest tests/ -v
```

### CI/CD 集成

```yaml
# .github/workflows/impact-analysis.yml
name: Impact Analysis
on: [pull_request]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install impactforge
      - run: impactforge --format sarif -o results.sarif
      - uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: results.sarif
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 快速贡献步骤

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 📄 开源协议

本项目采用 [MIT 协议](LICENSE) 开源。

---

<div align="center">

**Made with ❤️ by ImpactForge Team**

[GitHub](https://github.com/gitstq/ImpactForge) · [Issues](https://github.com/gitstq/ImpactForge/issues) · [Releases](https://github.com/gitstq/ImpactForge/releases)

</div>
