"""一致性校验：检查 Codex、Claude Code Skill 与项目路径。"""

import re
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent.parent
AGENTS_MD = BASE / "AGENTS.md"
README_MD = BASE / "README.md"
SKILL_ROOTS = {
    "Codex": BASE / ".agents/skills",
    "Claude Code": BASE / ".claude/skills",
}
SKILL_NAMES = ("build-knowledge", "interview", "interview-prep")

ERRORS = []
WARNINGS = []


def err(msg: str):
    ERRORS.append(msg)
    print(f"  [ERROR] {msg}")


def warn(msg: str):
    WARNINGS.append(msg)
    print(f"  [WARN]  {msg}")


def ok(msg: str):
    print(f"  [OK]    {msg}")


def check_file_exists(path: Path, label: str):
    if path.is_file():
        ok(f"{label} 存在")
    else:
        err(f"{label} 不存在: {path}")


def iter_skill_files():
    for platform, root in SKILL_ROOTS.items():
        for skill_name in SKILL_NAMES:
            yield platform, skill_name, root / skill_name / "SKILL.md"


def check_core_files():
    check_file_exists(AGENTS_MD, "AGENTS.md")
    check_file_exists(README_MD, "README.md")
    for platform, skill_name, path in iter_skill_files():
        check_file_exists(path, f"{platform} {skill_name}/SKILL.md")


def check_directory_structure():
    required_dirs = [
        "src",
        "knowledge-base",
        "data",
        "resumes",
        "records",
        ".agents/skills",
        ".claude/skills",
    ]
    for relative_path in required_dirs:
        path = BASE / relative_path
        if path.is_dir():
            ok(f"目录存在: {relative_path}/")
        else:
            err(f"目录缺失: {relative_path}/")


def check_skill_frontmatter():
    pattern = re.compile(
        r"\A---\s*\n(?=[\s\S]*?^name:\s*\S)(?=[\s\S]*?^description:\s*\S)[\s\S]*?\n---",
        re.MULTILINE,
    )
    for platform, skill_name, path in iter_skill_files():
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if pattern.search(text):
            ok(f"{platform} {skill_name} frontmatter 有效")
        else:
            err(f"{platform} {skill_name} 缺少 name 或 description frontmatter")


def check_command_refs():
    for platform, root in SKILL_ROOTS.items():
        interview_skill = root / "interview/SKILL.md"
        if not interview_skill.is_file():
            continue
        text = interview_skill.read_text(encoding="utf-8")
        refs = re.findall(r"python\s+src/pick\.py", text)
        if refs:
            ok(f"{platform} interview Skill 中有 {len(refs)} 处 src/pick.py 引用")
        else:
            err(f"{platform} interview Skill 中未找到 src/pick.py 引用")


def check_markdown_refs():
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    for platform, skill_name, path in iter_skill_files():
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for link_text, link_path in link_pattern.findall(text):
            if link_path.startswith(("http://", "https://", "#")):
                continue
            target = (path.parent / link_path).resolve()
            if target.exists():
                ok(f"{platform} {skill_name} 引用有效: {link_text} -> {link_path}")
            else:
                err(
                    f"{platform} {skill_name} 引用不存在: "
                    f"{link_text} -> {link_path}"
                )


def check_pick_path():
    pick_py = BASE / "src/pick.py"
    if not pick_py.is_file():
        err("pick.py 不存在")
        return

    text = pick_py.read_text(encoding="utf-8")
    if "parent.parent" in text and "data" in text:
        ok("pick.py 路径解析指向 parent.parent/data/")
    else:
        warn("pick.py 路径解析未使用 parent.parent/data/ 模式，请人工确认")


def check_build_script():
    script = BASE / "Build-Knowledge.ps1"
    if not script.is_file():
        err("Build-Knowledge.ps1 不存在")
        return

    text = script.read_text(encoding="utf-8")
    if "src\\" in text or "src/" in text:
        ok("Build-Knowledge.ps1 使用 src/ 路径")
    else:
        warn("Build-Knowledge.ps1 未使用 src/ 路径，请人工确认")
    if "scripts" in text:
        warn("Build-Knowledge.ps1 包含 scripts/ 引用（应为 src/）")


def main():
    print(f"=== 一致性校验: {BASE} ===\n")

    print("--- 核心文件 ---")
    check_core_files()

    print("\n--- 目录结构 ---")
    check_directory_structure()

    print("\n--- Skill frontmatter ---")
    check_skill_frontmatter()

    print("\n--- 命令引用 ---")
    check_command_refs()

    print("\n--- Skill 交叉引用 ---")
    check_markdown_refs()

    print("\n--- pick.py 路径 ---")
    check_pick_path()

    print("\n--- 构建脚本 ---")
    check_build_script()

    print("\n=== 结果 ===")
    if ERRORS:
        print(f"错误: {len(ERRORS)} 项 - 请修复")
        for message in ERRORS:
            print(f"  {message}")
    else:
        print("无错误")
    if WARNINGS:
        print(f"警告: {len(WARNINGS)} 项 - 建议人工检查")
        for message in WARNINGS:
            print(f"  {message}")
    else:
        print("无警告")

    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
