# 技能包验证清单

在运行 `package_skill.py` 打包前，对照以下清单逐项检查。

---

## 一、结构规范

- [ ] 目录名与 `SKILL.md` 中的 `name` 字段完全一致
- [ ] 存在 `SKILL.md`（必须）
- [ ] 不包含 `README.md`、`CHANGELOG.md` 等辅助文档
- [ ] 目录中没有与技能无关的临时文件（`.DS_Store`、`__pycache__`、`*.pyc` 等）

## 二、SKILL.md Frontmatter

- [ ] 以 `---` 开头，格式为合法 YAML
- [ ] `name`：小写字母+数字+连字符，以字母开头
- [ ] `description`：≥ 50 字符，说明了"做什么"和"何时触发"
- [ ] 无多余字段（仅允许 `name` 和 `description`）
- [ ] 所有 TODO 占位符已填写

## 三、SKILL.md Body

- [ ] Body 内容 ≥ 100 字符
- [ ] 所有 TODO 占位符已填写
- [ ] 引用的资源文件（`references/`、`scripts/`、`assets/`）均实际存在
- [ ] IO 声明完整（输入参数、输出格式、验证清单）
- [ ] 执行步骤有明确的自由度级别（高/中/低）

## 四、脚本质量

- [ ] 所有脚本有 docstring 说明（用法、输入、输出）
- [ ] 所有脚本有输入验证（文件存在、参数合法等）
- [ ] 所有脚本有明确的成功/失败退出码（0/非0）
- [ ] 核心脚本已实际运行测试，不只是伪代码
- [ ] 错误信息输出到 stderr，正常输出到 stdout

## 五、IO 明确性

- [ ] 每个功能都有参数类型声明（str/int/float/list 等）
- [ ] 明确标注哪些参数必填、哪些可选（含默认值）
- [ ] 成功输出有格式示例
- [ ] 失败情况有错误类型枚举
- [ ] 有可执行的验证清单（checkbox 格式）

## 六、可复用性

- [ ] 无硬编码路径（使用参数传入）
- [ ] 无硬编码密钥或凭证
- [ ] 触发场景足够泛化（description 覆盖了典型使用模式）
- [ ] 脚本支持命令行参数，可独立运行

## 七、渐进式加载

- [ ] SKILL.md body ≤ 500 行
- [ ] 详细内容已拆分到 `references/` 子文件
- [ ] SKILL.md 中明确引用了所有子文件及其适用场景
- [ ] 子文件 > 100 行时有目录（Table of Contents）

---

## 自动校验（package_skill.py 检查项）

运行 `python scripts/package_skill.py <skill-dir>` 时自动验证：

| 检查项 | 说明 |
|--------|------|
| SKILL.md 存在 | 必须文件缺失则终止 |
| frontmatter 格式 | YAML 解析成功 |
| name 格式 | 小写字母+数字+连字符 |
| name 与目录名一致 | 防止分发后名称混乱 |
| description 长度 | ≥ 50 字符 |
| description 无 TODO | 占位符未填写 |
| body 无 TODO | 占位符未填写 |
| body 长度 | ≥ 100 字符 |
| 引用文件存在 | 防止死链接 |
| 无禁止辅助文档 | README.md 等 |
