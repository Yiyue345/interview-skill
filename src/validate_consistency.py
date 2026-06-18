"""一致性校验：检查 CLAUDE.md 与 interview.md 之间的引用一致性

校验项：
  1. CLAUDE.md 中引用的 skill 文件路径是否存在
  2. interview.md 中引用的路径是否存在
  3. 两个文件中高频命令（python src/pick.py）的引用一致
  4. skill 描述中的路径引用是否匹配实际目录结构
"""

import re, sys
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────────────────────────
_BASE = Path(__file__).resolve().parent.parent  # interview/
CLAUDE_MD = _BASE / "CLAUDE.md"
INTERVIEW_MD = _BASE / ".claude/skills/interview/interview.md"
INTERVIEW_PREP_MD = _BASE / ".claude/skills/interview-prep/SKILL.md"
README_MD = _BASE / "README.md"

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


# ── 1. 核心文件存在性检查 ────────────────────────────────────────────────

def check_file_exists(path: Path, label: str):
    if path.exists():
        ok(f"{label} 存在")
    else:
        err(f"{label} 不存在: {path}")


# ── 2. 命令引用一致性 ────────────────────────────────────────────────────

def check_command_refs():
    """检查所有 python src/pick.py 引用一致"""
    if not CLAUDE_MD.exists() or not INTERVIEW_MD.exists():
        return

    claude_text = CLAUDE_MD.read_text(encoding="utf-8")
    interview_text = INTERVIEW_MD.read_text(encoding="utf-8")

    # 统计 pick.py 引用
    claude_refs = re.findall(r"python\s+(src/pick\.py)", claude_text)
    interview_refs = re.findall(r"python\s+(src/pick\.py)", interview_text)

    if claude_refs:
        ok(f"CLAUDE.md 中 {len(claude_refs)} 处 src/pick.py 引用")
    else:
        warn("CLAUDE.md 中未找到 src/pick.py 引用")

    if interview_refs:
        ok(f"interview.md 中 {len(interview_refs)} 处 src/pick.py 引用")
    else:
        warn("interview.md 中未找到 src/pick.py 引用")


# ── 3. 交叉引用路径完整性 ────────────────────────────────────────────────

def check_cross_refs():
    """检查 CLAUDE.md 中的引用路径是否可访问"""
    if not CLAUDE_MD.exists():
        return

    text = CLAUDE_MD.read_text(encoding="utf-8")
    # 匹配 markdown 链接: [text](path)
    refs = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)
    for link_text, link_path in refs:
        if link_path.startswith("http"):
            continue
        full = (_BASE / link_path).resolve()
        if full.exists() or full.with_suffix(".md").exists():
            ok(f"引用有效: {link_text} -> {link_path}")
        else:
            warn(f"引用路径不存在: {link_text} -> {link_path} (full: {full})")


# ── 4. 目录结构完整性 ────────────────────────────────────────────────────

def check_directory_structure():
    required_dirs = [
        "src",
        "knowledge-base",
        "data",
        "resumes",
        "records",
        ".claude/skills/interview",
        ".claude/skills/interview-prep",
    ]
    for d in required_dirs:
        path = _BASE / d
        if path.is_dir():
            ok(f"目录存在: {d}/")
        else:
            err(f"目录缺失: {d}/")


# ── 5. Pick.py 路径解析自检 ──────────────────────────────────────────────

def check_pick_path():
    """验证 pick.py 的数据路径解析是否正确指向 data/"""
    pick_py = _BASE / "src/pick.py"
    if not pick_py.exists():
        warn("pick.py 不存在，跳过路径检查")
        return

    # 检查 pick.py 中 BASE 或 DATA_DIR 的路径解析
    text = pick_py.read_text(encoding="utf-8")
    # 检查是否使用 parent.parent / "data"
    if "parent.parent" in text and "data" in text:
        ok("pick.py 路径解析指向 parent.parent/data/")
    else:
        warn("pick.py 路径解析未使用 parent.parent/data/ 模式，请人工确认")


# ── 6. Build-Knowledge.ps1 脚本一致性 ────────────────────────────────────

def check_build_script():
    """验证 Build-Knowledge.ps1 引用 src/ 而不是 scripts/"""
    script = _BASE / "Build-Knowledge.ps1"
    if not script.exists():
        warn("Build-Knowledge.ps1 不存在")
        return

    text = script.read_text(encoding="utf-8")
    if "src\\" in text or "src/" in text:
        ok("Build-Knowledge.ps1 使用 src/ 路径")
    else:
        warn("Build-Knowledge.ps1 未使用 src/ 路径，请人工确认")
    if "scripts" in text:
        warn("Build-Knowledge.ps1 包含 scripts/ 引用（应为 src/）")


# ── 主流程 ────────────────────────────────────────────────────────────────

def main():
    print(f"=== 一致性校验: {_BASE} ===\n")

    # 1. 核心文件
    print("--- 核心文件 ---")
    check_file_exists(CLAUDE_MD, "CLAUDE.md")
    check_file_exists(INTERVIEW_MD, "interview.md")
    check_file_exists(README_MD, "README.md")
    if INTERVIEW_PREP_MD.exists():
        ok("interview-prep/SKILL.md 存在")
    else:
        warn("interview-prep/SKILL.md 不存在")

    # 2. 目录结构
    print("\n--- 目录结构 ---")
    check_directory_structure()

    # 3. 命令引用
    print("\n--- 命令引用 ---")
    check_command_refs()

    # 4. 交叉引用
    print("\n--- 交叉引用 ---")
    check_cross_refs()

    # 5. pick.py 路径
    print("\n--- pick.py 路径 ---")
    check_pick_path()

    # 6. 构建脚本
    print("\n--- 构建脚本 ---")
    check_build_script()

    # 汇总
    print(f"\n=== 结果 ===")
    if ERRORS:
        print(f"错误: {len(ERRORS)} 项 — 请修复")
        for e in ERRORS:
            print(f"  {e}")
    else:
        print("无错误")
    if WARNINGS:
        print(f"警告: {len(WARNINGS)} 项 — 建议人工检查")
        for w in WARNINGS:
            print(f"  {w}")
    else:
        print("无警告")

    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
