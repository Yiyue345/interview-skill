# 移动端通用架构与服务集成题库

## MobileArchitecture

### 分层与状态建模
- [MobileArchitecture][basic] 一个完整的移动端应用通常包含哪些技术层次？
- [MobileArchitecture][basic] 如何划分界面状态、业务状态和需要长期保存的数据？
- [MobileArchitecture][intermediate] 网络数据、本地数据与 UI 状态应如何建立单向数据流？
- [MobileArchitecture][intermediate] 如何用加载、成功、空数据和失败四种状态统一描述异步页面？
- [MobileArchitecture][intermediate] 如何避免服务端字段变化直接影响业务逻辑和界面？
- [MobileArchitecture][advanced] 如何设计同时支持在线、离线和冲突恢复的移动端数据层？

### 分页与请求并发
- [MobileArchitecture][basic] 页码、游标和时间戳分页分别适合什么场景？
- [MobileArchitecture][intermediate] 下拉刷新和上拉加载更多并存时如何避免状态错乱？
- [MobileArchitecture][intermediate] 如何避免慢接口导致重复请求或旧响应覆盖新状态？
- [MobileArchitecture][advanced] 如何设计支持取消、去重、重试和缓存复用的请求调度层？

## MobileNetworking

### API 与弱网治理
- [MobileNetworking][basic] 移动端调用 REST API 时常见的认证方式有哪些？
- [MobileNetworking][basic] 搜索接口为什么通常需要防抖？
- [MobileNetworking][intermediate] 用户连续修改搜索条件时如何取消旧请求并避免响应乱序？
- [MobileNetworking][intermediate] 客户端应如何统一处理超时、无网络、限流和业务错误？
- [MobileNetworking][intermediate] 如何设计移动端接口缓存及其过期策略？
- [MobileNetworking][intermediate] HTTP 强缓存与协商缓存分别如何工作？
- [MobileNetworking][advanced] 弱网环境下如何设置超时、重试间隔和离线降级？
- [MobileNetworking][advanced] 大体积 JSON 响应会在哪些阶段造成性能问题，客户端应如何优化？

### 图片与列表数据
- [MobileNetworking][basic] 移动端图片加载为什么需要内存缓存和磁盘缓存？
- [MobileNetworking][intermediate] 如何避免页面每次进入时重复请求未变化的数据？
- [MobileNetworking][advanced] 如何设计头像、缩略图和原图的多级缓存及淘汰策略？

## BackendSecurity

### BaaS 与数据权限
- [BackendSecurity][basic] 使用 BaaS 与自建后端分别有哪些优势和限制？
- [BackendSecurity][basic] Supabase Auth 的基本认证流程是什么？
- [BackendSecurity][intermediate] PostgreSQL 行级安全策略（RLS）解决了什么问题？
- [BackendSecurity][intermediate] RLS 与传统后端接口鉴权有什么区别？
- [BackendSecurity][intermediate] 如何用 RLS 保证用户只能修改或删除自己的数据？
- [BackendSecurity][advanced] 客户端可见的匿名访问密钥有哪些风险，应如何通过权限策略降低风险？
- [BackendSecurity][advanced] 为什么敏感第三方 API 调用通常应经过服务端函数而不是由客户端直连？

## LLMIntegration

### Agent 与工具调用
- [LLMIntegration][basic] ReAct Agent 的核心思想是什么？
- [LLMIntegration][basic] ReAct 中 Reasoning 与 Acting 分别承担什么职责？
- [LLMIntegration][intermediate] 大模型为什么需要工具调用，而不能只依赖模型内部知识？
- [LLMIntegration][intermediate] 工具的输入参数、输出结构和错误协议应如何设计？
- [LLMIntegration][intermediate] 如何约束大模型稳定输出可解析的结构化结果？
- [LLMIntegration][advanced] 如何防止 Agent 重复调用工具、无限循环或执行越权操作？

### 可靠性与体验
- [LLMIntegration][basic] LLM 请求超时或失败时客户端应呈现哪些状态？
- [LLMIntegration][intermediate] 如何降低自动生成内容跑题、重复或质量不稳定的问题？
- [LLMIntegration][intermediate] 检索结果过多时如何减少上下文 token 消耗？
- [LLMIntegration][intermediate] 流式输出如何改善长耗时生成任务的用户体验？
- [LLMIntegration][advanced] 如何记录 LLM 调用的耗时、错误和 token 用量来定位问题？
