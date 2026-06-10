<div align="center">

# 🔥 ImpactForge

**智能代碼變更影響分析引擎**

*Smart Code Change Impact Analysis Engine*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-0-orange)](setup.py)
[![GitHub Stars](https://img.shields.io/github/stars/gitstq/ImpactForge?style=social)](https://github.com/gitstq/ImpactForge)

</div>

---

## 🎉 項目介紹

**ImpactForge** 是一款輕量級、零依賴的終端 CLI 工具，專為開發者打造，用於智能分析 Git 代碼變更的影響範圍和風險等級。在代碼審查、發布前檢查、CI/CD 流程中，幫助團隊快速識別潛在風險，提升代碼質量。

### 為什麼選擇 ImpactForge？

- 🚀 **零依賴** - 純 Python 標準庫實現，無需安裝任何第三方套件
- 🎯 **智能分析** - 基於文件路徑、變更類型、代碼內容多維度風險評估
- 📊 **可視化報告** - 支援 Mermaid 圖表、HTML 報告、SARIF 格式
- 🔧 **多場景支援** - 暫存區、工作區、Commit 範圍、分支對比
- 🌈 **彩色終端** - 美觀的 TUI 介面，直觀展示分析結果

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🔍 **Git 智能解析** | 自動解析 diff、commit、branch 等變更資訊 |
| 🧠 **影響範圍分析** | 識別變更對模組/項目/外部的影響範圍 |
| ⚠️ **風險評估引擎** | 智能評估風險等級（低/中/高/嚴重） |
| 📈 **可視化圖譜** | 生成 Mermaid/PlantUML 影響關係圖 |
| 📄 **多格式報告** | JSON / Markdown / HTML / SARIF |
| 🖥️ **TUI 交互介面** | 終端圖形化操作，美觀易用 |

---

## 🚀 快速開始

### 安裝

```bash
# 從 PyPI 安裝 (即將發布)
pip install impactforge

# 或從原始碼安裝
git clone https://github.com/gitstq/ImpactForge.git
cd ImpactForge
pip install -e .
```

### 基本使用

```bash
# 分析當前目錄的所有變更
impactforge

# 分析暫存區變更
impactforge --staged

# 分析最近 3 個 commit
impactforge --commit HEAD~3..HEAD

# 分析分支相對於 main 的變更
impactforge --branch feature/new-feature

# 生成 HTML 報告
impactforge --format html -o report.html

# 生成 SARIF 報告（用於 CI/CD）
impactforge --format sarif -o results.sarif
```

---

## 📖 詳細使用指南

### 命令列參數

```
impactforge [-h] [--version] [--path PATH]
            [--staged | --working | --commit REF | --branch BRANCH]
            [--format {json,markdown,html,sarif,table}] [--output FILE]
            [--no-color] [--verbose]
```

| 參數 | 說明 |
|------|------|
| `--path PATH` | 指定 Git 倉庫路徑 |
| `--staged, -s` | 分析暫存區變更 |
| `--working, -w` | 分析工作區未暫存變更 |
| `--commit REF` | 分析指定 commit 或範圍 |
| `--branch BRANCH` | 分析分支變更 |
| `--format FORMAT` | 輸出格式 |
| `--output FILE` | 輸出檔案路徑 |
| `--no-color` | 禁用顏色輸出 |
| `--verbose` | 顯示詳細輸出 |

### 風險等級說明

| 等級 | 評分 | 說明 |
|------|------|------|
| 🟢 LOW | 0-30 | 低風險，可按正常流程合併 |
| 🟡 MEDIUM | 31-60 | 中等風險，建議代碼審查 |
| 🟠 HIGH | 61-80 | 高風險，必須進行審查和測試 |
| 🔴 CRITICAL | 81-100 | 嚴重風險，需要安全審計 |

---

## 💡 設計思路與迭代規劃

### 架構設計

```
┌─────────────────────────────────────────┐
│              ImpactForge CLI             │
├─────────────────────────────────────────┤
│  Git Parser → Impact Analyzer → Reporter │
├─────────────────────────────────────────┤
│  Visualizer → TUI → Multi-Format Output  │
└─────────────────────────────────────────┘
```

### 迭代路線圖

- [x] v1.0.0 - 核心功能：Git 解析、影響分析、風險評估
- [ ] v1.1.0 - 支援更多語言（JavaScript、Go、Rust）
- [ ] v1.2.0 - AI 增強分析（整合 LLM 進行深度代碼審查）
- [ ] v1.3.0 - CI/CD 外掛（GitHub Actions、GitLab CI）
- [ ] v2.0.0 - Web 儀表板和團隊協作功能

---

## 📦 打包與部署指南

### 本地構建

```bash
# 安裝構建依賴
pip install build

# 構建分發包
python -m build

# 生成的檔案在 dist/ 目錄
dist/
  ├── impactforge-1.0.0-py3-none-any.whl
  └── impactforge-1.0.0.tar.gz
```

### 執行測試

```bash
# 安裝測試依賴
pip install pytest

# 執行測試
pytest tests/ -v
```

### CI/CD 整合

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

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！請查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解詳情。

---

## 📄 開源協議

本項目採用 [MIT 協議](LICENSE) 開源。

---

<div align="center">

**Made with ❤️ by ImpactForge Team**

[GitHub](https://github.com/gitstq/ImpactForge) · [Issues](https://github.com/gitstq/ImpactForge/issues) · [Releases](https://github.com/gitstq/ImpactForge/releases)

</div>
