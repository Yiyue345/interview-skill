"""从 fundamentals.md 和 coding-challenges.md 构建索引 JSON
支持新版分层格式：
  ## 技术栈
  ### 子话题
  - [技术栈][难度] 题目正文
"""
import re, json
from pathlib import Path


def parse_questions_八股(file: Path) -> list[dict]:
    """解析新版分层 markdown，返回题目列表"""
    questions = []
    current_subtopic = ""
    valid_tags = {
        "C++", "C#", "Lua", "Unity", "Graphics", "Algorithms",
        "Networking", "DesignPatterns", "GameDesign", "Performance",
        "basic", "Advanced", "intermediate", "advanced",
    }

    discarded_tags: set[str] = set()

    for line in file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(">") or stripped.startswith("# "):
            continue

        # 技术栈标题: ## C++
        if stripped.startswith("## ") and not stripped.startswith("### "):
            current_subtopic = ""
            continue

        # 子话题标题: ### 多态
        if stripped.startswith("### "):
            current_subtopic = stripped[4:].strip()
            continue

        # 题目行: - [C++][basic] 正文
        m = re.match(r"^-\s+(\[[^\]]+\](?:\[[^\]]+\])*)\s*(.*)", stripped)
        if not m:
            continue
        
        tags_str = m.group(1)
        text = m.group(2).strip()
        found_tags = re.findall(r"\[([^\]]+)\]", tags_str)
        tags = []
        for t in found_tags:
            if t in valid_tags:
                tags.append(t)
            else:
                discarded_tags.add(t)

        if not text:
            continue

        questions.append({
            "id": len(questions) + 1,
            "tags": tags,
            "subtopic": current_subtopic,
            "text": text,
        })

    if discarded_tags:
        print(f"  Warning: {len(discarded_tags)} unknown tag(s) discarded: {sorted(discarded_tags)}")

    return questions


def parse_questions_手撕(file: Path) -> list[dict]:
    """笔试手撕保持原有平铺格式"""
    questions = []
    valid_tags = {
        "C++", "C#", "Unity", "Graphics", "Algorithms",
        "Networking", "DesignPatterns", "GameDesign", "Performance",
    }
    discarded_tags: set[str] = set()

    for line in file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(">") or stripped.startswith("#"):
            continue
        m = re.match(r"^(\d+)\.\s*(\[[^\]]+\](?:\[[^\]]+\])*)?\s*(.*)", stripped)
        if not m:
            continue
        tags_str = m.group(2) or ""
        text = m.group(3).strip()
        if not text:
            continue
        found_tags = re.findall(r"\[([^\]]+)\]", tags_str)
        tags = []
        for t in found_tags:
            if t in valid_tags:
                tags.append(t)
            else:
                discarded_tags.add(t)
        questions.append({
            "id": len(questions) + 1,
            "tags": tags,
            "subtopic": "",
            "text": text,
        })

    if discarded_tags:
        print(f"  Warning: {len(discarded_tags)} unknown tag(s) discarded: {sorted(discarded_tags)}")

    return questions


def build(source_name: str, source_file: Path) -> list[dict]:
    if source_name == "手撕":
        return parse_questions_手撕(source_file)
    return parse_questions_八股(source_file)


if __name__ == "__main__":
    # 向上搜索项目根目录（含 知识库/ 的上级目录）
    root = Path(__file__).resolve()
    for _ in range(6):  # 最多向上 6 层
        if (root / "knowledge-base").is_dir():
            break
        root = root.parent
    index = {
        "八股": build("八股", root / "knowledge-base/fundamentals.md"),
        "手撕": build("手撕", root / "knowledge-base/coding-challenges.md"),
    }

    out = root / "data/index.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"索引已生成: {out}")
    print(f"  八股题库: {len(index['八股'])} 题")
    print(f"  手撕题库: {len(index['手撕'])} 题")
