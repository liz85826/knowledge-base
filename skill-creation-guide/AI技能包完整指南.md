# AI 技能包完整指南
## 可复用 · 可执行 · 可验证 · IO 明确

> 版本：v1.0 | 生成日期：2026-05-02

---

## 目录

1. [四大目标定义](#一四大目标定义)
2. [技能包标准结构](#二技能包标准结构)
3. [SKILL.md 完整规范](#三skillmd-完整规范)
4. [IO 声明规范](#四io-声明规范)
5. [自由度三级模式](#五自由度三级模式)
6. [渐进式加载设计](#六渐进式加载设计)
7. [创建六步流程](#七创建六步流程)
8. [完整领域示例](#八完整领域示例)
9. [验证清单](#九验证清单)
10. [工具脚本使用](#十工具脚本使用)

---

## 一、四大目标定义

| 目标 | 含义 | 核心手段 |
|------|------|---------|
| **可复用** | 同一技能包可在不同任务中反复触发，无需重新定制 | 泛化 description + 参数化设计 |
| **可执行** | AI 能直接按步骤完成任务，无需猜测或探索 | 脚本化 + 自由度三级适配 |
| **可验证** | 结果正确与否有明确判断依据，可独立检验 | 显式成功标准 + 校验步骤 |
| **IO 明确** | 输入/输出有清晰定义，参数类型、格式、约束无歧义 | 接口声明 + 示例驱动 |

---

## 二、技能包标准结构

```
my-skill/
├── SKILL.md                    ← 必须，核心控制文件（触发 + 执行指令）
├── scripts/                    ← 可选，可执行脚本（Python/Bash/JS）
│   ├── main_script.py          #   核心处理逻辑
│   └── helper.py               #   辅助工具
├── references/                 ← 可选，参考文档（按需加载到上下文）
│   ├── api_docs.md             #   API 文档、Schema
│   └── domain_knowledge.md     #   领域知识、业务规则
└── assets/                     ← 可选，模板/图片/字体等输出素材
    └── template.xlsx           #   报告模板、图片等
```

**⚠️ 禁止创建**：`README.md`、`CHANGELOG.md`、`INSTALLATION_GUIDE.md` 等辅助文档。  
技能包只存放 AI 执行任务所需的内容。

---

## 三、SKILL.md 完整规范

### 3.1 Frontmatter（触发机制）

```yaml
---
name: skill-name-kebab-case
description: >
  [一句话说明技能做什么，涵盖核心能力]。
  当用户提出以下需求时触发：
  (1) [触发场景1，要具体]；
  (2) [触发场景2，要具体]；
  (3) [触发场景3，要具体]。
---
```

**规则**：
- `description` 是**唯一触发机制**，body 在触发后才加载
- 不允许添加其他字段（仅 `name` + `description`）
- `name` 须为小写字母+数字+连字符，与目录名一致
- 触发场景要穷举典型使用模式

### 3.2 Body（执行指令）

使用**命令式/不定式**语态编写，要求：

```markdown
## [功能名称]

### 执行步骤
1. [步骤1，具体动作]
2. [步骤2，具体动作]

### IO 声明
输入：...
输出：...
验证：...

## 参考资源
- 详见 [references/xxx.md](references/xxx.md)
```

---

## 四、IO 声明规范

### 完整模板

```markdown
### 输入
| 参数名      | 类型        | 必填 | 默认值 | 说明           |
|------------|-------------|------|--------|----------------|
| param1     | str         | 是   | —      | 文件绝对路径    |
| param2     | int         | 否   | 0      | 处理数量上限    |
| param3     | list[str]   | 否   | []     | 过滤条件列表    |

### 输出
**成功**：
```json
{
  "status": "ok",
  "result": "<处理后的值>",
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

### 核心公式/逻辑
```
[伪代码或公式]
```

### 验证清单
- [ ] 输出字段完整，无 null 关键字段
- [ ] 数值在合理范围（如正数、百分比 ≤ 1）
- [ ] 结果与已知测试用例一致（误差 < 0.01%）
- [ ] 失败时原数据未被修改
```

---

## 五、自由度三级模式

### 高自由度（文字说明）
**适用**：多方案可行，Claude 可自主判断

```markdown
## 数据清洗
识别数据中的异常值和缺失值，
根据字段类型选择合适的填充或删除策略，
完成后报告处理了多少行、采用了什么策略。
```

### 中等自由度（伪代码 + 参数声明）
**适用**：有首选方案，允许适度变化

```markdown
## 文件转换
输入：input_path: str, output_format: str ("pdf"|"docx"|"html")
逻辑：
  if output_format not in ["pdf","docx","html"]:
      报错并列出支持格式
  调用对应转换脚本
输出：成功返回输出路径；失败返回错误类型
```

### 低自由度（严格步骤序列）
**适用**：操作脆弱、结果一致性要求高

```markdown
## 财务计算（严格按序执行）
1. 验证所有输入参数为正数，否则立即报错
2. 按公式 EOQ = √(2DS/H) 计算
3. 验证结果 > 0 且两项成本相等（最优点）
4. 四舍五入到整数
5. 返回结果和计算过程

错误处理：
- 负数输入 → 提示合法范围，不执行计算
- 除零风险 → 检查 H > 0，否则报错
```

### 选择决策树

```
任务失败代价大（数据损坏/财务错误）？
  └── 是 → 低自由度
  └── 否 → 有明确首选方案？
              └── 有 → 中等自由度
              └── 无 → 高自由度
```

---

## 六、渐进式加载设计

```
第1级  name + description     ← 始终在上下文（~100词）
    ↓ 技能触发
第2级  SKILL.md body          ← 触发后加载（< 500行 / < 5k词）
    ↓ 按需读取
第3级  scripts/references/assets  ← 仅在需要时加载
```

**SKILL.md 中引用子资源**：
```markdown
## 高级功能
- **表单填写详情**：见 [references/forms.md](references/forms.md)
- **批量处理指南**：见 [references/batch.md](references/batch.md)
- **错误代码参考**：见 [references/errors.md](references/errors.md)
```

**子文件超过 100 行**时，在文件顶部添加目录：
```markdown
## 目录
- [章节A](#章节a)
- [章节B](#章节b)
```

---

## 七、创建六步流程

```
┌─────────────────────────────────────────────────────────────┐
│  步骤1  理解需求                                              │
│         收集 3-5 个具体使用案例                               │
│         明确触发词和触发场景                                   │
├─────────────────────────────────────────────────────────────┤
│  步骤2  规划内容                                              │
│         识别重复劳动 → 脚本化                                  │
│         识别参考资料 → references/                            │
│         识别输出模板 → assets/                                │
├─────────────────────────────────────────────────────────────┤
│  步骤3  初始化                                                │
│         python scripts/init_skill.py <name> --path <dir>    │
├─────────────────────────────────────────────────────────────┤
│  步骤4  实现内容                                              │
│         ① 写并测试脚本（必须实际运行）                         │
│         ② 完善参考文档                                        │
│         ③ 填写 SKILL.md（IO声明、步骤、引用）                  │
├─────────────────────────────────────────────────────────────┤
│  步骤5  打包分发                                              │
│         python scripts/package_skill.py <skill-dir>         │
│         → 自动校验 + 生成 .skill 文件                         │
├─────────────────────────────────────────────────────────────┤
│  步骤6  迭代改进                                              │
│         实际使用 → 发现问题 → 更新内容 → 重新打包               │
└─────────────────────────────────────────────────────────────┘
```

---

## 八、完整领域示例

### 示例 A：营运管理计算技能包

```
operations-mgmt/
├── SKILL.md
├── scripts/
│   ├── eoq_calculator.py     # 经济订购量
│   ├── reorder_point.py      # 再订货点
│   └── service_level.py      # 服务水平分析
├── references/
│   ├── formulas.md           # 公式汇总
│   └── task1-4.md            # 任务1-4知识点
└── assets/
    └── calc_template.xlsx    # 计算辅助表格
```

**SKILL.md**：
```yaml
---
name: operations-mgmt
description: >
  营运管理计算与分析技能。覆盖库存管理、生产计划、服务水平分析。
  触发条件：(1) 计算 EOQ/经济订购量；(2) 确定再订货点 ROP；
  (3) 计算安全库存；(4) 分析服务水平与缺货概率；
  (5) 任务1-4相关公式推导与验算。
---
```

**IO 声明（EOQ 计算）**：
```markdown
输入：
- demand_rate: float  # 年需求量（单位/年）
- order_cost: float   # 每次订购成本（元/次）
- holding_cost: float # 单位持有成本（元/单位/年）

输出：
- EOQ: float          # 经济订购量（单位）
- total_cost: float   # 年总成本（元）
- cycle_time: float   # 订购周期（天）

公式：EOQ = √(2 × D × S / H)

验证：
- [ ] EOQ > 0
- [ ] 订购成本 ≈ 持有成本（最优点特征，误差 < 0.01%）
- [ ] 与手算结果一致
```

---

### 示例 B：PDF 处理技能包

```
pdf-editor/
├── SKILL.md
├── scripts/
│   ├── rotate_pdf.py
│   └── extract_text.py
└── references/
    └── forms.md
```

---

### 示例 C：数据分析技能包

```
data-analysis/
├── SKILL.md
├── scripts/
│   ├── load_data.py
│   └── plot_chart.py
├── references/
│   └── chart-types.md
└── assets/
    └── report_template.md
```

---

## 九、验证清单

### 结构规范
- [ ] 目录名 = `name` 字段值
- [ ] 存在 `SKILL.md`
- [ ] 无 `README.md`、`CHANGELOG.md` 等辅助文档
- [ ] 无 `.DS_Store`、`__pycache__` 等临时文件

### SKILL.md Frontmatter
- [ ] YAML 格式合法
- [ ] `name` 为小写字母+数字+连字符
- [ ] `description` ≥ 50 字符，包含触发条件
- [ ] 无多余字段
- [ ] 无 TODO 占位符

### SKILL.md Body
- [ ] Body ≥ 100 字符，≤ 500 行
- [ ] 所有引用文件实际存在
- [ ] IO 声明完整（输入/输出/验证）
- [ ] 无 TODO 占位符

### 脚本质量
- [ ] 有 docstring（用法/输入/输出说明）
- [ ] 有输入验证
- [ ] 成功退出码 0，失败非 0
- [ ] 已实际运行测试

### IO 明确性
- [ ] 每个参数有类型声明
- [ ] 明确标注必填/可选/默认值
- [ ] 成功/失败输出格式均有示例
- [ ] 有可执行验证清单

---

## 十、工具脚本使用

```bash
# 初始化新技能包
python scripts/init_skill.py <skill-name> --path <output-dir>
# 示例：
python scripts/init_skill.py operations-mgmt --path ./skills

# 校验 + 打包
python scripts/package_skill.py <path/to/skill-folder>
# 指定输出目录：
python scripts/package_skill.py ./operations-mgmt ./dist
```

**package_skill.py 自动校验项**：

| 检查项 | 失败后果 |
|--------|---------|
| SKILL.md 存在 | 终止，不打包 |
| frontmatter YAML 合法 | 终止，不打包 |
| name 格式 + 与目录名一致 | 终止，不打包 |
| description ≥ 50字符 | 终止，不打包 |
| 无 TODO 占位符 | 终止，不打包 |
| 引用文件存在 | 终止，不打包 |
| 无禁止辅助文档 | 终止，不打包 |

---

*本文档由 WorkBuddy 自动生成，对应技能包路径：`skill-creation-guide/`*
