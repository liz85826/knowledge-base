# 领域技能包完整示例

以下三个示例展示不同领域的技能包设计，覆盖 SKILL.md 结构与 IO 声明。

---

## 示例 1：PDF 处理技能包

**目录结构**
```
pdf-editor/
├── SKILL.md
├── scripts/
│   ├── rotate_pdf.py      # 旋转页面
│   ├── extract_text.py    # 提取文字
│   └── merge_pdf.py       # 合并文件
└── references/
    └── forms.md           # 表单填写高级指南
```

**SKILL.md 片段**
```yaml
---
name: pdf-editor
description: >
  PDF 文档处理工具。支持旋转页面、提取文字/表格、合并拆分文件、填写表单。
  当用户需要对 .pdf 文件执行任何操作时触发，包括：
  (1) 旋转/裁剪页面，(2) 提取文字或表格，
  (3) 合并多个 PDF，(4) 填写表单字段。
---
```

**IO 声明**
```markdown
### 旋转页面
输入：
- file_path: str   # 必填，绝对路径
- angle: int       # 必填，90 / 180 / 270
- pages: list[int] # 可选，默认全部

输出：
- 成功：新文件路径（原文件名加 _rotated 后缀）
- 失败：错误描述 + 原文件不受影响

验证：
- [ ] 输出文件可正常打开
- [ ] 页数与原文件一致
- [ ] 指定页面方向已改变
```

---

## 示例 2：数据分析技能包

**目录结构**
```
data-analysis/
├── SKILL.md
├── scripts/
│   ├── load_data.py       # 加载 CSV/Excel
│   ├── describe_stats.py  # 描述统计
│   └── plot_chart.py      # 生成图表
├── references/
│   └── chart-types.md     # 图表选型指南
└── assets/
    └── report_template.md # 报告模板
```

**SKILL.md 片段**
```yaml
---
name: data-analysis
description: >
  数据分析与可视化技能。处理 CSV/Excel/JSON 文件，
  生成统计摘要、图表、异常检测报告。
  当用户上传数据文件并要求分析、画图、找规律、做报告时触发。
---
```

**IO 声明**
```markdown
### 标准分析流程
输入：
- file_path: str    # 必填，.csv / .xlsx / .json
- goal: str         # 必填，用户自然语言描述分析目标

输出：
- Markdown 摘要报告（含结论和建议）
- 图表文件 PNG（文件名含时间戳）
- 数据质量说明（空值率、异常点数量）

验证：
- [ ] 处理行数与原文件一致
- [ ] 图表文件可正常打开
- [ ] 报告包含"结论"和"建议"两节
```

---

## 示例 3：营运管理计算技能包

**目录结构**
```
operations-mgmt/
├── SKILL.md
├── scripts/
│   ├── eoq_calculator.py   # 经济订购量计算
│   ├── reorder_point.py    # 再订货点计算
│   └── service_level.py    # 服务水平分析
├── references/
│   ├── formulas.md         # 所有公式汇总
│   ├── task1-4.md          # 任务1-4知识点
│   └── glossary.md         # 术语表
└── assets/
    └── calc_template.xlsx  # 计算辅助表格
```

**SKILL.md 片段**
```yaml
---
name: operations-mgmt
description: >
  营运管理计算与分析技能。覆盖库存管理、生产计划、服务水平、
  供应链优化等核心计算。当用户提出以下需求时触发：
  (1) 计算 EOQ（经济订购量）；
  (2) 确定再订货点 ROP；
  (3) 计算安全库存；
  (4) 分析服务水平与缺货概率；
  (5) 任务1-4相关公式推导与验算。
---
```

**IO 声明**
```markdown
### EOQ 计算
输入：
- demand_rate: float    # 必填，年需求量（单位/年）
- order_cost: float     # 必填，每次订购成本（元/次）
- holding_cost: float   # 必填，单位持有成本（元/单位/年）

输出：
- EOQ: float            # 经济订购量
- total_cost: float     # 最优总成本
- order_frequency: float # 年订购次数
- cycle_time: float     # 订购周期（天）

公式：EOQ = √(2DS/H)
  D = 年需求量
  S = 每次订购成本
  H = 单位持有成本

验证：
- [ ] EOQ > 0
- [ ] 总成本 = 订购成本 + 持有成本（两者应相等，为最优点验证）
- [ ] 与手算结果误差 < 0.01%

### 再订货点 ROP
输入：
- lead_time_demand: float   # 必填，提前期需求量
- safety_stock: float       # 可选，默认为 0

输出：
- ROP: float               # 再订货点库存水平
公式：ROP = d̄ × L + SS
  d̄ = 日均需求
  L = 提前期（天）
  SS = 安全库存

验证：
- [ ] ROP ≥ 提前期日均需求
- [ ] 有安全库存时 ROP > 无安全库存时的 ROP
```

---

## 通用 IO 声明模板

```markdown
### [功能名称]

**输入**
| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|---------|------|
| param1 | str  | 必填    | 描述 |
| param2 | int  | 可选    | 描述，默认值 X |

**输出**
- 成功：`{字段: 值, ...}` — 说明
- 失败：`{error: "类型", message: "原因"}` — 说明

**核心公式/逻辑**
```
公式或伪代码
```

**验证清单**
- [ ] 输出值在合理范围内
- [ ] 关键约束条件满足
- [ ] 与已知测试用例结果一致
```
