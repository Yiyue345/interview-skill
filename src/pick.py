"""按岗位、标签、难度和历史曝光权重抽取面试题。"""

import argparse
import json
import os
import random
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from profiles import detect_profile_from_file, load_profiles
from project_paths import (
    DEFAULT_RESUME,
    GRAPH_FILE,
    INDEX_FILE,
    PROFILE_CONFIG,
    QUESTION_HISTORY_FILE,
)


DIFFICULTY_ORDER = ["advanced", "intermediate", "basic"]


def load_index(source: str, index_file: Path = INDEX_FILE) -> List[Dict[str, Any]]:
    data = json.loads(Path(index_file).read_text(encoding="utf-8"))
    return data.get(source, [])


def parse_asked(raw: str) -> Set[int]:
    asked = set()
    if not raw:
        return asked
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            try:
                asked.update(range(int(start.strip()), int(end.strip()) + 1))
            except ValueError:
                continue
        else:
            try:
                asked.add(int(part))
            except ValueError:
                continue
    return asked


def filter_candidates(
    questions: List[Dict[str, Any]],
    profile_id: str,
    tags: List[str],
    level: str,
    asked: Set[int],
    subtopic: str = "",
) -> List[Dict[str, Any]]:
    level_lower = level.lower() if level else ""
    result = []
    for question in questions:
        if profile_id not in question.get("profiles", []):
            continue
        if question.get("id") in asked:
            continue
        question_tags = set(question.get("tags", []))
        if tags and not any(tag in question_tags for tag in tags):
            continue
        if level_lower and not any(tag.lower() == level_lower for tag in question_tags):
            continue
        if subtopic and question.get("subtopic", "") != subtopic:
            continue
        result.append(question)
    return result


def load_history(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"schema_version": 1, "profiles": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema_version") != 1 or not isinstance(data.get("profiles"), dict):
            raise ValueError("schema mismatch")
        return data
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print("Warning: 抽题历史无法读取，将忽略历史: {}".format(exc), file=sys.stderr)
        return {"schema_version": 1, "profiles": {}}


def question_weight(entry: Optional[Dict[str, Any]], now: Optional[float] = None) -> float:
    if not entry:
        return 1.5
    current_time = time.time() if now is None else now
    count = max(int(entry.get("count", 0)), 0)
    age = max(current_time - float(entry.get("last_asked", 0)), 0)
    if age < 24 * 60 * 60:
        recency = 0.1
    elif age < 7 * 24 * 60 * 60:
        recency = 0.35
    elif age < 30 * 24 * 60 * 60:
        recency = 0.7
    else:
        recency = 1.0
    return (1.0 / (1 + count)) * recency


def weighted_choice(
    candidates: List[Dict[str, Any]],
    profile_history: Dict[str, Any],
    rng: random.Random,
    now: Optional[float] = None,
) -> Optional[Dict[str, Any]]:
    if not candidates:
        return None
    weights = [question_weight(profile_history.get(item["qid"]), now) for item in candidates]
    return rng.choices(candidates, weights=weights, k=1)[0]


def save_history(path: Path, history: Dict[str, Any]) -> bool:
    temporary_path = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=str(path.parent), delete=False, suffix=".tmp"
        ) as temporary:
            temporary_path = Path(temporary.name)
            json.dump(history, temporary, ensure_ascii=False, indent=2)
        os.replace(str(temporary_path), str(path))
        return True
    except OSError as exc:
        print("Warning: 抽题历史无法写入，本次结果仍然有效: {}".format(exc), file=sys.stderr)
        if temporary_path and temporary_path.exists():
            try:
                temporary_path.unlink()
            except OSError:
                pass
        return False


def record_exposure(
    history: Dict[str, Any], profile_id: str, question: Dict[str, Any], now: Optional[float] = None
) -> None:
    timestamp = time.time() if now is None else now
    profile_history = history.setdefault("profiles", {}).setdefault(profile_id, {})
    entry = profile_history.setdefault(question["qid"], {"count": 0, "last_asked": 0})
    entry["count"] = int(entry.get("count", 0)) + 1
    entry["last_asked"] = timestamp


def _levels_below(level: str) -> List[str]:
    if not level:
        return []
    normalized = level.lower()
    try:
        current = DIFFICULTY_ORDER.index(normalized)
    except ValueError:
        return []
    return DIFFICULTY_ORDER[current + 1:]


def pick_question(
    questions: List[Dict[str, Any]],
    profile_id: str,
    profile: Dict[str, Any],
    tags: List[str],
    level: str,
    asked: Set[int],
    subtopic: str,
    fallback: bool,
    profile_history: Dict[str, Any],
    rng: random.Random,
) -> Optional[Dict[str, Any]]:
    attempts = [(tags, level, subtopic)]
    if fallback:
        for lower_level in _levels_below(level):
            attempts.append((tags, lower_level, subtopic))
        expanded = set(tags)
        related = profile.get("related_tags", {})
        for tag in tags:
            expanded.update(related.get(tag, []))
        if expanded != set(tags):
            attempts.append((sorted(expanded), level, subtopic))
            for lower_level in _levels_below(level):
                attempts.append((sorted(expanded), lower_level, subtopic))
        if subtopic:
            attempts.append((tags, level, ""))
        attempts.append(([], level, ""))
        attempts.append(([], "", ""))

    seen_attempts = set()
    for attempt_tags, attempt_level, attempt_subtopic in attempts:
        key = (tuple(attempt_tags), attempt_level, attempt_subtopic)
        if key in seen_attempts:
            continue
        seen_attempts.add(key)
        candidates = filter_candidates(
            questions, profile_id, attempt_tags, attempt_level, asked, attempt_subtopic
        )
        selected = weighted_choice(candidates, profile_history, rng)
        if selected:
            return selected
    return None


def resolve_profile(
    explicit_profile: str, resume_path: Path, config: Dict[str, Any]
) -> Dict[str, Any]:
    if explicit_profile:
        if explicit_profile not in config["profiles"]:
            return {
                "error": "unknown_profile",
                "profile": explicit_profile,
                "available_profiles": sorted(config["profiles"]),
            }
        return {"profile": explicit_profile}
    return detect_profile_from_file(resume_path, config)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="多岗位加权抽题")
    parser.add_argument("--source", choices=["八股", "手撕"], default="八股")
    parser.add_argument("--profile", default="", help="岗位 ID，显式指定时覆盖简历识别")
    parser.add_argument("--resume", default=str(DEFAULT_RESUME), help="用于识别岗位的简历路径")
    parser.add_argument("--detect-profile", action="store_true", help="仅识别岗位，不抽题")
    parser.add_argument("--tag", default="", help="技术标签，多个用逗号分隔")
    parser.add_argument(
        "--level", default="", choices=["", "basic", "intermediate", "advanced", "Advanced"]
    )
    parser.add_argument("--subtopic", default="")
    parser.add_argument("--asked", default="")
    parser.add_argument("--fallback", action="store_true")
    parser.add_argument("--graph-from", default="")
    parser.add_argument("--config", default=str(PROFILE_CONFIG))
    parser.add_argument("--index", default=str(INDEX_FILE))
    parser.add_argument("--history-file", default=str(QUESTION_HISTORY_FILE))
    parser.add_argument("--no-history", action="store_true")
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()

    if args.graph_from:
        edges = []
        if GRAPH_FILE.exists():
            graph = json.loads(GRAPH_FILE.read_text(encoding="utf-8"))
            edges = [edge for edge in graph.get("edges", []) if edge.get("from") == args.graph_from]
            edges.sort(key=lambda edge: edge.get("weight", 0.5), reverse=True)
        print(json.dumps({"node": args.graph_from, "edges": edges}, ensure_ascii=False))
        return 0

    config = load_profiles(Path(args.config))
    resolution = resolve_profile(args.profile, Path(args.resume), config)
    if args.detect_profile:
        print(json.dumps(resolution, ensure_ascii=False))
        return 2 if resolution.get("error") else 0
    if "profile" not in resolution or resolution.get("error"):
        print(json.dumps(resolution, ensure_ascii=False))
        return 2

    profile_id = resolution["profile"]
    profile = config["profiles"][profile_id]
    history_path = Path(args.history_file)
    history = {"schema_version": 1, "profiles": {}} if args.no_history else load_history(history_path)
    profile_history = history.get("profiles", {}).get(profile_id, {})
    rng = random.Random(args.seed)
    tags = [tag.strip() for tag in args.tag.split(",") if tag.strip()]
    question = pick_question(
        load_index(args.source, Path(args.index)),
        profile_id,
        profile,
        tags,
        args.level.lower() if args.level else "",
        parse_asked(args.asked),
        args.subtopic,
        args.fallback,
        profile_history,
        rng,
    )
    if not question:
        print(json.dumps({"empty": True, "profile": profile_id}, ensure_ascii=False))
        return 0

    result = dict(question)
    result["profile"] = profile_id
    if not args.no_history:
        record_exposure(history, profile_id, question)
        save_history(history_path, history)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
