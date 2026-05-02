#!/usr/bin/env python3
"""
package_skill.py — 技能包打包与校验脚本

用法：
    python scripts/package_skill.py <path/to/skill-folder>
    python scripts/package_skill.py <path/to/skill-folder> ./dist  # 指定输出目录

功能：
    1. 自动校验技能包合规性
    2. 校验通过后打包为 .skill 文件（实为 ZIP 格式）
    3. 校验失败则输出详细错误并退出，不生成包

输出：
    成功：<output-dir>/<skill-name>.skill
    失败：详细错误报告，退出码 1
"""

import argparse
import os
import re
import sys
import zipfile
from pathlib import Path

import yaml  # pip install pyyaml


# ── 校验规则 ─────────────────────────────────────────────────────────────────

def validate_skill(skill_dir: Path) -> list[str]:
    """返回错误列表，空列表表示校验通过。"""
    errors = []

    # 1. 必须存在 SKILL.md
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append("缺少必须文件：SKILL.md")
        return errors  # 无法继续校验

    content = skill_md.read_text(encoding="utf-8")

    # 2. 解析 YAML frontmatter
    if not content.startswith("---"):
        errors.append("SKILL.md 缺少 YAML frontmatter（应以 '---' 开头）")
        return errors

    try:
        parts = content.split("---", 2)
        if len(parts) < 3:
            raise ValueError("frontmatter 格式不完整")
        frontmatter = yaml.safe_load(parts[1])
    except Exception as e:
        errors.append(f"YAML frontmatter 解析失败：{e}")
        return errors

    # 3. 必填字段 name
    if not frontmatter.get("name"):
        errors.append("frontmatter 缺少必填字段：name")
    else:
        name = frontmatter["name"]
        if not re.match(r'^[a-z][a-z0-9-]*$', str(name)):
            errors.append(f"name 格式不合法（须小写字母/数字/连字符，字母开头）：{name}")
        if str(name) != skill_dir.name:
            errors.append(f"name（{name}）与目录名（{skill_dir.name}）不一致")

    # 4. 必填字段 description
    desc = frontmatter.get("description", "")
    if not desc:
        errors.append("frontmatter 缺少必填字段：description")
    else:
        desc_str = str(desc).strip()
        if len(desc_str) < 50:
            errors.append(f"description 过短（当前 {len(desc_str)} 字符，建议 ≥ 50）")
        if "TODO" in desc_str:
            errors.append("description 包含未填写的 TODO 占位符")

    # 5. 不允许的字段
    allowed_fields = {"name", "description"}
    extra_fields = set(frontmatter.keys()) - allowed_fields
    if extra_fields:
        errors.append(f"frontmatter 包含不允许的字段：{extra_fields}（仅允许 name, description）")

    # 6. body 不应为空
    body = parts[2].strip() if len(parts) >= 3 else ""
    if len(body) < 100:
        errors.append("SKILL.md body 内容过少（建议至少 100 字符）")

    # 7. body 中的 TODO 检查
    if "TODO" in body:
        errors.append("SKILL.md body 包含未填写的 TODO 占位符")

    # 8. 引用的资源文件必须存在
    ref_pattern = re.compile(r'\[.*?\]\(((?:references|scripts|assets)/[^\)]+)\)')
    for match in ref_pattern.finditer(body):
        ref_path = skill_dir / match.group(1)
        if not ref_path.exists():
            errors.append(f"引用的资源文件不存在：{match.group(1)}")

    # 9. 禁止的辅助文档
    forbidden_files = ["README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md"]
    for fname in forbidden_files:
        if (skill_dir / fname).exists():
            errors.append(f"不应包含辅助文档：{fname}（技能包只存放 AI 执行所需内容）")

    return errors


# ── 打包逻辑 ─────────────────────────────────────────────────────────────────

def package_skill(skill_dir: Path, output_dir: Path) -> Path:
    """将技能包目录打包为 .skill 文件。"""
    skill_name = skill_dir.name
    output_path = output_dir / f"{skill_name}.skill"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(skill_dir.rglob("*")):
            if file_path.is_file():
                arcname = file_path.relative_to(skill_dir.parent)
                zf.write(file_path, arcname)
    
    return output_path


# ── 主流程 ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="校验并打包 AI 技能包",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例：\n  python scripts/package_skill.py ./my-skill\n  python scripts/package_skill.py ./my-skill ./dist"
    )
    parser.add_argument("skill_path", help="技能包目录路径")
    parser.add_argument("output_dir", nargs="?", default=None, help="输出目录（默认：技能包父目录）")
    args = parser.parse_args()

    skill_dir = Path(args.skill_path).expanduser().resolve()
    if not skill_dir.is_dir():
        print(f"错误：目录不存在 — {skill_dir}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else skill_dir.parent

    print(f"🔍 校验技能包：{skill_dir.name}")
    print()

    errors = validate_skill(skill_dir)

    if errors:
        print("❌ 校验失败，请修复以下问题后重新打包：")
        print()
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        print()
        sys.exit(1)

    print("✅ 校验通过")
    print()

    try:
        output_path = package_skill(skill_dir, output_dir)
        size_kb = output_path.stat().st_size / 1024
        print(f"📦 打包成功：{output_path}")
        print(f"   文件大小：{size_kb:.1f} KB")
        print()
        print("💡 分发方式：将 .skill 文件发送给其他用户，对方双击即可安装。")
    except Exception as e:
        print(f"错误：打包失败 — {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
