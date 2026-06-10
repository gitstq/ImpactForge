# 贡献指南

感谢您对 ImpactForge 的兴趣！我们欢迎所有形式的贡献。

## 如何贡献

### 报告问题

如果您发现了 bug 或有功能建议，请通过 GitHub Issues 提交：

1. 检查是否已有相关 issue
2. 使用 issue 模板提供详细信息
3. 包含复现步骤（如适用）

### 提交代码

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码规范

- 遵循 PEP 8 风格指南
- 添加适当的注释和文档字符串
- 确保代码通过所有测试
- 保持零依赖原则（仅使用 Python 标准库）

### 提交信息规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

## 开发环境

```bash
# 克隆仓库
git clone https://github.com/impactforge/impactforge.git
cd impactforge

# 安装开发模式
pip install -e .

# 运行测试
python -m pytest tests/
```

## 行为准则

请保持友善和尊重，共同维护开放的社区环境。
