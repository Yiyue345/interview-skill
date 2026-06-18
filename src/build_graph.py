"""从 fundamentals.md 自动构建 knowledge-graph.json

信号源（按优先级）:
  1. 已有手工边 — 完全保留（更精确的 subtopic→subtopic 映射）
  2. `关联: XXX` 注释 — 子话题级别的跨栈关联
  3. 跨标签题目 — 同一题标记多个技术栈，暗示关联

用法:
  python build_graph.py
      [--kb ../../knowledge-base/fundamentals.md]
      [--index ../../data/index.json]
      [--existing ../../data/knowledge-graph.json]
      [--output ../../data/knowledge-graph.json]

"""

import re, json, sys
from pathlib import Path
from collections import defaultdict

# ── 配置 ──────────────────────────────────────────────────────────────────
# 向上搜索项目根目录（含 知识库/ 的上级目录）
_BASE = Path(__file__).resolve().parent
for _ in range(6):
    if (_BASE / "knowledge-base").is_dir():
        break
    _BASE = _BASE.parent
BASE = _BASE
DEFAULT_KB = BASE / "knowledge-base/fundamentals.md"
DEFAULT_INDEX = BASE / "data/index.json"
DEFAULT_EXISTING = BASE / "data/knowledge-graph.json"
DEFAULT_OUTPUT = BASE / "data/knowledge-graph.json"

VALID_STACKS = {
    "C++", "C#", "Lua", "Unity", "Graphics", "Algorithms",
    "Networking", "DesignPatterns", "GameDesign", "Performance",
}

# 栈 → 中文名映射（用于 auto-label）
STACK_LABELS = {
    "C++": "C++", "C#": "C#", "Lua": "Lua", "Unity": "Unity",
    "Graphics": "图形学", "Algorithms": "算法",
    "Networking": "网络", "DesignPatterns": "设计模式",
    "GameDesign": "游戏设计", "Performance": "性能优化",
}


# ── 信号源 1：解析 `关联:` 注释 ────────────────────────────────────────

def parse_kb_cross_refs(kb_path: Path) -> list[dict]:
    """从 markdown `关联:` 行提取跨栈边候选

    格式:
      ## C++
      ### 多态
      关联: C# · Unity

    返回: [{"from": "C++:多态", "to": "C#", "label": "跨栈: C#", "weight": 0.6}, ...]
    """
    edges = []
    current_stack = ""
    current_subtopic = ""
    # 用于去重 (from, to) 对
    seen = set()

    for line in kb_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()

        # 技术栈标题: ## C++
        m = re.match(r"^##\s+(\S+)", stripped)
        if m and m.group(1) in VALID_STACKS:
            current_stack = m.group(1)
            current_subtopic = ""
            continue

        # 子话题标题: ### 多态
        m = re.match(r"^###\s+(.+)", stripped)
        if m:
            current_subtopic = m.group(1).strip()
            continue

        # 关联行: 关联: C# · Unity
        m = re.match(r"^关联:\s*(.+)", stripped)
        if m and current_stack and current_subtopic:
            refs = [r.strip() for r in re.split(r"[·,、]", m.group(1)) if r.strip()]
            for ref in refs:
                if ref in VALID_STACKS:
                    key = (f"{current_stack}:{current_subtopic}", ref)
                    if key not in seen:
                        seen.add(key)
                        edges.append({
                            "from": f"{current_stack}:{current_subtopic}",
                            "to": ref,  # 栈级引用，非 subtopic 级
                            "label": f"跨栈: {STACK_LABELS.get(ref, ref)}",
                            "weight": 0.6,
                            "source": "关联注释",
                        })

    return edges


# ── 信号源 2：跨标签题目 ────────────────────────────────────────────────

def parse_cross_tag_refs(index_path: Path) -> list[dict]:
    """从索引中提取跨标签关联

    当一个问题标记了多个技术栈（如 [C++][C#][advanced]），
    就暗示这些栈之间有关联。

    返回: [{"from": "C++", "to": "C#", "label": "跨标签题", "weight": 0.3}, ...]
    """
    edges = []
    if not index_path.exists():
        return edges

    data = json.loads(index_path.read_text(encoding="utf-8"))
    seen = set()

    for source_name, questions in data.items():
        for q in questions:
            tags = q.get("tags", [])
            # 过滤出技术栈标签（非难度）
            stacks = [t for t in tags if t in VALID_STACKS]
            # 只关心多栈题
            if len(stacks) < 2:
                continue

            subtopic = q.get("subtopic", "")
            from_node = f"{stacks[0]}:{subtopic}" if subtopic else stacks[0]

            for to_stack in stacks[1:]:
                key = (from_node, to_stack)
                if key not in seen:
                    seen.add(key)
                    edges.append({
                        "from": from_node,
                        "to": to_stack,
                        "label": f"跨标签: {q.get('text', '')[:20]}",
                        "weight": 0.3,
                        "source": "跨标签题",
                    })

    return edges


# ── 合并 ──────────────────────────────────────────────────────────────────

def load_existing(graph_path: Path) -> list[dict]:
    """加载已有手工边"""
    if not graph_path.exists():
        return []
    data = json.loads(graph_path.read_text(encoding="utf-8"))
    return data.get("edges", [])


def merge_edges(
    auto_edges: list[dict],
    cross_edges: list[dict],
    manual_edges: list[dict],
) -> list[dict]:
    """合并三路信号源

    优先级: manual > 关联注释 > 跨标签
    同 (from, to) 对：manual 覆盖 auto，关联注释覆盖跨标签
    """
    # 手工边的 (from, to) 集合
    manual_keys = {(e["from"], e["to"]) for e in manual_edges}

    # 自动边去重 + 过滤掉手工边已覆盖的
    auto_by_key: dict[tuple[str, str], dict] = {}
    for e in auto_edges + cross_edges:
        key = (e["from"], e["to"])
        if key in manual_keys:
            continue
        # 关联注释比跨标签优先级高
        if key in auto_by_key:
            existing_source = auto_by_key[key].get("source", "")
            if e.get("source", "") == "关联注释" and "跨标签" in existing_source:
                auto_by_key[key] = e
        else:
            auto_by_key[key] = e

    merged = manual_edges + list(auto_by_key.values())
    # 按 from → to → weight 降序排列
    merged.sort(key=lambda e: (e["from"], e["to"], -e.get("weight", 0)))
    return merged


# ── CLI ───────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="自动构建知识图谱")
    parser.add_argument("--kb", default=str(DEFAULT_KB))
    parser.add_argument("--index", default=str(DEFAULT_INDEX))
    parser.add_argument("--existing", default=str(DEFAULT_EXISTING))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--verbose", action="store_true", help="打印统计信息")
    args = parser.parse_args()

    kb_path = Path(args.kb)
    index_path = Path(args.index)
    existing_path = Path(args.existing)
    output_path = Path(args.output)

    # 1. 解析 `关联:` 注释
    auto_edges = parse_kb_cross_refs(kb_path)
    if args.verbose:
        print(f"  关联注释边: {len(auto_edges)}")

    # 2. 解析跨标签题
    cross_edges = parse_cross_tag_refs(index_path)
    if args.verbose:
        print(f"  跨标签边: {len(cross_edges)}")

    # 3. 加载已有手工边
    manual_edges = load_existing(existing_path)
    if args.verbose:
        print(f"  已有手工边: {len(manual_edges)}")

    # 4. 合并
    merged = merge_edges(auto_edges, cross_edges, manual_edges)
    if args.verbose:
        print(f"  合并后总边: {len(merged)}")
        added = len(merged) - len(manual_edges)
        print(f"  新增边: {added}")

    # 5. 输出
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps({"edges": merged}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"知识图谱已生成: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
