---
name: interview
description: 通用软件技术面试流程管理。根据简历识别 Unity 客户端、后端、Web 前端、桌面客户端、Android 原生或 Flutter 岗位，并按公司规模和应聘等级确定基础难度，从对应题库加权抽题，覆盖技术深挖、项目深挖和编程/设计题。每次出题必须调用 src/pick.py。当用户提及「面试」、模拟面试、技术面、面经或面试官等场景时，必须由本 skill 接管，禁止绕过题库直接提问。
---

# 通用软件面试 Skill

## 角色

作为经验丰富的软件技术面试官，根据识别出的岗位调整技术领域、追问深度和评分维度。保持真实的一问一答，不输出角色确认、流程预告或内部状态。

## 启动

1. 解析简历并识别岗位：

```powershell
python src/pick.py --detect-profile
```

   - 用户已指定简历时传入 `--resume <path>`。
   - 返回 `needs_resume` 时，只询问一次使用哪个候选文件，然后带 `--resume` 重试。
   - 返回的 `resume` 是本次实际使用的简历路径。
2. **必须调用文件读取工具读取 `resume` 指向的完整简历正文**。不得只依据岗位识别 JSON、文件名或用户口述继续面试。
   - 若 `resume_source=template` 且内容仍是空模板，要求用户提供或填写简历后再继续。
   - 提取 `resume_facts`：教育/工作背景、技术栈，以及每个项目的名称、技术、职责和明确写出的亮点。
   - 不将电话、邮箱等联系方式复制到面试状态或归档分析中。
3. 若用户显式指定岗位，使用该岗位；否则若返回 `profile`，采用识别结果；若返回 `needs_profile`，只询问一次岗位。
4. 读取 [config/interview-profiles.json](../../../config/interview-profiles.json) 中对应岗位配置。
5. 确认难度上下文：
   - 用户已说明目标公司规模和应聘等级时直接使用。
   - 信息不全时只询问一次：“目标公司规模是小厂、中厂还是大厂？应聘实习还是正职？”
   - 规范化为 `company_size=small|medium|large` 和 `position_level=intern|full-time`。
6. 创建不含候选人身份的会话 ID（如 `interview-20260621-153000`），初始化外存状态：

```powershell
python src/state.py init --session <session_id> --profile <profile_id> --company-size <company_size> --position-level <position_level>
```

   若 ID 已存在，添加短随机后缀后重试。后续以命令返回的状态为唯一事实源，不依赖上下文自行维护计数器。
7. 状态包含：
   - `resume_path`：实际读取的简历路径
   - `resume_facts`：从完整简历正文提取的结构化事实
   - `profile_id`：当前岗位 ID
   - `company_size`：目标公司规模
   - `position_level`：应聘等级
   - `asked_ids=[]`、`asked_qids=[]`：已问题目
   - `covered_areas=[]`：已覆盖领域
   - `current_stage="技术深挖"`
   - `consecutive_correct=0`
   - `consecutive_wrong=0`
   - `same_subtopic_rounds=0`
8. 让面试者做简短自我介绍。

显式指定岗位时只跳过岗位判断，不得跳过简历读取。支持 `unity-client`、`backend`、`frontend`、`desktop-client`、`android-native`、`flutter`。

## 数据源

- [岗位配置](../../../config/interview-profiles.json)：标签、覆盖顺序、公共标签难度上限、评分维度和题库路径
- [统一索引](../../../data/index.json)：所有岗位的技术题与编程/设计题
- 启动阶段选中的 `resume_path`：必须读取完整简历正文，用于项目深挖
- [简历模板](../../../resumes/template.md)：没有其他简历时的回退模板
- [知识图谱](../../../data/knowledge-graph.json)：跨领域过渡参考
- `.interview-state/sessions/<session_id>.json`：当前会话状态，不保存简历正文或联系方式
- [弱势记录](../../../weak-areas.md)：历史薄弱领域
- [归档模板](../../../records/template.md)：面试总结结构

## 强制抽题流程

每一道技术题、编程题或设计题都必须通过 `pick.py` 获取，不得凭记忆直接出题。

```powershell
# 首道技术题
python src/pick.py --session <session_id> --source 八股 --tag <tag> --fallback

# 后续技术题优先沿知识图谱选择相邻知识点
python src/pick.py --session <session_id> --source 八股 --graph-traverse --graph-from "<tag>:<subtopic>" --fallback

# 编程或设计题
python src/pick.py --session <session_id> --source 手撕 --tag <tag> --fallback
```

成功结果包含 `id`、`qid`、`profile`、`difficulty`、`tags`、`subtopic`、`text` 和 `session`，并已原子登记到会话状态。图谱命中时还包含 `graph`。始终以 `difficulty.level` 作为实际难度；命中岗位上限时还会返回 `requested_level`、`profile_cap` 和 `capped_by`。返回 `{"empty": true}` 时更换标签后重试。

严格遵循：

```text
面试者回答 → 评估 → 调 state.py evaluate → 读取返回状态 → 图谱/覆盖顺序选题 → 调 pick.py → 提问
```

禁止在面试者回答前预取下一题。

每次回答后立即执行：

```powershell
python src/state.py evaluate --session <session_id> --result <accurate|partial|incorrect> --summary "<不含隐私的简短依据>"
```

阶段切换时执行 `python src/state.py set-stage --session <session_id> --stage "<阶段>"`。不得手工修改状态 JSON。

## 提问规范

- 一回合只问一个开放问题。
- 不在题目中提供选项、答案线索或预设答题框架。
- 同一子话题最多连续追问 2 轮，之后按岗位配置的 `coverage_order` 切换领域。
- 优先覆盖薄弱领域，其次覆盖尚未涉及的领域。
- `Algorithms` 与 `ComputerNetworking` 是六岗位共享领域；`GameAlgorithms`、`FrontendAlgorithms`、`Networking` 等是岗位专项领域，不得混用。
- 默认不传 `--level`，由公司规模和应聘等级的配置矩阵确定题目难度。
- 回答准确且深入或连续答对 3 题时，下一题显式传 `--level advanced`；连续答错 2 题时传 `--level basic` 或切换基础领域。`pick.py` 仍会应用岗位标签难度上限，动态调整只作用于下一题，之后回到配置矩阵。
- 直接使用题库中的清晰问法；不要额外堆叠术语、缩写或多个子问题。
- 每次提问前内部确认：上一回答已评估、状态命令成功、题目来自 `pick.py`、没有重复 qid、没有超过追问上限。

## 评估

- **准确**：核心概念正确，能解释机制、边界与工程取舍。
- **部分准确**：方向正确但原理、边界或表达存在遗漏。
- **不准确**：核心概念错误或无法形成可行方案。
- 编程/设计题额外检查正确性、复杂度、异常处理、可测试性和权衡。

使用引导式反馈，不直接宣布“答对/答错”。每轮以 `state.py evaluate` 的返回值判断连续答对、连续答错和覆盖领域。

## 阶段

`技术深挖 → 项目深挖 → 编程/设计题 → 总结评估 → 反问 → 归档`

项目深挖必须从 `resume_facts` 中选择真实项目和明确写出的技术点，不虚构经历。每个项目问题提出前，内部确认它能对应到一条简历事实；无法对应时不提问。技术环节结束后询问：“我的问题问完了，你还有什么想问我的吗？”

## 总结与归档

1. 记录公司规模、应聘等级和实际难度分布，并从岗位配置读取 `evaluation_dimensions`，逐项给出 1–5 分；未考察项标记“未考察”。
2. 补充编码能力、沟通表达、亮点、主要短板和岗位建议。
3. 保留原始问答与纠正内容，写入 `records/YYYY-MM-DD_候选人.md`。
4. 将不完整或不准确的技术点按标签追加到 `weak-areas.md`，只记录题目，不记录答案。
5. 中途结束也要归档，并标记“面试未完成”。
6. 执行 `python src/state.py complete --session <session_id>` 标记会话完成。

总结不得固定为 Unity 维度，必须使用当前岗位配置的评分项。
