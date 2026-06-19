# 面试 Skill

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-8A2BE2)](#)
[![Codex Skill](https://img.shields.io/badge/OpenAI%20Codex-Skill-111111)](#)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python)](#)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-4A90D9)](#)
[![License](https://img.shields.io/badge/License-MIT-green)](#)

**可配置的通用软件技术面试系统。** 根据简历识别岗位，从对应题库加权抽题，覆盖技术深挖 → 项目深挖 → 编程/设计题全流程，并自动输出岗位化面试总结。

内置 `unity-client`、`backend`、`frontend`、`client` 四个岗位预设，也可以只添加配置和 Markdown 题库扩展新岗位。

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
- [TODO](#todo)
- [贡献指南](#贡献指南)
- [许可](#许可)

---

## 特点

- **岗位识别** — 从期望岗位、技术栈和简历全文识别方向，歧义时只询问一次
- **加权命题** — 新题优先，近期高频题自动衰减，当前面试同题不重复
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

# 2. 在 Codex 或 Claude Code 中开始面试
#    输入：开始面试
```

> Codex 会从 `.agents/skills/` 加载 Skill，Claude Code 会从 `.claude/skills/` 加载 Skill。

系统默认读取 `resumes/template.md` 识别岗位。也可以直接指定：

```powershell
python src/pick.py --profile backend --source 八股 --tag Java --level basic --fallback
python src/pick.py --resume resumes/template.md --detect-profile
```

### 首次使用 Checklist

- [ ] 运行 `Build-Knowledge.ps1` 生成索引
- [ ] 将面试信息填入 `resumes/template.md`
- [ ] 在 Codex 或 Claude Code 中输入 `开始面试` 或 `模拟面试`

## 前置条件

| 依赖 | 版本要求 | 用途 |
|------|---------|------|
| Python | 3.8+ | 运行选题脚本、构建索引 |
| Codex 或 Claude Code | 最新 | 面试流程的 AI 引擎 |
| PowerShell / bash | 任意 | 执行构建脚本 |

## 使用指南

### 模拟面试

在 Codex 或 Claude Code 中提及「面试」关键词即可自动触发。系统先识别岗位；无可靠结果时会请你从候选岗位中选择一次。面试按以下阶段进行：

```
自我介绍 → 技术深挖 → 项目深挖 → 手撕代码 → 总结评估 → 反问 → 归档
```

参数参考（AI 内部自动调用，无需手动执行）：

```powershell
# 技术深挖：按标签和难度抽题
python src/pick.py --profile unity-client --source 八股 --tag C++ --level basic --fallback

# 手撕代码：随机出编程题
python src/pick.py --profile unity-client --source 手撕 --tag Algorithms --asked 1,3,5-10 --fallback
```

### 答题指导

除了面试模式，这套 Skill 还包含**答题指导**功能。当你说「面试问到 X 该怎么答」时，AI 助手会加载答题指导模式，帮助你理解：

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
1. `build_index.py` — 从 `config/interview-profiles.json` 声明的 Markdown 题库生成统一索引
2. `build_graph.py` — 从全部岗位题库自动提取知识点关联
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
├── AGENTS.md                       # Codex 项目级行为约束
├── Build-Knowledge.ps1             # 一键构建索引 + 知识图谱
├── config/interview-profiles.json  # 岗位、题库、标签、识别词和评分维度
├── README.md                       # 本文件
├── weak-areas.md                   # 历史薄弱知识点汇总（自动更新）
│
├── src/                            # Python 工具脚本
│   ├── pick.py                     # 岗位过滤与加权抽题引擎
│   ├── profiles.py                 # 简历岗位识别
│   ├── project_paths.py            # 稳定项目路径
│   ├── build_index.py              # 从 markdown 解析生成索引
│   ├── build_graph.py              # 自动提取知识图谱关联
│   └── validate_consistency.py     # 路径与引用一致性校验
│
├── knowledge-base/                 # 题库（由你维护）
│   ├── fundamentals.md             # Unity 客户端原有题库
│   ├── backend-*.md                # 后端题库
│   ├── frontend-*.md               # Web 前端题库
│   └── client-*.md                 # 通用客户端题库
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
├── .agents/skills/                 # Codex Skill 定义
│   ├── build-knowledge/SKILL.md    # 知识库构建 Skill
│   ├── interview/SKILL.md          # 面试流程 Skill
│   └── interview-prep/SKILL.md     # 答题指导 Skill
└── .claude/skills/                 # Claude Code Skill 定义
    ├── build-knowledge/SKILL.md    # 知识库构建 Skill
    ├── interview/SKILL.md          # 面试流程 Skill
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

### 添加岗位预设

在 `config/interview-profiles.json` 中新增 profile，声明简历关键词、题库文件、标签、覆盖顺序、相近领域和评分维度；题库使用现有 Markdown 格式。无需修改 Python 标签白名单。

### 修改面试官风格

编辑对应平台的 `skills/interview/SKILL.md` 中「角色定义」和「核心约束」部分，可以调整面试官的语气、追问深度、严格程度等。共享规则应同步修改 `.agents/skills/` 与 `.claude/skills/`。

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
A: 不需要。项目同时支持 Codex CLI、Codex IDE 扩展、Codex App 和 Claude Code。请从仓库根目录启动对应工具，以便自动发现项目级 Skill。

**Q: 可以和其他 AI 工具一起用吗？**
A: 核心选题脚本（`pick.py`）和索引构建（`build_index.py`）是纯 Python 工具，可以在任何环境中运行。完整面试流程需要支持项目级 Skill 的 Codex 或 Claude Code。

**Q: 题库如何导入已有的面试题？**
A: 按照 `fundamentals.md` 的格式添加题目，确保标签和难度标记正确，然后运行 `Build-Knowledge.ps1` 重建索引即可。

**Q: 面试记录保存在哪里？**
A: 自动保存到 `records/` 目录，文件名格式为 `YYYY-MM-DD_面试者.md`。

**Q: 如何重置状态（比如换一位面试者）？**
A: 在 Codex 或 Claude Code 中开始新对话即可。所有面试状态（已问题号、计数器等）都是对话级的。


## 贡献指南

欢迎通过 Issue 和 Pull Request 贡献：

1. **题库扩充** — 在 `knowledge-base/` 中添加新题目，遵循标签和难度标记规范
2. **脚本改进** — 优化 `src/` 下的 Python 工具
3. **Skill 优化** — 改进面试流程的提示词质量

提交前请运行一致性校验：

```powershell
python src/validate_consistency.py
```

## TODO

> 如果你想改进，开个 Issue 说一声

### P0 架构缺陷

- [x] **加权抽题替代纯随机**
  使用岗位级本地历史记录曝光次数和时间，新题优先，近期题目衰减。
  → `src/pick.py`

- [x] **路径解析硬编码**
  所有脚本通过 `src/project_paths.py` 从固定文件位置确定项目根目录。
  → `src/project_paths.py`

### P1 能力缺失

- [ ] **图谱驱动自动出题链路**
  目前图谱只在 AI 联想时被动使用。
  → `src/pick.py`（新增 `--graph-traverse` 模式）

- [ ] **添加单元测试**
  `src/` 下 4 个脚本无测试。`pick.py` 的标签匹配、`build_index.py` 的 markdown 解析、`build_graph.py` 的边合并逻辑都是纯函数，适合 pytest。
  → `tests/`

- [ ] **对话状态外存化**
  现在 `asked_ids`、计数器、评估记录全在 LLM 上下文中。长面试场景，上下文累积后一致性维护会退化。
  → `src/state.py`（新增）

### P2 增量改进

- [ ] **语义追问推荐**
  候选人回答后，embedding 匹配题库中最相关的追问作为候选，而非 AI 凭记忆想下一题。可本地用 `sentence-transformers` 轻量实现。
  → `src/pick.py`（新增 `--semantic` 模式）

- [ ] **Makefile 跨平台构建入口**
  `Build-Knowledge.ps1` 仅限 Windows。加一个 `Makefile` 统一 `make build` / `make test` / `make lint`。
  → `Makefile`（新增）

## 许可

MIT © 2026 Concorde0
