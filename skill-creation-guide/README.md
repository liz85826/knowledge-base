# AI 技能包完整指南 — `skill-creation-guide`

> 版本：v1.0 | 最后更新：2026-05-02
> 适用对象：希望为 AI 助手构建可复用技能包的开发者、分析师、运维工程师

---

## 目录

1. [项目简介](#项目简介)
2. [核心概念速查](#核心概念速查)
3. [安装与前置依赖](#安装与前置依赖)
4. [十分钟快速上手](#十分钟快速上手)
5. [SKILL.md 写作规范](#skillmd-写作规范)
6. [自由度三级模式](#自由度三级模式)
7. [IO 声明模板](#io-声明模板)
8. [渐进式加载设计](#渐进式加载设计)
9. [工具脚本详解](#工具脚本详解)
10. [完整领域示例](#完整领域示例)
11. [打包与分发](#打包与分发)
12. [验证清单](#验证清单)
13. [FAQ](#faq)

---

## 项目简介

`skill-creation-guide` 提供一套完整的 **AI 技能包设计方法论 + 可执行工具脚本**，帮助你（或 AI 助手）创建符合四大目标的技能包：

| 目标 | 含义 | 核心手段 |
|------|------|---------|
| **可复用** | 可在不同任务中反复触发，无需重新定制 | 泛化 description + 参数化设计 |
| **可执行** | AI 能直接按步骤完成任务 | 脚本化 + 自由度三级适配 |
| **可验证** | 结果正确与否有明确判断依据 | 显式成功标准 + 校验步骤 |
| **IO 明确** | 输入/输出有清晰定义 | 接口声明 + 示例驱动 |

### 为什么需要技能包？

直接将指令写在 prompt 里也能用，但有三个问题：

1. **不可复用**：每次对话都要重新说明，无法跨会话保留
2. **浪费上下文**：长指令每次都占用 token
3. **无法验证**：没有标准格式，AI 执行质量参差不齐

技能包通过**渐进式加载**解决以上问题（详见[第8节](#渐进式加载设计)）。

---

## 核心概念速查

| 概念 | 一句话解释 |
|------|-----------|
| **SKILL.md** | 技能包唯一必须文件。frontmatter 控制触发，body 控制执行 |
| **description 触发机制** | `description` 字段是唯一触发入口，body 不在普通上下文中 |
| **自由度三级** | 高/中/低自由度，匹配任务的可变程度（详见第6节） |
| **IO 声明** | 每个功能模块都要声明输入、输出、验证清单（详见第7节） |
| **.skill 文件** | 实为 ZIP 格式，双击即可安装到 WorkBuddy |

---

## 安装与前置依赖

```bash
# 唯一依赖
pip install pyyaml

# 验证
python -c "import yaml; print('OK')"
```

**系统要求**：Python ≥ 3.9，Windows/macOS/Linux 均可。

---

## 十分钟快速上手

### Step 1：初始化骨架

```bash
python scripts/init_skill.py pdf-editor --path ./skills
```

生成结构：
```
skills/pdf-editor/
├── SKILL.md                ← 含 TODO，需手动完善
├── scripts/
│   └── example_script.py
├── references/
│   └── example_reference.md
└── assets/
    └── .gitkeep
```

### Step 2：完善 SKILL.md

打开 `skills/pdf-editor/SKILL.md`，填写所有 TODO：

```yaml
---
name: pdf-editor
description: >
  PDF 文档处理工具。支持旋转、合并、提取文字。
  触发条件：(1) 旋转 PDF 页面；(2) 合并多个 PDF；(3) 提取文字。
---
```

### Step 3：实现脚本

在 `scripts/` 中编写可独立运行的脚本（见[第9节](#工具脚本详解)示例）。

### Step 4：打包

```bash
python scripts/package_skill.py ./skills/pdf-editor
```

校验通过后生成 `pdf-editor.skill`，双击即可安装。

---

## SKILL.md 写作规范

### Frontmatter（唯一触发机制）

```yaml
---
name: pdf-editor
description: >
  一句话说明技能做什么。
  触发条件：(1) 场景一；(2) 场景二；(3) 场景三。
---
```

**规则**：

| 规则 | 原因 |
|------|------|
| `description` 是唯一触发机制 | body 在触发前不在上下文 |
| 只允许 `name` + `description` | 多余字段无意义且增加维护成本 |
| `name` 与目录名必须一致 | `package_skill.py` 会校验，不一致则拒绝打包 |
| 触发场景要穷举 | AI 无法触发一个它不知道自己能做的技能 |

### Body（执行指令）

每个功能模块按此格式编写：

```markdown
## [功能名称]

### 输入
- param1: str    # 必填，说明
- param2: int    # 可选，默认值，说明

### 执行步骤
1. 步骤一（具体动作）
2. 步骤二

### 输出
- 成功：格式描述 + 示例
- 失败：错误类型 + 处理说明

### 验证清单
- [ ] 验证项一
- [ ] 验证项二
```

**引用子资源**（渐进式加载的关键）：

```markdown
## 高级功能
- **批量处理**：> 10 个文件时，
  详见 [references/batch.md](references/batch.md)
- **错误代码**：见 [references/errors.md](references/errors.md)
```

---

## 自由度三级模式

根据任务特征选择对应级别（详见 [references/freedom-levels.md](references/freedom-levels.md)）。

### 决策树

```
任务是否有"唯一正确执行序列"？
├── 是 → 低自由度
└── 否 → 失败代价大吗？
          ├── 大 → 低自由度
          └── 一般 → 有首选方案？
                      ├── 有 → 中等自由度
                      └── 无 → 高自由度
```

### 高自由度（文字说明）

适用：创意类、分析类，方案不唯一。

```markdown
## 数据清洗
识别数据中的异常值和缺失值，
根据字段类型选择合适的填充或删除策略，
完成后报告处理了哪些列、采用了什么策略。
注意：删除行之前必须征得用户确认。
```

### 中等自由度（伪代码 + 参数声明）

适用：数据处理、格式转换，核心逻辑固定。

```markdown
## 文件转换
输入：input_path: str, output_format: str ("pdf"|"docx"|"html")
逻辑：
  if output_format not in ["pdf","docx","html"]:
      返回错误，列出支持格式
  调用 scripts/convert.py
输出：成功返回输出路径；失败返回错误类型
```

### 低自由度（严格步骤序列）

适用：文件操作、财务计算等高风险任务。

```markdown
## EOQ 计算（严格按序执行）

1. 验证 demand_rate > 0，否则报错终止
2. 验证 order_cost > 0，否则报错终止
3. 验证 holding_cost > 0，否则报错终止
4. 计算 EOQ = sqrt(2 * D * S / H)
5. 验证：订购成本 ≈ 持有成本（误差 < 0.01%）
6. 返回结果 JSON

错误处理：
| 错误类型     | 处理方式              |
|-------------|-----------------------|
| 参数 ≤ 0   | 立即终止，返回错误    |
| 计算 NaN    | 建议检查输入数量级    |
```

---

## IO 声明模板

每个功能模块都必须包含完整 IO 声明（可直接复制使用）：

```markdown
### [功能名称]

#### 输入
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| param1 | str  | 是   | —      | 文件绝对路径 |
| param2 | int  | 否   | 0      | 处理数量上限 |

#### 输出
**成功**：
```json
{
  "status": "ok",
  "result": "<值>",
  "count": 42
}
```

**失败**：
```json
{
  "status": "error",
  "error_type": "FILE_NOT_FOUND | INVALID_PARAM | PROCESS_FAILED",
  "message": "具体原因描述"
}
```

#### 核心公式
```
EOQ = √(2 × D × S / H)
```

#### 验证清单
- [ ] 输出字段完整，无 null 关键字段
- [ ] 数值在合理范围
- [ ] 与已知测试用例一致（误差 < 0.01%）
- [ ] 失败时原数据未被修改
```

---

## 渐进式加载设计

### 为什么需要？

AI 上下文窗口有限。技能包的参考资料可能有 5000 词，但某次任务只需要其中 200 词，全部加载是浪费。

### 三级加载策略

```
第1级  name + description     ← 始终在上下文（~100 词）
    ↓ 技能被触发
第2级  SKILL.md body        ← 触发后加载（建议 < 500 行）
    ↓ 任务需要更多细节
第3级  scripts/references/   ← 仅在需要时读取
```

### 引用子资源格式

```markdown
## 进阶功能
- **批量处理**：> 10 个文件时，
  详见 [references/batch.md](references/batch.md)
- **错误代码**：见 [references/errors.md](references/errors.md)
```

### 子文件 > 100 行时加目录

```markdown
## 目录
- [API 端点](#api-端点)
- [错误代码](#错误代码)
```

---

## 工具脚本详解

### `init_skill.py` — 初始化骨架

```bash
python scripts/init_skill.py <skill-name> --path <output-dir>

# 示例
python scripts/init_skill.py pdf-editor --path ./skills
python scripts/init_skill.py operations-mgmt --path .
```

**名称格式**：`^[a-z][a-z0-9-]*$`，脚本会自动校验，不合法则拒绝。

**生成内容**：

| 文件 | 用途 | 后续操作 |
|------|------|---------|
| `SKILL.md` | 核心技能文件，含 TODO | 必须手动填写所有 TODO |
| `scripts/example_script.py` | 带 docstring 的脚本模板 | 修改或删除 |
| `references/example_reference.md` | 参考文档模板 | 修改或删除 |
| `assets/.gitkeep` | 保留空目录 | 放入实际素材 |

---

### `package_skill.py` — 校验并打包

```bash
python scripts/package_skill.py <skill-folder> [output-dir]

# 示例
python scripts/package_skill.py ./skills/pdf-editor
python scripts/package_skill.py ./skills/pdf-editor ./dist
```

**自动校验项**（任一失败则拒绝打包）：

| # | 检查项 | 失败提示 |
|---|--------|---------|
| 1 | `SKILL.md` 存在 | `缺少必须文件：SKILL.md` |
| 2 | frontmatter 为合法 YAML | `YAML frontmatter 解析失败` |
| 3 | `name` 格式合法 | `name 格式不合法` |
| 4 | `name` 与目录名一致 | `name 与目录名不一致` |
| 5 | `description` ≥ 50 字符 | `description 过短` |
| 6 | 无 TODO 占位符 | `包含未填写的 TODO 占位符` |
| 7 | 引用文件实际存在 | `引用的资源文件不存在：...` |
| 8 | 无禁止辅助文档 | `不应包含辅助文档：README.md` |

**.skill 文件格式说明**：实为 ZIP，可用任意解压工具打开查看。

---

## 完整领域示例

详见 [references/domain-examples.md](references/domain-examples.md)，以下为摘要。

### 示例 1：PDF 处理技能包

```
pdf-editor/
├── SKILL.md
├── scripts/
│   ├── rotate_pdf.py
│   ├── extract_text.py
│   └── merge_pdf.py
└── references/
    └── forms.md
```

**SKILL.md 触发片段**：
```yaml
---
name: pdf-editor
description: >
  PDF 文档处理工具。支持旋转、提取文字、合并、填写表单。
  触发条件：(1) 旋转/裁剪页面；(2) 提取文字或表格；
  (3) 合并多个 PDF；(4) 填写表单字段。
---
```

---

### 示例 2：营运管理计算技能包

```
operations-mgmt/
├── SKILL.md
├── scripts/
│   ├── eoq_calculator.py     # 经济订购量
│   ├── reorder_point.py       # 再订货点
│   └── service_level.py       # 服务水平分析
├── references/
│   ├── formulas.md            # 所有公式汇总
│   ├── task1-4.md             # 任务1-4 知识点
│   └── glossary.md            # 术语表
└── assets/
    └── calc_template.xlsx     # 计算辅助表格
```

**核心公式**：

```
EOQ = √(2 × D × S / H)
ROP = 平均日需求 × 提前期 + 安全库存
安全库存 SS = z × σd × √L
  （z = 服务水平系数，σd = 需求标准差，L = 提前期）
```

---

### 示例 3：数据分析技能包

```
data-analysis/
├── SKILL.md
├── scripts/
│   ├── load_data.py
│   ├── describe_stats.py
│   └── plot_chart.py
├── references/
│   └── chart-types.md
└── assets/
    └── report_template.md
```

---

## 打包与分发

### 完整打包流程

```bash
# 1. 校验（package_skill.py 自动执行）
python scripts/package_skill.py ./skills/my-skill

# 2. 校验通过，生成 .skill 文件
#    输出：./skills/my-skill.skill

# 3. 指定输出目录
python scripts/package_skill.py ./skills/my-skill ./dist
#    输出：./dist/my-skill.skill
```

### 分发方式

将 `.skill` 文件发送给其他用户，**双击即可安装到 WorkBuddy**。

> 💡 `.skill` 文件实为 ZIP 格式，可用 `unzip -l xxx.skill` 查看内容。

---

## 验证清单

运行打包前，**必须**对照以下清单自查（完整版见 [references/verification-checklist.md](references/verification-checklist.md)）。

### 结构规范
- [ ] 目录名 = `name` 字段值
- [ ] 存在 `SKILL.md`
- [ ] 无 `README.md`、`CHANGELOG.md` 等辅助文档
- [ ] 无临时文件（`.DS_Store`、`__pycache__` 等）

### SKILL.md Frontmatter
- [ ] YAML 格式合法（以 `---` 开头）
- [ ] `name`：小写字母+数字+连字符，以字母开头
- [ ] `description`：≥ 50 字符，说明了触发条件
- [ ] 无多余字段（仅允许 `name` 和 `description`）
- [ ] 所有 TODO 占位符已填写

### 脚本质量
- [ ] 所有脚本有 docstring（用法/输入/输出说明）
- [ ] 所有脚本有输入验证
- [ ] 成功退出码 0，失败非 0
- [ ] **已实际运行测试**（不只停留在伪代码）

### IO 明确性
- [ ] 每个参数有类型声明
- [ ] 明确标注必填/可选/默认值
- [ ] 成功/失败输出均有格式示例
- [ ] 有可执行的验证清单

---

## FAQ

### Q：技能包里能不能放 README.md？
**A：不能。** 技能包只存放 AI 执行任务所需的内容。`README.md` 是给人看的，会增加 AI 上下文负担。`skill-creation-guide` 里的 `README.md` 是项目级的说明文件，不是技能包内容。

### Q：description 写多长合适？
**A：** 建议 50~200 字符。要回答两个问题："这个技能做什么？"、"什么时候应该触发它？" 触发场景要穷举，宁多勿少。

### Q：scripts/ 里的脚本必须用 Python 吗？
**A：** 不一定。可以用 Bash、Node.js、PowerShell 等任何可执行的脚本语言，只要在目标环境里能运行即可。

### Q：如何判断应该用哪个自由度级别？
**A：** 用决策树（见[第6节](#自由度三级模式)）。核心判断标准：任务失败会不会造成严重后果？会 → 低自由度；不会 → 看有没有首选方案。

### Q：.skill 文件能逆向看内容吗？
**A：** 能。`.skill` 实为 ZIP 格式，直接改扩展名或用解压工具打开即可查看所有文件。

---

## 与 qiushi-skill 集成说明

`skill-creation-guide` 可与 `qiushi-skill`（已安装在你的 WorkBuddy 中）协同使用：

```
qiushi-skill 提供：方法论框架（矛盾分析法、调查研究等）
    ↓ 指导
设计技能包的"执行逻辑"和"分析框架"
    ↓ 写入
SKILL.md 的 body 部分
    ↓ 打包
生成 .skill 文件，分发给其他用户
```

**建议流程**：
1. 用 `qiushi-skill` 的方法论分析任务本质
2. 将分析方法转化为 SKILL.md 中的执行步骤
3. 用 `init_skill.py` 初始化技能包骨架
4. 用 `package_skill.py` 打包分发

---

## 参考资料

| 文件 | 内容 |
|------|------|
| [AI技能包完整指南.md](AI技能包完整指南.md) | 本技能包的配套完整设计指南（中文） |
| [references/domain-examples.md](references/domain-examples.md) | PDF/数据分析/营运管理 完整示例 |
| [references/freedom-levels.md](references/freedom-levels.md) | 自由度三级模式详解 |
| [references/verification-checklist.md](references/verification-checklist.md) | 发布前完整验证清单 |

---

## License

MIT License — 可自由使用、修改和分发。

