"""持久化单次面试的流程状态，避免依赖 LLM 上下文维护计数器。"""

import argparse
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, Optional

from project_paths import SESSION_STATE_DIR


SCHEMA_VERSION = 1
SESSION_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
RESULTS = {"accurate", "partial", "incorrect"}


def validate_session_id(session_id: str) -> str:
    if not SESSION_ID_PATTERN.fullmatch(session_id):
        raise ValueError("invalid_session_id")
    return session_id


def session_path(session_id: str, directory: Path = SESSION_STATE_DIR) -> Path:
    validate_session_id(session_id)
    return Path(directory) / (session_id + ".json")


def new_state(
    session_id: str,
    profile: str,
    company_size: str,
    position_level: str,
    now: Optional[float] = None,
) -> Dict[str, Any]:
    timestamp = time.time() if now is None else now
    return {
        "schema_version": SCHEMA_VERSION,
        "session_id": validate_session_id(session_id),
        "profile": profile,
        "company_size": company_size,
        "position_level": position_level,
        "stage": "技术深挖",
        "asked_ids": [],
        "asked_qids": [],
        "covered_areas": [],
        "consecutive_correct": 0,
        "consecutive_wrong": 0,
        "same_subtopic_rounds": 0,
        "last_subtopic": "",
        "evaluations": [],
        "status": "active",
        "created_at": timestamp,
        "updated_at": timestamp,
    }


def load_state(path: Path) -> Dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported_state_schema")
    return data


def save_state(path: Path, state: Dict[str, Any]) -> None:
    path = Path(path)
    temporary_path = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=str(path.parent),
            delete=False,
            suffix=".tmp",
        ) as handle:
            json.dump(state, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            temporary_path = Path(handle.name)
        os.replace(str(temporary_path), str(path))
    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()


def record_question(state: Dict[str, Any], question: Dict[str, Any]) -> None:
    question_id = question.get("id")
    qid = question.get("qid", "")
    if question_id is not None and question_id not in state["asked_ids"]:
        state["asked_ids"].append(question_id)
    if qid and qid not in state["asked_qids"]:
        state["asked_qids"].append(qid)
    for tag in question.get("tags", []):
        if tag.lower() not in {"basic", "intermediate", "advanced"}:
            if tag not in state["covered_areas"]:
                state["covered_areas"].append(tag)
    subtopic = question.get("subtopic", "")
    if subtopic and subtopic == state.get("last_subtopic"):
        state["same_subtopic_rounds"] += 1
    else:
        state["last_subtopic"] = subtopic
        state["same_subtopic_rounds"] = 1 if subtopic else 0
    state["updated_at"] = time.time()


def record_evaluation(
    state: Dict[str, Any], result: str, summary: str = "", now: Optional[float] = None
) -> None:
    if result not in RESULTS:
        raise ValueError("invalid_evaluation_result")
    if result == "accurate":
        state["consecutive_correct"] += 1
        state["consecutive_wrong"] = 0
    elif result == "incorrect":
        state["consecutive_wrong"] += 1
        state["consecutive_correct"] = 0
    else:
        state["consecutive_correct"] = 0
        state["consecutive_wrong"] = 0
    state["evaluations"].append({
        "question_id": state["asked_ids"][-1] if state["asked_ids"] else None,
        "qid": state["asked_qids"][-1] if state["asked_qids"] else "",
        "result": result,
        "summary": summary[:500],
        "timestamp": time.time() if now is None else now,
    })
    state["updated_at"] = time.time() if now is None else now


def print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="面试会话状态管理")
    parser.add_argument("--state-dir", default=str(SESSION_STATE_DIR))
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--session", required=True)
    init_parser.add_argument("--profile", required=True)
    init_parser.add_argument("--company-size", required=True)
    init_parser.add_argument("--position-level", required=True)

    for command in ("show", "complete"):
        command_parser = subparsers.add_parser(command)
        command_parser.add_argument("--session", required=True)

    stage_parser = subparsers.add_parser("set-stage")
    stage_parser.add_argument("--session", required=True)
    stage_parser.add_argument("--stage", required=True)

    evaluate_parser = subparsers.add_parser("evaluate")
    evaluate_parser.add_argument("--session", required=True)
    evaluate_parser.add_argument("--result", required=True, choices=sorted(RESULTS))
    evaluate_parser.add_argument("--summary", default="")

    args = parser.parse_args()
    try:
        path = session_path(args.session, Path(args.state_dir))
        if args.command == "init":
            if path.exists():
                print_json({"error": "session_exists", "session": args.session})
                return 2
            state = new_state(
                args.session, args.profile, args.company_size, args.position_level
            )
            save_state(path, state)
        else:
            state = load_state(path)
            if args.command == "set-stage":
                state["stage"] = args.stage[:100]
                state["updated_at"] = time.time()
                save_state(path, state)
            elif args.command == "evaluate":
                record_evaluation(state, args.result, args.summary)
                save_state(path, state)
            elif args.command == "complete":
                state["status"] = "completed"
                state["updated_at"] = time.time()
                save_state(path, state)
        print_json(state)
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print_json({"error": str(exc), "session": getattr(args, "session", "")})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
