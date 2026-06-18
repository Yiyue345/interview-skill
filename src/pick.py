"""随机选题脚本 — 从索引中按标签/子话题/难度筛选后随机抽取"""
import json, random, sys, argparse
from pathlib import Path

BASE = Path(__file__).parent.parent / "data"
INDEX_FILE = BASE / "index.json"

# 相近领域映射（fallback 时使用）
APPROXIMATE = {
    "Unity": {"Performance"},
    "Performance": {"Unity"},
    "Graphics": {"Unity"},
    "GameDesign": {"Unity"},
}

DIFFICULTY_ORDER = ["advanced", "intermediate", "basic"]


def load_index(source: str) -> list[dict]:
    data = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    return data.get(source, [])


def parse_asked(raw: str) -> set[int]:
    """解析 --asked 参数："1,2,5-10" → {1,2,5,6,7,8,9,10}"""
    asked = set()
    if not raw:
        return asked
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            try:
                asked.update(range(int(a.strip()), int(b.strip()) + 1))
            except ValueError:
                continue
        else:
            try:
                asked.add(int(part))
            except ValueError:
                continue
    return asked


def filter_candidates(
    questions: list[dict], tags: list[str], level: str,
    asked: set[int], subtopic: str = "",
) -> list[dict]:
    """按标签、难度、已问、子话题过滤候选"""
    level_lower = level.lower() if level else ""
    def match(q: dict) -> bool:
        if q["id"] in asked:
            return False
        q_tags = q.get("tags", [])
        q_tag_set = set(q_tags)
        # 技术栈标签（只要匹配一个）
        has_tag = any(t in q_tag_set for t in tags) if tags else True
        # 难度（空字符串表示不限难度），大小写不敏感
        has_level = True
        if level_lower:
            has_level = any(t.lower() == level_lower for t in q_tags)
        # 子话题精确匹配
        if subtopic and q.get("subtopic", "") != subtopic:
            return False
        return has_tag and has_level
    return [q for q in questions if match(q)]


def pick(questions: list[dict], tags: list[str], level: str,
         asked: set[int], subtopic: str = "",
         fallback: bool = False) -> dict | None:
    """核心选题逻辑，fallback=True 时自动降级"""
    candidates = filter_candidates(questions, tags, level, asked, subtopic)
    if candidates:
        return random.choice(candidates)

    if not fallback:
        return None

    # Fallback 1: 降难度
    if level:
        current_idx = DIFFICULTY_ORDER.index(level) if level in DIFFICULTY_ORDER else -1
        for lower_level in DIFFICULTY_ORDER[current_idx + 1:]:
            candidates = filter_candidates(questions, tags, lower_level, asked, subtopic)
            if candidates:
                return random.choice(candidates)

    # Fallback 2: 扩展到相近领域
    expanded_tags = set(tags)
    for t in tags:
        expanded_tags.update(APPROXIMATE.get(t, set()))
    if expanded_tags != set(tags):
        candidates = filter_candidates(questions, list(expanded_tags), level, asked, subtopic)
        if candidates:
            return random.choice(candidates)

        # Fallback 2.5: 相近领域 + 降难度
        if level:
            for lower_level in DIFFICULTY_ORDER[current_idx + 1:]:
                candidates = filter_candidates(
                    questions, list(expanded_tags), lower_level, asked, subtopic)
                if candidates:
                    return random.choice(candidates)

    # Fallback 3: 完全去掉子话题限制（仅当指定了 --subtopic 时）
    if subtopic:
        candidates = filter_candidates(questions, tags, level, asked, subtopic="")
        if candidates:
            return random.choice(candidates)

    # Fallback 4: 不限制技术栈
    candidates = filter_candidates(questions, [], level, asked, subtopic)
    if candidates:
        return random.choice(candidates)

    # Fallback 5: 不限技术栈 + 不限难度 + 不限子话题
    return random.choice(questions) if questions else None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="随机选题")
    parser.add_argument("--source", choices=["八股", "手撕"], default="八股",
                        help="题库：八股 | 手撕")
    parser.add_argument("--tag", default="",
                        help="技术栈标签，多个用逗号分隔，如 C++,Unity")
    parser.add_argument("--level", default="", choices=["", "basic", "intermediate", "advanced", "Advanced"],
                        help="难度：basic / intermediate / advanced，留空不限")
    parser.add_argument("--subtopic", default="",
                        help="子话题精确匹配，如 '多态'，留空不限")
    parser.add_argument("--asked", default="",
                        help="已问题号，如 '1,3,5-10'")
    parser.add_argument("--fallback", action="store_true",
                        help="候选为空时自动降级")
    parser.add_argument("--graph-from", default="",
                        help="查询节点的出边，如 C#:GC与内存管理")
    args = parser.parse_args()

    # --graph-from: 查询节点的出边，返回后立即退出
    if args.graph_from:
        graph_file = BASE / "knowledge-graph.json"
        if graph_file.exists():
            graph = json.loads(graph_file.read_text(encoding="utf-8"))
            edges = [e for e in graph.get("edges", []) if e.get("from") == args.graph_from]
            edges.sort(key=lambda e: e.get("weight", 0.5), reverse=True)
        else:
            edges = []
        print(json.dumps({"node": args.graph_from, "edges": edges}, ensure_ascii=False))
        return

    tags = [t.strip() for t in args.tag.split(",") if t.strip()]
    asked = parse_asked(args.asked)
    level = args.level.lower() if args.level else ""
    questions = load_index(args.source)

    result = pick(questions, tags, level, asked,
                  subtopic=args.subtopic, fallback=args.fallback)
    if result:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(json.dumps({"empty": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
