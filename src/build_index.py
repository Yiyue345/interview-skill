"""从岗位配置声明的 Markdown 题库构建统一索引。"""

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from profiles import load_profiles
from project_paths import INDEX_FILE, PROFILE_CONFIG, PROJECT_ROOT


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip().lower()


def make_qid(source: str, stack: str, subtopic: str, text: str) -> str:
    raw = "|".join(
        (source, normalize_text(stack), normalize_text(subtopic), normalize_text(text))
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def parse_fundamentals(file_path: Path, profile_id: str) -> List[Dict[str, Any]]:
    questions = []
    current_stack = ""
    current_subtopic = ""
    for line in file_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(">") or stripped.startswith("# "):
            continue
        if stripped.startswith("## ") and not stripped.startswith("### "):
            current_stack = stripped[3:].strip()
            current_subtopic = ""
            continue
        if stripped.startswith("### "):
            current_subtopic = stripped[4:].strip()
            continue
        match = re.match(r"^-\s+(\[[^\]]+\](?:\[[^\]]+\])*)\s*(.*)", stripped)
        if not match:
            continue
        text = match.group(2).strip()
        if not text:
            continue
        tags = re.findall(r"\[([^\]]+)\]", match.group(1))
        questions.append({
            "qid": make_qid("八股", current_stack, current_subtopic, text),
            "tags": tags,
            "subtopic": current_subtopic,
            "text": text,
            "profiles": [profile_id],
        })
    return questions


def parse_challenges(file_path: Path, profile_id: str) -> List[Dict[str, Any]]:
    questions = []
    for line in file_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(">") or stripped.startswith("#"):
            continue
        match = re.match(r"^\d+\.\s*(\[[^\]]+\](?:\[[^\]]+\])*)?\s*(.*)", stripped)
        if not match:
            continue
        text = match.group(2).strip()
        if not text:
            continue
        tags = re.findall(r"\[([^\]]+)\]", match.group(1) or "")
        questions.append({
            "qid": make_qid("手撕", ",".join(tags), "", text),
            "tags": tags,
            "subtopic": "",
            "text": text,
            "profiles": [profile_id],
        })
    return questions


def _merge_questions(groups: Iterable[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    merged = {}
    order = []
    for questions in groups:
        for question in questions:
            qid = question["qid"]
            if qid not in merged:
                merged[qid] = question
                order.append(qid)
            else:
                existing = merged[qid]
                existing["profiles"] = sorted(set(existing["profiles"] + question["profiles"]))
                existing["tags"] = list(dict.fromkeys(existing["tags"] + question["tags"]))

    result = []
    for number, qid in enumerate(order, start=1):
        question = dict(merged[qid])
        question["id"] = number
        result.append(question)
    return result


def build_index(config_path: Optional[Path] = None) -> Dict[str, List[Dict[str, Any]]]:
    config = load_profiles(config_path)
    fundamental_groups = []
    challenge_groups = []
    for profile_id, profile in config["profiles"].items():
        for relative_path in profile.get("fundamentals", []):
            fundamental_groups.append(parse_fundamentals(PROJECT_ROOT / relative_path, profile_id))
        for relative_path in profile.get("coding_challenges", []):
            challenge_groups.append(parse_challenges(PROJECT_ROOT / relative_path, profile_id))
    return {
        "八股": _merge_questions(fundamental_groups),
        "手撕": _merge_questions(challenge_groups),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="构建多岗位面试题索引")
    parser.add_argument("--config", default=str(PROFILE_CONFIG))
    parser.add_argument("--output", default=str(INDEX_FILE))
    args = parser.parse_args()

    index = build_index(Path(args.config))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print("索引已生成: {}".format(output))
    print("  八股题库: {} 题".format(len(index["八股"])))
    print("  手撕题库: {} 题".format(len(index["手撕"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
