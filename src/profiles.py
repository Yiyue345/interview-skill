"""岗位配置加载与简历岗位识别。"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from project_paths import PROFILE_CONFIG


def load_profiles(path: Optional[Path] = None) -> Dict[str, Any]:
    config_path = Path(path) if path else PROFILE_CONFIG
    data = json.loads(config_path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("profiles"), dict):
        raise ValueError("岗位配置格式无效")
    return data


def _extract_expected_position(text: str) -> str:
    match = re.search(r"期望岗位(?:\*\*)?\s*[：:]\s*([^\n\r]+)", text, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def _extract_section(text: str, title: str) -> str:
    pattern = r"^##\s*" + re.escape(title) + r"\s*$([\s\S]*?)(?=^##\s|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
    return match.group(1) if match else ""


def _keyword_hits(text: str, keywords: List[str]) -> int:
    lowered = text.lower()
    return sum(1 for keyword in keywords if keyword.lower() in lowered)


def detect_profile(resume_text: str, config: Dict[str, Any]) -> Dict[str, Any]:
    expected_position = _extract_expected_position(resume_text)
    technology_section = _extract_section(resume_text, "技术栈")
    scores = []

    for profile_id, profile in config["profiles"].items():
        keywords = profile.get("resume_keywords", {})
        score = (
            _keyword_hits(expected_position, keywords.get("job_titles", [])) * 3
            + _keyword_hits(technology_section, keywords.get("technologies", [])) * 2
            + _keyword_hits(resume_text, keywords.get("general", []))
        )
        scores.append({
            "id": profile_id,
            "display_name": profile.get("display_name", profile_id),
            "score": score,
        })

    scores.sort(key=lambda item: (-item["score"], item["id"]))
    top_score = scores[0]["score"] if scores else 0
    top_profiles = [item for item in scores if item["score"] == top_score]
    if top_score >= 3 and len(top_profiles) == 1:
        return {"profile": top_profiles[0]["id"], "scores": scores}

    return {
        "needs_profile": True,
        "reason": "no_match" if top_score == 0 else "ambiguous",
        "candidates": scores,
    }


def detect_profile_from_file(path: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        text = ""
    return detect_profile(text, config)
