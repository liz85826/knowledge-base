#!/usr/bin/env python3
"""
init_skill.py — 技能包目录初始化脚本

用法：
    python scripts/init_skill.py <skill-name> --path <output-directory>

示例：
    python scripts/init_skill.py pdf-editor --path ./skills
    python scripts/init_skill.py data-analysis --path ~/my-skills

输出：
    在 <output-directory>/<skill-name>/ 下生成标准技能包骨架
"""

import argparse
import os
import sys
import textwrap
from pathlib import Path


SKILL_MD_TEMPLATE = """\
---
name: {skill_name}
description: >
  TODO: 用一段话描述此技能做什么，并明确列举触发条件。
  当用户提出以下需求时触发：
  (1) TODO 触发条件1；
  (2) TODO 触发条件2；
  (3) TODO 触发条件3。
---

# {skill_title}

TODO: 简要说明此技能的核心能力（1-3句）。

## 标准工作流

TODO: 描述 AI 执行此技能的主要步骤。

## IO 声明

### 输入
- param1: str    # 必填，说明
- param2: int    # 可选，默认值，说明

### 输出
- 成功：TODO 格式描述
- 失败：TODO 错误类型 + 说明

### 验证清单
- [ ] TODO 验证项1
- [ ] TODO 验证项2

## 参考资源

TODO: 如有子资源文件，在此引用：
- **功能A详情**：见 [references/feature-a.md](references/feature-a.md)
- **错误处理指南**：见 [references/error-handling.md](references/error-handling.md)
"""

SCRIPT_EXAMPLE = """\
#!/usr/bin/env python3
\"\"\"
example_script.py — 示例脚本（请根据实际需要修改或删除）

用法：
    python scripts/example_script.py <input> [--output <output>]

输入：
    input  : 输入文件路径（必填）
    output : 输出文件路径（可选，默认在输入目录下生成）

输出：
    成功：打印输出文件路径，退出码 0
    失败：打印错误信息到 stderr，退出码 1
\"\"\"

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="示例脚本")
    parser.add_argument("input", help="输入文件路径")
    parser.add_argument("--output", help="输出文件路径（可选）")
    args = parser.parse_args()

    input_path = Path(args.input)

    # 1. 验证输入
    if not input_path.exists():
        print(f"错误：文件不存在 — {input_path}", file=sys.stderr)
        sys.exit(1)

    # 2. 确定输出路径
    output_path = Path(args.output) if args.output else input_path.parent / f"{input_path.stem}_output{input_path.suffix}"

    # 3. TODO: 执行核心逻辑
    # result = do_something(input_path)
    # output_path.write_text(result)

    # 4. 验证输出
    # if not output_path.exists() or output_path.stat().st_size == 0:
    #     print("错误：输出文件生成失败", file=sys.stderr)
    #     sys.exit(1)

    print(f"成功：{output_path}")


if __name__ == "__main__":
    main()
"""

REFERENCE_EXAMPLE = """\
# 参考文档示例

TODO: 将此文件替换为实际的参考文档内容，或直接删除。

参考文档的用途：
- API 文档、数据库 Schema
- 领域知识、业务规则
- 详细的工作流说明（不适合放在 SKILL.md 中的长内容）

## 目录（文件超过100行时建议添加）

- [章节 1](#章节-1)
- [章节 2](#章节-2)

## 章节 1

TODO: 内容

## 章节 2

TODO: 内容
"""


def create_skill_structure(skill_name: str, output_path: Path):
    skill_dir = output_path / skill_name
    
    # 防止覆盖已有目录
    if skill_dir.exists():
        print(f"错误：目录已存在 — {skill_dir}", file=sys.stderr)
        print("请删除后重试，或选择其他输出路径。", file=sys.stderr)
        sys.exit(1)
    
    # 创建目录结构
    dirs = [
        skill_dir,
        skill_dir / "scripts",
        skill_dir / "references",
        skill_dir / "assets",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    
    # 生成 SKILL.md
    skill_title = skill_name.replace("-", " ").title()
    (skill_dir / "SKILL.md").write_text(
        SKILL_MD_TEMPLATE.format(skill_name=skill_name, skill_title=skill_title),
        encoding="utf-8"
    )
    
    # 生成示例脚本
    (skill_dir / "scripts" / "example_script.py").write_text(SCRIPT_EXAMPLE, encoding="utf-8")
    
    # 生成示例参考文档
    (skill_dir / "references" / "example_reference.md").write_text(REFERENCE_EXAMPLE, encoding="utf-8")
    
    # assets 目录留空（放一个 .gitkeep）
    (skill_dir / "assets" / ".gitkeep").write_text("", encoding="utf-8")
    
    print(f"✅ 技能包骨架已生成：{skill_dir}")
    print()
    print("📁 目录结构：")
    for item in sorted(skill_dir.rglob("*")):
        if item.name.startswith("."):
            continue
        indent = "  " * (len(item.relative_to(skill_dir).parts) - 1)
        print(f"  {indent}{'📄' if item.is_file() else '📁'} {item.name}")
    print()
    print("📝 下一步：")
    print(f"  1. 编辑 {skill_dir}/SKILL.md，填写 TODO 项")
    print(f"  2. 在 scripts/ 中实现实际脚本（替换或删除示例）")
    print(f"  3. 在 references/ 中添加参考文档（替换或删除示例）")
    print(f"  4. 完成后运行：python scripts/package_skill.py {skill_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="初始化 AI 技能包目录结构",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            示例：
              python scripts/init_skill.py pdf-editor --path ./skills
              python scripts/init_skill.py data-analysis --path ~/my-skills
        """)
    )
    parser.add_argument("skill_name", help="技能包名称（小写，用连字符分隔）")
    parser.add_argument("--path", default=".", help="输出目录（默认当前目录）")
    args = parser.parse_args()
    
    # 验证技能包名称格式
    import re
    if not re.match(r'^[a-z][a-z0-9-]*$', args.skill_name):
        print(f"错误：技能包名称须为小写字母、数字、连字符，且以字母开头", file=sys.stderr)
        print(f"  示例：pdf-editor, data-analysis, operations-mgmt", file=sys.stderr)
        sys.exit(1)
    
    output_path = Path(args.path).expanduser().resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    
    create_skill_structure(args.skill_name, output_path)


if __name__ == "__main__":
    main()
