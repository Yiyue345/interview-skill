---
name: build-knowledge
description: 知识库一键构建工具。当用户说「重建索引」「更新知识图谱」「重新构建」「索引过期了」「图谱要更新」「跑一遍构建」等涉及知识库数据构建的场景时使用。
---

## 启动

```powershell
.\Build-Knowledge.ps1
```

可选参数：
- `-Quick` — 跳过校验（日常推荐）
- `-GraphOnly` — 仅构建知识图谱
- `-IndexOnly` — 仅构建索引

## 步骤

| # | 脚本 | 输出 |
|---|------|------|
| 1 | `src/build_index.py` | `data/index.json` |
| 2 | `src/build_graph.py` | `data/knowledge-graph.json` |
| 3 | `src/validate_consistency.py` | 校验 CLAUDE.md ↔ interview.md |

## 触发时机

- 修改了 `knowledge-base/fundamentals.md`、`knowledge-base/coding-challenges.md`、`关联:` 注释之后
- 首次 clone / 迁移后
- 面试前确保数据最新

无需重建：只改 `resumes/`、`records/`、`weak-areas.md` 等非题库文件时。面试中 `pick.py` 实时读 `data/index.json`，索引未变不重建。
