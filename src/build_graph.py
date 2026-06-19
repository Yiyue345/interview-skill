"""从全部岗位题库构建知识图谱。"""

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

from profiles import load_profiles
from project_paths import GRAPH_FILE, INDEX_FILE, PROFILE_CONFIG, PROJECT_ROOT


def configured_tags(config: Dict[str, Any]) -> Set[str]:
    tags = set()
    for profile in config["profiles"].values():
        tags.update(profile.get("tags", []))
    return tags


def configured_kb_files(config: Dict[str, Any]) -> List[Path]:
    paths = []
    seen = set()
    for profile in config["profiles"].values():
        for relative_path in profile.get("fundamentals", []):
            path = (PROJECT_ROOT / relative_path).resolve()
            if path not in seen:
                seen.add(path)
                paths.append(path)
    return paths


def parse_kb_cross_refs(kb_path: Path, valid_tags: Set[str]) -> List[Dict[str, Any]]:
    edges = []
    current_stack = ""
    current_subtopic = ""
    seen = set()
    for line in kb_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        stack_match = re.match(r"^##\s+(.+)", stripped)
        if stack_match and not stripped.startswith("###"):
            candidate = stack_match.group(1).strip()
            current_stack = candidate if candidate in valid_tags else ""
            current_subtopic = ""
            continue
        subtopic_match = re.match(r"^###\s+(.+)", stripped)
        if subtopic_match:
            current_subtopic = subtopic_match.group(1).strip()
            continue
        ref_match = re.match(r"^关联:\s*(.+)", stripped)
        if not ref_match or not current_stack or not current_subtopic:
            continue
        for reference in re.split(r"[·,、]", ref_match.group(1)):
            target = reference.strip()
            key = ("{}:{}".format(current_stack, current_subtopic), target)
            if target in valid_tags and key not in seen:
                seen.add(key)
                edges.append({
                    "from": key[0],
                    "to": target,
                    "label": "跨栈: {}".format(target),
                    "weight": 0.6,
                    "source": "关联注释",
                })
    return edges


def parse_cross_tag_refs(index_path: Path, valid_tags: Set[str]) -> List[Dict[str, Any]]:
    if not index_path.exists():
        return []
    data = json.loads(index_path.read_text(encoding="utf-8"))
    edges = []
    seen = set()
    for questions in data.values():
        for question in questions:
            stacks = [tag for tag in question.get("tags", []) if tag in valid_tags]
            if len(stacks) < 2:
                continue
            subtopic = question.get("subtopic", "")
            source = "{}:{}".format(stacks[0], subtopic) if subtopic else stacks[0]
            for target in stacks[1:]:
                key = (source, target)
                if key not in seen:
                    seen.add(key)
                    edges.append({
                        "from": source,
                        "to": target,
                        "label": "跨标签: {}".format(question.get("text", "")[:20]),
                        "weight": 0.3,
                        "source": "跨标签题",
                    })
    return edges


def load_existing(graph_path: Path) -> List[Dict[str, Any]]:
    if not graph_path.exists():
        return []
    return json.loads(graph_path.read_text(encoding="utf-8")).get("edges", [])


def merge_edges(auto_edges: Iterable[Dict[str, Any]], manual_edges: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_key = {}
    for edge in auto_edges:
        key = (edge["from"], edge["to"])
        existing = by_key.get(key)
        if not existing or edge.get("weight", 0) > existing.get("weight", 0):
            by_key[key] = edge
    for edge in manual_edges:
        by_key[(edge["from"], edge["to"])] = edge
    result = list(by_key.values())
    result.sort(key=lambda edge: (edge["from"], edge["to"], -edge.get("weight", 0)))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="自动构建多岗位知识图谱")
    parser.add_argument("--config", default=str(PROFILE_CONFIG))
    parser.add_argument("--kb", action="append", help="覆盖配置中的题库文件，可重复指定")
    parser.add_argument("--index", default=str(INDEX_FILE))
    parser.add_argument("--existing", default=str(GRAPH_FILE))
    parser.add_argument("--output", default=str(GRAPH_FILE))
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    config = load_profiles(Path(args.config))
    tags = configured_tags(config)
    kb_files = [Path(path) for path in args.kb] if args.kb else configured_kb_files(config)
    auto_edges = []
    for kb_file in kb_files:
        auto_edges.extend(parse_kb_cross_refs(kb_file, tags))
    auto_edges.extend(parse_cross_tag_refs(Path(args.index), tags))
    existing = load_existing(Path(args.existing))
    merged = merge_edges(auto_edges, existing)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"edges": merged}, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.verbose:
        print("  题库文件: {}".format(len(kb_files)))
        print("  自动边: {}".format(len(auto_edges)))
        print("  合并后总边: {}".format(len(merged)))
    print("知识图谱已生成: {}".format(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
