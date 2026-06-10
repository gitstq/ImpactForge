<div align="center">

# 🔥 ImpactForge

**Smart Code Change Impact Analysis Engine**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-0-orange)](setup.py)
[![GitHub Stars](https://img.shields.io/github/stars/gitstq/ImpactForge?style=social)](https://github.com/gitstq/ImpactForge)

</div>

---

## 🎉 Introduction

**ImpactForge** is a lightweight, zero-dependency terminal CLI tool designed for developers to intelligently analyze the impact scope and risk level of Git code changes. It helps teams quickly identify potential risks during code reviews, pre-release checks, and CI/CD pipelines.

### Why ImpactForge?

- 🚀 **Zero Dependencies** - Pure Python standard library, no third-party packages required
- 🎯 **Smart Analysis** - Multi-dimensional risk assessment based on file paths, change types, and code content
- 📊 **Visual Reports** - Supports Mermaid charts, HTML reports, SARIF format
- 🔧 **Multi-Scenario** - Staged, working directory, commit ranges, branch comparison
- 🌈 **Colorful TUI** - Beautiful terminal interface with intuitive analysis results

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🔍 **Git Smart Parser** | Automatically parse diff, commit, branch changes |
| 🧠 **Impact Analysis** | Identify impact scope on modules/project/externals |
| ⚠️ **Risk Assessment** | Smart risk level evaluation (Low/Medium/High/Critical) |
| 📈 **Visual Graphs** | Generate Mermaid/PlantUML impact relationship diagrams |
| 📄 **Multi-Format Reports** | JSON / Markdown / HTML / SARIF |
| 🖥️ **TUI Interface** | Terminal graphical interface, beautiful and easy to use |

---

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (coming soon)
pip install impactforge

# Or install from source
git clone https://github.com/gitstq/ImpactForge.git
cd ImpactForge
pip install -e .
```

### Basic Usage

```bash
# Analyze all changes in current directory
impactforge

# Analyze staged changes
impactforge --staged

# Analyze last 3 commits
impactforge --commit HEAD~3..HEAD

# Analyze branch changes relative to main
impactforge --branch feature/new-feature

# Generate HTML report
impactforge --format html -o report.html

# Generate SARIF report for CI/CD
impactforge --format sarif -o results.sarif
```

---

## 📖 Detailed Usage Guide

### Command Line Arguments

```
impactforge [-h] [--version] [--path PATH]
            [--staged | --working | --commit REF | --branch BRANCH]
            [--format {json,markdown,html,sarif,table}] [--output FILE]
            [--no-color] [--verbose]
```

| Argument | Description |
|----------|-------------|
| `--path PATH` | Specify Git repository path |
| `--staged, -s` | Analyze staged changes |
| `--working, -w` | Analyze unstaged working changes |
| `--commit REF` | Analyze specific commit or range |
| `--branch BRANCH` | Analyze branch changes |
| `--format FORMAT` | Output format |
| `--output FILE` | Output file path |
| `--no-color` | Disable color output |
| `--verbose` | Show detailed output |

### Risk Levels

| Level | Score | Description |
|-------|-------|-------------|
| 🟢 LOW | 0-30 | Low risk, can merge normally |
| 🟡 MEDIUM | 31-60 | Medium risk, code review recommended |
| 🟠 HIGH | 61-80 | High risk, must review and test |
| 🔴 CRITICAL | 81-100 | Critical risk, security audit required |

---

## 💡 Design & Roadmap

### Architecture

```
┌─────────────────────────────────────────┐
│              ImpactForge CLI             │
├─────────────────────────────────────────┤
│  Git Parser → Impact Analyzer → Reporter │
├─────────────────────────────────────────┤
│  Visualizer → TUI → Multi-Format Output  │
└─────────────────────────────────────────┘
```

### Roadmap

- [x] v1.0.0 - Core features: Git parsing, impact analysis, risk assessment
- [ ] v1.1.0 - Support more languages (JavaScript, Go, Rust)
- [ ] v1.2.0 - AI-enhanced analysis (LLM integration for deep code review)
- [ ] v1.3.0 - CI/CD plugins (GitHub Actions, GitLab CI)
- [ ] v2.0.0 - Web dashboard and team collaboration

---

## 📦 Build & Deploy

### Local Build

```bash
# Install build dependencies
pip install build

# Build distribution packages
python -m build

# Generated files in dist/ directory
dist/
  ├── impactforge-1.0.0-py3-none-any.whl
  └── impactforge-1.0.0.tar.gz
```

### Run Tests

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/ -v
```

### CI/CD Integration

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

## 🤝 Contributing

We welcome all forms of contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📄 License

This project is open-sourced under the [MIT License](LICENSE).

---

<div align="center">

**Made with ❤️ by ImpactForge Team**

[GitHub](https://github.com/gitstq/ImpactForge) · [Issues](https://github.com/gitstq/ImpactForge/issues) · [Releases](https://github.com/gitstq/ImpactForge/releases)

</div>
