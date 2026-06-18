# 面试 Skill

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-8A2BE2)](#)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python)](#)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-4A90D9)](#)
[![License](https://img.shields.io/badge/License-MIT-green)](#)

**Unity 客户端面试系统。** 从题库随机抽题，覆盖技术深挖 → 项目深挖 → 手撕代码全流程，自动输出结构化面试总结。
> 实际上可以将知识库,索引,图谱等内容重新转化为相对应的技术栈与学习方向,微调 skill 即可复用

---

## 目录

- [特点](#特点)
- [快速开始](#快速开始)
- [前置条件](#前置条件)
- [使用指南](#使用指南)
  - [模拟面试](#模拟面试)
  - [答题指导](#答题指导)
  - [维护题库](#维护题库)
- [目录结构](#目录结构)
- [流程详解](#流程详解)
  - [面试阶段流转](#面试阶段流转)
  - [自适应难度调整](#自适应难度调整)
  - [弱势追踪](#弱势追踪)
- [自定义你的 Skill](#自定义你的-skill)
- [FAQ](#faq)
- [贡献指南](#贡献指南)
- [许可](#许可)

---

## 特点

- **智能命题** — 从题库按标签、难度、子话题精确筛选，同题不重复
- **自适应调整** — 根据候选人表现动态调整难度和领域覆盖
- **标准化评估** — 概念题 / 原理题 / 设计题 / 编程题各有明确评分标准
- **知识图谱联动** — 知识点间的跨栈关联辅助面试官自然过渡话题
- **自动化归档** — 面试结束自动生成结构化总结，更新弱势技术栈
- **答题指导** — 内置面试准备模式，帮助候选人理解答题思路
- **可定制题库** — 按标签体系自由增删题目，一键重建索引

## 快速开始

```powershell
# 1. 构建题库索引（首次使用必须执行）
.\Build-Knowledge.ps1

# 2. 在 Claude Code 中开始面试
#    输入：开始面试
```

> Claude 会自动加载面试 Skill，以面试官身份开始提问。

### 首次使用 Checklist

- [ ] 运行 `Build-Knowledge.ps1` 生成索引
- [ ] 将面试信息填入 `resumes/template.md`
- [ ] 在 Claude Code 中输入 `开始面试` 或 `模拟面试`

## 前置条件

| 依赖 | 版本要求 | 用途 |
|------|---------|------|
| Python | 3.8+ | 运行选题脚本、构建索引 |
| Claude Code | 最新 | 面试流程的 AI 引擎 |
| PowerShell / bash | 任意 | 执行构建脚本 |

## 使用指南

### 模拟面试

在 Claude Code 中提及「面试」关键词即可自动触发。面试按以下阶段进行：

```
自我介绍 → 技术深挖 → 项目深挖 → 手撕代码 → 总结评估 → 反问 → 归档
```

参数参考（AI 内部自动调用，无需手动执行）：

```powershell
# 技术深挖：按标签和难度抽题
python src/pick.py --source 八股 --tag C++ --level basic --fallback

# 手撕代码：随机出编程题
python src/pick.py --source 手撕 --tag Algorithms --asked 1,3,5-10 --fallback
```

### 答题指导

除了面试模式，这套 Skill 还包含**答题指导**功能。当你说「面试问到 X 该怎么答」时，Claude 会加载答题指导模式，帮助你理解：

- 这个问题的考察意图是什么
- 回答要点和最佳实践
- 常见的回答误区
- 如果是面试官追问，下一步可能会问什么

### 维护题库

题库文件位于 `knowledge-base/` 目录：

| 文件 | 内容 | 格式 |
|------|------|------|
| `fundamentals.md` | 概念、原理、设计类问题 | `## 技术栈 → ### 子话题 → - [标签][难度] 题目` |
| `coding-challenges.md` | 编程题 | `1. [标签] 题目描述` |

修改后重新构建索引：

```powershell
.\Build-Knowledge.ps1
```

索引构建过程：
1. `build_index.py` — 从 markdown 解析题目，生成 `data/index.json`
2. `build_graph.py` — 自动提取知识点关联，生成 `data/knowledge-graph.json`
3. `validate_consistency.py` — 校验路径引用一致性

#### 题目格式示例

```markdown
## C++

### 多态
- [C++][basic] C++ 中多态的实现原理是什么？
- [C++][Advanced] 虚函数表的布局是怎样的？多重继承下有几个虚表指针？
  关联: C# · Unity
```

## 目录结构

```
interview/                          # 项目根目录
├── Build-Knowledge.ps1             # 一键构建索引 + 知识图谱
├── README.md                       # 本文件
├── weak-areas.md                   # 历史薄弱知识点汇总（自动更新）
│
├── src/                            # Python 工具脚本
│   ├── pick.py                     # 随机选题引擎
│   ├── build_index.py              # 从 markdown 解析生成索引
│   ├── build_graph.py              # 自动提取知识图谱关联
│   └── validate_consistency.py     # 路径与引用一致性校验
│
├── knowledge-base/                 # 题库（由你维护）
│   ├── fundamentals.md             # 概念/原理/设计题
│   └── coding-challenges.md        # 编程题
│
├── data/                           # 自动生成的索引文件
│   ├── index.json                  # 结构化题库索引
│   └── knowledge-graph.json        # 知识点关联图谱
│
├── resumes/                        # 候选人简历（按需填写）
│   └── template.md
│
├── records/                        # 面试记录（自动归档）
│   └── template.md
│
└── .claude/skills/                 # Claude Code Skill 定义
    ├── interview/interview.md      # 面试流程 Skill
    └── interview-prep/SKILL.md     # 答题指导 Skill
```

## 流程详解

### 面试阶段流转

```
┌─────────────┐
│  自我介绍    │  ← 面试者简述背景
└─────┬───────┘
      ▼
┌─────────────┐     ┌──────────────────┐
│  技术深挖    │────▶│  自适应出题       │
│  (15-20min) │     │  - 按标签/难度   │
└─────┬───────┘     │  - 覆盖多领域    │
      │             │  - 弱势优先      │
      ▼             └──────────────────┘
┌─────────────┐
│  项目深挖    │  ← 针对简历项目深入提问
└─────┬───────┘
      ▼
┌─────────────┐
│  手撕代码    │  ← 随机出编程题，限时完成
└─────┬───────┘
      ▼
┌─────────────┐
│  总结评估    │  ← 结构化评分 + 面试总结
└─────┬───────┘
      ▼
┌─────────────┐
│  反问环节    │  ← "你还有什么想问我的吗？"
└─────┬───────┘
      ▼
┌─────────────┐
│  归档       │  ← 写入 records/ + 更新 weak-areas.md
└─────────────┘
```

### 自适应难度调整

面试 AI 会根据候选人的回答质量动态调整策略：

| 表现 | AI 策略 |
|------|---------|
| 连续答对 3 题以上 | 提高 Advanced 题比例 |
| 连续答错 2 题以上 | 换基础领域或降低难度 |
| 回答准确且深入 | 当前子话题出 Advanced 题 |
| 回答不准确 | 回溯前置基础知识 |

### 弱势追踪

`weak-areas.md` 记录了历次面试中候选人答得不完整的技术点。下次面试同一候选人时，AI 会优先覆盖这些薄弱领域，并有针对性地增加 Advanced 题比例。

## 自定义你的 Skill

### 修改面试官风格

编辑 `.claude/skills/interview/interview.md` 中的「角色定义」和「核心约束」部分，可以调整面试官的语气、追问深度、严格程度等。

### 扩展题库

- `knowledge-base/fundamentals.md`：添加技术栈（`##`）→ 子话题（`###`）→ 题目（`- [tag][level] text`）
- 标签体系：`C++`、`C#`、`Unity`、`Graphics`、`Algorithms`、`Networking`、`DesignPatterns`、`GameDesign`、`Performance`
- 难度分级：`basic`、`intermediate`、`Advanced`
- 支持多标签：`- [C++][C#][Advanced] 题目描述`

### 添加跨栈关联

在子话题下添加 `关联:` 注释，图谱构建时会自动提取：

```markdown
### 内存管理
- [C++][basic] 讲讲 C++ 的内存分区。
  关联: C# · Unity
```

## FAQ

**Q: 必须用 Claude Code 吗？**
A: 是的，这套系统是 Claude Code 的 Skill，依赖 Claude 的 AI 能力运行。如果想用其他的 IDE,可以将 CLAUDE.md 中的内容复制到 agent.md,再将 .claude 文件夹转换为相对应的文件夹

**Q: 可以和其他 AI 工具一起用吗？**
A: 核心选题脚本（`pick.py`）和索引构建（`build_index.py`）是纯 Python 工具，可以在任何环境中运行。但面试流程本身需要 Claude Code 的 Skill 系统支持。

**Q: 题库如何导入已有的面试题？**
A: 按照 `fundamentals.md` 的格式添加题目，确保标签和难度标记正确，然后运行 `Build-Knowledge.ps1` 重建索引即可。

**Q: 面试记录保存在哪里？**
A: 自动保存到 `records/` 目录，文件名格式为 `YYYY-MM-DD_面试者.md`。

**Q: 如何重置状态（比如换一位面试者）？**
A: 在 Claude Code 中开始新对话即可。所有面试状态（已问题号、计数器等）都是对话级的。


## 贡献指南

欢迎通过 Issue 和 Pull Request 贡献：

1. **题库扩充** — 在 `knowledge-base/` 中添加新题目，遵循标签和难度标记规范
2. **脚本改进** — 优化 `src/` 下的 Python 工具
3. **Skill 优化** — 改进面试流程的提示词质量

提交前请运行一致性校验：

```powershell
python src/validate_consistency.py
```

## 许可

MIT © 2026 Concorde0
