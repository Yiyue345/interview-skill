---
name: interview-prep
description: 通用软件面试答题指导。根据 Unity 客户端、后端、Web 前端或通用客户端岗位配置，从对应题库分析技术问题，提供考察意图、精炼回答、常见坑和追问预测。当用户询问答题指导、怎么回答、面试准备或面试攻略时使用。
---

# 通用面试答题指导 Skill

## 定位

从考生视角提供答题策略，不切换为模拟面试，不生成录用评级，不修改面试记录。

## 岗位与数据定位

1. 用户明确岗位时，读取 [岗位配置](../../../config/interview-profiles.json) 中对应 profile。
2. 用户未明确岗位时，调用：

```powershell
python src/pick.py --resume resumes/template.md --detect-profile
```

3. 返回 `needs_profile` 时，只询问一次岗位。
4. 根据 profile 的 `fundamentals`、`tags` 与 `coverage_order` 定位相关题库。
5. 读取 [统一索引](../../../data/index.json) 中同时匹配 profile 与话题的题目，并用 [知识图谱](../../../data/knowledge-graph.json) 预测关联追问。

## 输出结构

### 面试官意图

说明题型、关键考察信号和建议回答时间。

### 精炼回答建议

按“核心结论 → 底层原理 → 工程取舍 → 实际例子”组织成一条可直接表达的主线，不机械拆成多个等级。

### 常见坑

列出 2–3 个最可能导致扣分的概念混淆、遗漏或不合理工程判断。

### 后续追问预测

结合当前岗位的领域顺序、同子话题 advanced 题和知识图谱关联，说明面试官可能如何继续深入。

末尾给出相关话题建议。

## 使用模式

- 单题：针对一个明确问题输出完整四段指导。
- 岗位学习：按 profile 的 `coverage_order` 逐个覆盖子话题，并维护 `covered_subtopics` 避免重复。
- 学习模式优先处理 [weak-areas.md](../../../weak-areas.md) 中属于当前岗位标签的薄弱项。

## 质量要求

- 基础回答必须概念正确。
- 进阶回答应解释机制、边界和复杂度。
- 高质量回答应结合岗位场景说明方案权衡与实际经验。
- 不输出“请使用 pick.py 选题”，不要求用户现场作答，不修改 `weak-areas.md` 或 `records/`。
