---
name: skill-creation-guide
description: >
  AI 技能包设计与创建专家。帮助用户从零构建可复用、可执行、可验证、IO 明确的 AI 技能包（.skill 文件）。
  当用户提出以下需求时触发：(1) 创建/设计一个新的 AI 技能包；(2) 为某个领域制作 SKILL.md；
  (3) 规划技能包的目录结构、脚本、参考文档；(4) 打包或验证现有技能包；
  (5) 询问"如何让技能包可复用/可执行/可验证/IO明确"等设计问题。
---

# Skill Creation Guide

帮助创建满足「可复用 · 可执行 · 可验证 · IO 明确」四大目标的 AI 技能包。

## 四大目标速查

| 目标 | 核心手段 |
|------|---------|
| **可复用** | 泛化 description + 参数化设计 |
| **可执行** | 脚本化 + 自由度三级适配 |
| **可验证** | 显式成功标准 + 校验步骤 |
| **IO 明确** | 接口声明 + 示例驱动 |

## 标准目录结构

```
my-skill/
├── SKILL.md              ← 必须，核心控制文件
├── scripts/              ← 可选，可执行脚本
├── references/           ← 可选，参考文档（按需加载）
└── assets/               ← 可选，模板/素材
```

> ⚠️ 禁止创建 README.md、CHANGELOG.md 等辅助文档。

## 创建流程（6步）

```
步骤1  理解需求  →  收集具体使用案例，明确触发场景
步骤2  规划内容  →  识别重复劳动 → 转化为 scripts/references/assets
步骤3  初始化    →  运行 scripts/init_skill.py 生成目录骨架
步骤4  实现内容  →  写脚本、写参考文档、完善 SKILL.md
步骤5  打包分发  →  运行 scripts/package_skill.py 生成 .skill 文件
步骤6  迭代改进  →  实际使用中发现问题 → 更新内容
```

## SKILL.md 写作规范

### Frontmatter（触发机制）

```yaml
---
name: <技能名，小写加连字符>
description: >
  <一段话说明技能做什么 + 明确列举何时触发>
  触发条件：(1) ... (2) ... (3) ...
---
```

- `description` 是**唯一触发机制**，body 在触发后才加载
- **不要**在 frontmatter 添加其他字段
- 触发场景要穷举常见 pattern

### Body（执行指令）

使用**自由度三级模式**匹配任务特征：

- **高自由度**（文字说明）→ 多方案均可时
- **中自由度**（伪代码 + 参数声明）→ 有首选方案时
- **低自由度**（具体脚本 + 严格步骤）→ 易出错、需一致性时

详细模式说明：见 [references/freedom-levels.md](references/freedom-levels.md)

## IO 声明模板

```markdown
### 输入
- param_1: str    # 必填，说明
- param_2: int    # 可选，默认值，说明

### 输出
- 成功：<格式描述 + 示例>
- 失败：<错误类型 + 说明>

### 验证清单
- [ ] 输出文件大小 > 0
- [ ] 关键字段不为空
- [ ] 结果与预期格式匹配
```

## 渐进式加载（节约上下文）

```
第1级  name + description     ← 始终在上下文（~100词）
  ↓ 触发
第2级  SKILL.md body          ← 触发后加载（< 500行）
  ↓ 按需
第3级  scripts/references/assets  ← 仅在需要时加载
```

在 SKILL.md 中用如下格式引用子资源：

```markdown
- **高级功能 A**：见 [references/feature-a.md](references/feature-a.md)
- **批量处理**：见 [references/batch.md](references/batch.md)
```

## 完整领域示例

见 [references/domain-examples.md](references/domain-examples.md)，包含：
- PDF 处理技能包示例
- 数据分析技能包示例
- 营运管理计算技能包示例

## 打包与验证

```bash
# 初始化新技能包
python scripts/init_skill.py <skill-name> --path <output-dir>

# 打包（含自动校验）
python scripts/package_skill.py <path/to/skill-folder>
python scripts/package_skill.py <path/to/skill-folder> ./dist  # 指定输出目录
```

打包脚本会自动检查：
- YAML frontmatter 格式与必填字段
- 目录结构规范
- description 完整性
- 资源文件引用一致性
