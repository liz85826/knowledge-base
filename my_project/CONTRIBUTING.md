# Contributing to my_project

感谢你对本项目的兴趣！以下是参与贡献的指南。

## 行为准则

参与者应遵循友好、包容的社区准则。

## 如何贡献

### 报告 Bug

1. 搜索已有 Issues，确认没有重复
2. 使用 Bug Report 模板创建 Issue
3. 提供：复现步骤、期望行为、实际行为、环境信息

### 提交新功能

1. 先创建 Feature Request Issue 讨论方案
2. Fork 仓库，在新分支上开发
3. 确保测试覆盖率不降低
4. 更新 CHANGELOG.md
5. 提交 Pull Request

## 开发流程

```bash
# 安装开发依赖
pip install -e ".[dev]"
pre-commit install

# 运行测试
pytest

# 代码检查
ruff check . && ruff format . && mypy src/
```

## Commit 规范

使用 [Conventional Commits](https://www.conventionalcommits.org/)：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档变更
- `style:` 代码格式调整
- `refactor:` 重构
- `test:` 添加/修改测试
- `chore:` 构建/工具变更

## Pull Request 检查项

- [ ] 测试通过 (`pytest`)
- [ ] 代码风格检查通过 (`ruff`)
- [ ] 类型检查通过 (`mypy`)
- [ ] 已更新 CHANGELOG.md
- [ ] 已添加必要的测试
