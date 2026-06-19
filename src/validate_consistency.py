"""校验岗位配置、题库索引和 Codex/Claude Skill 一致性。"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

from profiles import load_profiles
from project_paths import INDEX_FILE, PROFILE_CONFIG, PROJECT_ROOT


DIFFICULTY_LEVELS = {"basic", "intermediate", "advanced"}
SKILL_ROOTS = {
    "Codex": PROJECT_ROOT / ".agents/skills",
    "Claude Code": PROJECT_ROOT / ".claude/skills",
}
SKILL_NAMES = ("build-knowledge", "interview", "interview-prep")
ERRORS = []
WARNINGS = []


def error(message: str) -> None:
    ERRORS.append(message)
    print("  [ERROR] {}".format(message))


def warning(message: str) -> None:
    WARNINGS.append(message)
    print("  [WARN]  {}".format(message))


def success(message: str) -> None:
    print("  [OK]    {}".format(message))


def iter_skill_files() -> Iterable[Tuple[str, str, Path]]:
    for platform, root in SKILL_ROOTS.items():
        for skill_name in SKILL_NAMES:
            yield platform, skill_name, root / skill_name / "SKILL.md"


def check_core_files() -> None:
    required = [
        PROJECT_ROOT / "AGENTS.md",
        PROJECT_ROOT / "README.md",
        PROFILE_CONFIG,
        INDEX_FILE,
        PROJECT_ROOT / "src/project_paths.py",
        PROJECT_ROOT / "src/profiles.py",
        PROJECT_ROOT / "src/difficulty.py",
    ]
    required.extend(path for _, _, path in iter_skill_files())
    for path in required:
        if path.is_file():
            success("文件存在: {}".format(path.relative_to(PROJECT_ROOT)))
        else:
            error("文件不存在: {}".format(path))


def check_profile_config(config: Dict[str, Any]) -> None:
    policy = config.get("difficulty_policy", {})
    company_sizes = policy.get("company_sizes", {})
    position_levels = policy.get("position_levels", {})
    matrix = policy.get("matrix", {})
    if not company_sizes or not position_levels:
        error("难度策略缺少公司规模或岗位等级配置")
    else:
        for company_size in company_sizes:
            for position_level in position_levels:
                weights = matrix.get(company_size, {}).get(position_level, {})
                if set(weights) != DIFFICULTY_LEVELS or sum(weights.values()) != 100:
                    error(
                        "难度矩阵无效: {} × {}".format(company_size, position_level)
                    )
        if not ERRORS:
            success("公司规模与岗位等级难度矩阵有效")

    required_keys = {
        "display_name", "fundamentals", "coding_challenges", "tags",
        "coverage_order", "related_tags", "evaluation_dimensions", "resume_keywords",
    }
    for profile_id, profile in config["profiles"].items():
        missing = sorted(required_keys - set(profile))
        if missing:
            error("岗位 {} 缺少配置: {}".format(profile_id, ", ".join(missing)))
            continue
        source_files = profile["fundamentals"] + profile["coding_challenges"]
        missing_files = [path for path in source_files if not (PROJECT_ROOT / path).is_file()]
        if missing_files:
            error("岗位 {} 题库不存在: {}".format(profile_id, ", ".join(missing_files)))
        elif not profile["tags"] or not profile["coverage_order"] or not profile["evaluation_dimensions"]:
            error("岗位 {} 的标签、覆盖顺序和评分维度不能为空".format(profile_id))
        else:
            success("岗位配置有效: {}".format(profile_id))


def check_index(config: Dict[str, Any]) -> None:
    try:
        index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        error("索引无法读取: {}".format(exc))
        return
    if set(index) != {"八股", "手撕"}:
        error("索引顶层必须仅包含八股和手撕")
        return
    for source, questions in index.items():
        for question in questions:
            if not question.get("qid") or not question.get("profiles"):
                error("{}题目缺少 qid 或 profiles: {}".format(source, question.get("id")))
                return
    for profile_id in config["profiles"]:
        profile_questions = {
            source: [q for q in questions if profile_id in q.get("profiles", [])]
            for source, questions in index.items()
        }
        fundamentals = len(profile_questions["八股"])
        challenges = len(profile_questions["手撕"])
        if fundamentals < 25 or challenges < 5:
            error("岗位 {} 题量不足: 八股={} 手撕={}".format(profile_id, fundamentals, challenges))
        else:
            success("岗位题量: {} 八股={} 手撕={}".format(profile_id, fundamentals, challenges))
        for source, questions in profile_questions.items():
            levels = {
                tag.lower()
                for question in questions
                for tag in question.get("tags", [])
                if tag.lower() in DIFFICULTY_LEVELS
            }
            if levels != DIFFICULTY_LEVELS:
                error(
                    "岗位 {} 的{}缺少难度级别: {}".format(
                        profile_id, source, ", ".join(sorted(DIFFICULTY_LEVELS - levels))
                    )
                )


def check_skills() -> None:
    frontmatter = re.compile(
        r"\A---\s*\n(?=[\s\S]*?^name:\s*\S)(?=[\s\S]*?^description:\s*\S)[\s\S]*?\n---",
        re.MULTILINE,
    )
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    for platform, skill_name, path in iter_skill_files():
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if not frontmatter.search(text):
            error("{} {} frontmatter 无效".format(platform, skill_name))
        if skill_name == "interview" and "python src/pick.py" not in text:
            error("{} interview 未强制使用 pick.py".format(platform))
        for label, target in link_pattern.findall(text):
            if target.startswith(("http://", "https://", "#")):
                continue
            if not (path.parent / target).resolve().exists():
                error("{} {} 引用不存在: {} -> {}".format(platform, skill_name, label, target))

    for skill_name in SKILL_NAMES:
        codex = SKILL_ROOTS["Codex"] / skill_name / "SKILL.md"
        claude = SKILL_ROOTS["Claude Code"] / skill_name / "SKILL.md"
        if codex.is_file() and claude.is_file() and codex.read_bytes() == claude.read_bytes():
            success("双平台 Skill 同步: {}".format(skill_name))
        else:
            error("双平台 Skill 内容不一致: {}".format(skill_name))


def check_path_architecture() -> None:
    for filename in ("build_index.py", "build_graph.py", "pick.py"):
        text = (PROJECT_ROOT / "src" / filename).read_text(encoding="utf-8")
        if "for _ in range(" in text:
            error("{} 仍包含向上遍历查找根目录".format(filename))
        elif "project_paths" in text:
            success("{} 使用共享路径模块".format(filename))
        else:
            warning("{} 未显式使用共享路径模块".format(filename))


def main() -> int:
    print("=== 一致性校验: {} ===".format(PROJECT_ROOT))
    config = load_profiles(PROFILE_CONFIG)
    check_core_files()
    check_profile_config(config)
    check_index(config)
    check_skills()
    check_path_architecture()
    print("\n=== 结果 ===")
    print("错误: {}，警告: {}".format(len(ERRORS), len(WARNINGS)))
    return 1 if ERRORS else 0


if __name__ == "__main__":
    raise SystemExit(main())
