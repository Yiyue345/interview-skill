"""公司规模与岗位等级对应的面试难度策略。"""

import random
from typing import Any, Dict, List, Optional


DIFFICULTY_LEVELS = ("basic", "intermediate", "advanced")


def _normalize_dimension(
    value: str, definitions: Dict[str, Dict[str, Any]]
) -> Optional[str]:
    normalized = value.strip().lower()
    if not normalized:
        return None
    for item_id, item in definitions.items():
        aliases = [item_id, item.get("display_name", "")]
        aliases.extend(item.get("aliases", []))
        if normalized in {str(alias).strip().lower() for alias in aliases if alias}:
            return item_id
    return None


def resolve_difficulty_context(
    config: Dict[str, Any], company_size: str, position_level: str
) -> Dict[str, Any]:
    policy = config.get("difficulty_policy", {})
    company_sizes = policy.get("company_sizes", {})
    position_levels = policy.get("position_levels", {})
    normalized_company = _normalize_dimension(company_size, company_sizes)
    normalized_position = _normalize_dimension(position_level, position_levels)

    if not normalized_company:
        return {
            "error": "unknown_company_size",
            "company_size": company_size,
            "available_company_sizes": sorted(company_sizes),
        }
    if not normalized_position:
        return {
            "error": "unknown_position_level",
            "position_level": position_level,
            "available_position_levels": sorted(position_levels),
        }

    weights = (
        policy.get("matrix", {})
        .get(normalized_company, {})
        .get(normalized_position, {})
    )
    if not isinstance(weights, dict) or not any(
        float(weights.get(level, 0)) > 0 for level in DIFFICULTY_LEVELS
    ):
        return {
            "error": "missing_difficulty_policy",
            "company_size": normalized_company,
            "position_level": normalized_position,
        }

    return {
        "company_size": normalized_company,
        "company_size_name": company_sizes[normalized_company].get(
            "display_name", normalized_company
        ),
        "position_level": normalized_position,
        "position_level_name": position_levels[normalized_position].get(
            "display_name", normalized_position
        ),
        "weights": {
            level: float(weights.get(level, 0)) for level in DIFFICULTY_LEVELS
        },
    }


def choose_difficulty(context: Dict[str, Any], rng: random.Random) -> str:
    weights = context["weights"]
    return rng.choices(
        list(DIFFICULTY_LEVELS),
        weights=[weights[level] for level in DIFFICULTY_LEVELS],
        k=1,
    )[0]


def apply_tag_difficulty_cap(
    level: str, tags: List[str], profile: Dict[str, Any]
) -> Dict[str, Any]:
    if not level:
        return {"level": level}

    caps = profile.get("tag_difficulty_caps", {})
    applicable = [
        (tag, caps[tag])
        for tag in tags
        if tag in caps and caps[tag] in DIFFICULTY_LEVELS
    ]
    if not applicable:
        return {"level": level}

    capped_by, cap = min(
        applicable, key=lambda item: DIFFICULTY_LEVELS.index(item[1])
    )
    if DIFFICULTY_LEVELS.index(level) <= DIFFICULTY_LEVELS.index(cap):
        return {"level": level}
    return {
        "level": cap,
        "requested_level": level,
        "profile_cap": cap,
        "capped_by": capped_by,
    }
