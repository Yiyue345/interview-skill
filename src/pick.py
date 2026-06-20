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

from difficulty import (
    apply_tag_difficulty_cap,
    choose_difficulty,
    resolve_difficulty_context,
)
from profiles import detect_profile_from_file, load_profiles, resolve_resume_path
from project_paths import (
    DEFAULT_RESUME,
    GRAPH_FILE,
    INDEX_FILE,
    PROFILE_CONFIG,
    QUESTION_HISTORY_FILE,
    SESSION_STATE_DIR,
)
from state import load_state, record_question, save_state, session_path


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


def load_graph_edges(graph_file: Path = GRAPH_FILE) -> List[Dict[str, Any]]:
    try:
        data = json.loads(Path(graph_file).read_text(encoding="utf-8"))
        return data.get("edges", []) if isinstance(data.get("edges", []), list) else []
    except (OSError, ValueError):
        print("警告：知识图谱无法读取，将退化为普通抽题。", file=sys.stderr)
        return []


def graph_targets(
    start: str,
    edges: List[Dict[str, Any]],
    valid_tags: Set[str],
    max_depth: int = 1,
) -> List[Dict[str, Any]]:
    """按路径权重返回可用于题库筛选的相邻知识点。"""
    adjacency = {}
    for edge in edges:
        adjacency.setdefault(edge.get("from", ""), []).append(edge)
    frontier = [(start, 1.0, [])]
    best = {}
    for depth in range(1, max(max_depth, 1) + 1):
        next_frontier = []
        for node, path_weight, route in frontier:
            for edge in adjacency.get(node, []):
                target = edge.get("to", "")
                tag = target.split(":", 1)[0]
                if not target or tag not in valid_tags or target in route or target == start:
                    continue
                weight = path_weight * float(edge.get("weight", 0.5))
                candidate = {
                    "node": target,
                    "tag": tag,
                    "subtopic": target.split(":", 1)[1] if ":" in target else "",
                    "weight": weight,
                    "depth": depth,
                    "route": route + [target],
                }
                if weight > best.get(target, {}).get("weight", -1):
                    best[target] = candidate
                next_frontier.append((target, weight, route + [target]))
        frontier = next_frontier
    return sorted(best.values(), key=lambda item: (-item["weight"], item["node"]))


def pick_graph_question(
    questions: List[Dict[str, Any]],
    profile_id: str,
    profile: Dict[str, Any],
    level: str,
    asked: Set[int],
    profile_history: Dict[str, Any],
    rng: random.Random,
    start: str,
    edges: List[Dict[str, Any]],
    max_depth: int,
) -> Optional[Dict[str, Any]]:
    targets = graph_targets(start, edges, set(profile.get("tags", [])), max_depth)
    for target in targets:
        target_level = apply_tag_difficulty_cap(
            level, [target["tag"]], profile
        )["level"]
        selected = pick_question(
            questions,
            profile_id,
            profile,
            [target["tag"]],
            target_level,
            asked,
            target["subtopic"],
            False,
            profile_history,
            rng,
        )
        if selected:
            result = dict(selected)
            result["graph"] = {
                "from": start,
                "to": target["node"],
                "depth": target["depth"],
                "path_weight": target["weight"],
                "level": target_level,
            }
            return result
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


def resolve_requested_difficulty(
    config: Dict[str, Any],
    company_size: str,
    position_level: str,
    explicit_level: str,
    rng: random.Random,
) -> Dict[str, Any]:
    if bool(company_size) != bool(position_level):
        return {
            "error": "incomplete_difficulty_context",
            "required": ["company_size", "position_level"],
        }
    if not company_size:
        return {
            "level": explicit_level,
            "source": "explicit" if explicit_level else "unspecified",
        }

    context = resolve_difficulty_context(config, company_size, position_level)
    if context.get("error"):
        return context
    context["level"] = explicit_level or choose_difficulty(context, rng)
    context["source"] = "explicit" if explicit_level else "policy"
    return context


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="多岗位、分级别加权抽题")
    parser.add_argument("--source", choices=["八股", "手撕"], default="八股")
    parser.add_argument("--profile", default="", help="岗位 ID，显式指定时覆盖简历识别")
    parser.add_argument(
        "--resume",
        default="",
        help="用于识别岗位的文本简历路径；省略时自动发现 resumes 下的非模板简历",
    )
    parser.add_argument("--detect-profile", action="store_true", help="仅识别岗位，不抽题")
    parser.add_argument("--tag", default="", help="技术标签，多个用逗号分隔")
    parser.add_argument(
        "--level", default="", choices=["", "basic", "intermediate", "advanced", "Advanced"]
    )
    parser.add_argument(
        "--company-size",
        default="",
        help="目标公司规模，支持 small/medium/large 或小厂/中厂/大厂",
    )
    parser.add_argument(
        "--position-level",
        default="",
        help="应聘岗位等级，支持 intern/full-time 或实习/正职",
    )
    parser.add_argument("--subtopic", default="")
    parser.add_argument("--asked", default="")
    parser.add_argument("--fallback", action="store_true")
    parser.add_argument("--graph-from", default="")
    parser.add_argument("--graph-traverse", action="store_true")
    parser.add_argument("--graph-depth", type=int, choices=[1, 2, 3], default=1)
    parser.add_argument("--graph-file", default=str(GRAPH_FILE))
    parser.add_argument("--session", default="", help="从持久化会话读取并更新面试状态")
    parser.add_argument("--state-dir", default=str(SESSION_STATE_DIR))
    parser.add_argument("--config", default=str(PROFILE_CONFIG))
    parser.add_argument("--index", default=str(INDEX_FILE))
    parser.add_argument("--history-file", default=str(QUESTION_HISTORY_FILE))
    parser.add_argument("--no-history", action="store_true")
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()

    if args.graph_from and not args.graph_traverse:
        edges = [
            edge for edge in load_graph_edges(Path(args.graph_file))
            if edge.get("from") == args.graph_from
        ]
        if edges:
            edges.sort(key=lambda edge: edge.get("weight", 0.5), reverse=True)
        print(json.dumps({"node": args.graph_from, "edges": edges}, ensure_ascii=False))
        return 0

    session_state = None
    session_file = None
    if args.session:
        try:
            session_file = session_path(args.session, Path(args.state_dir))
            session_state = load_state(session_file)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(json.dumps({"error": str(exc), "session": args.session}, ensure_ascii=False))
            return 2
        context_fields = {
            "profile": "profile",
            "company_size": "company_size",
            "position_level": "position_level",
        }
        for argument, state_key in context_fields.items():
            supplied = getattr(args, argument)
            stored = session_state.get(state_key, "")
            if supplied and stored and supplied != stored:
                print(json.dumps({
                    "error": "session_context_mismatch",
                    "field": argument,
                    "expected": stored,
                    "actual": supplied,
                }, ensure_ascii=False))
                return 2
            if not supplied:
                setattr(args, argument, stored)

    config = load_profiles(Path(args.config))
    resume_info = {}
    resume_path = DEFAULT_RESUME
    if args.detect_profile or not args.profile:
        resume_info = resolve_resume_path(args.resume)
        if resume_info.get("error") or resume_info.get("needs_resume"):
            print(json.dumps(resume_info, ensure_ascii=False))
            return 2
        resume_path = Path(resume_info["resume"])

    resolution = resolve_profile(args.profile, resume_path, config)
    if resume_info:
        resolution["resume"] = resume_info["resume"]
        resolution["resume_source"] = resume_info["resume_source"]
    if args.detect_profile:
        print(json.dumps(resolution, ensure_ascii=False))
        return 2 if resolution.get("error") else 0
    if "profile" not in resolution or resolution.get("error"):
        print(json.dumps(resolution, ensure_ascii=False))
        return 2

    profile_id = resolution["profile"]
    profile = config["profiles"][profile_id]
    rng = random.Random(args.seed)
    difficulty = resolve_requested_difficulty(
        config,
        args.company_size,
        args.position_level,
        args.level.lower() if args.level else "",
        rng,
    )
    if difficulty.get("error"):
        print(json.dumps(difficulty, ensure_ascii=False))
        return 2

    tags = [tag.strip() for tag in args.tag.split(",") if tag.strip()]
    difficulty.update(apply_tag_difficulty_cap(difficulty["level"], tags, profile))
    history_path = Path(args.history_file)
    history = {"schema_version": 1, "profiles": {}} if args.no_history else load_history(history_path)
    profile_history = history.get("profiles", {}).get(profile_id, {})
    questions = load_index(args.source, Path(args.index))
    asked = parse_asked(args.asked)
    if session_state:
        asked_qids = set(session_state.get("asked_qids", []))
        questions = [question for question in questions if question.get("qid") not in asked_qids]
    question = None
    if args.graph_traverse:
        if not args.graph_from:
            print(json.dumps({"error": "graph_from_required"}, ensure_ascii=False))
            return 2
        question = pick_graph_question(
            questions,
            profile_id,
            profile,
            difficulty["level"],
            asked,
            profile_history,
            rng,
            args.graph_from,
            load_graph_edges(Path(args.graph_file)),
            args.graph_depth,
        )
    if not question and (not args.graph_traverse or args.fallback):
        question = pick_question(
            questions,
            profile_id,
            profile,
            tags,
            difficulty["level"],
            asked,
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
    if result.get("graph"):
        difficulty.update(apply_tag_difficulty_cap(
            difficulty["level"], [result["graph"]["to"].split(":", 1)[0]], profile
        ))
    result["difficulty"] = difficulty
    if session_state and session_file:
        record_question(session_state, question)
        save_state(session_file, session_state)
        result["session"] = args.session
    if not args.no_history:
        record_exposure(history, profile_id, question)
        save_history(history_path, history)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
