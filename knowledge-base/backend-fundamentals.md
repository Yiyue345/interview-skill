# 后端开发基础题库

## Java

### 语言与集合
- [Java][basic] Java 中 equals 与 hashCode 为什么必须保持一致？
- [Java][basic] ArrayList 与 LinkedList 的适用场景有什么区别？
- [Java][intermediate] HashMap 在发生哈希冲突时如何组织数据？
- [Java][intermediate] checked exception 与 unchecked exception 应如何选择？
- [Java][advanced] JVM 类加载过程和双亲委派模型解决了什么问题？

## Python

### 运行时与并发
- [Python][basic] Python 的可变对象与不可变对象有什么区别？
- [Python][basic] 生成器相较于直接返回列表有什么优势？
- [Python][intermediate] 装饰器如何保留被包装函数的元数据？
- [Python][intermediate] GIL 对 CPU 密集和 IO 密集任务分别有什么影响？
- [Python][advanced] asyncio 事件循环如何调度协程？

## Database

### 事务与索引
- [Database][basic] 数据库事务的 ACID 分别表示什么？
- [Database][basic] B+ 树为什么适合作为数据库索引？
- [Database][intermediate] 联合索引的最左匹配原则是什么？
- [Database][intermediate] 可重复读隔离级别如何处理幻读？
- [Database][advanced] 如何定位并优化一条慢 SQL？
  关联: Cache · DistributedSystems

## Cache

### 缓存设计
- [Cache][basic] 使用缓存时为什么要设置过期时间？
- [Cache][basic] 缓存穿透、击穿和雪崩分别是什么？
- [Cache][intermediate] Cache Aside 模式如何保证数据库与缓存最终一致？
- [Cache][intermediate] Redis 的常用数据结构分别适合什么场景？
- [Cache][advanced] 热点 Key 和大 Key 应如何发现与治理？
  关联: Database · DistributedSystems

## DistributedSystems

### 一致性与可靠性
- [DistributedSystems][basic] 水平扩展与垂直扩展有什么区别？
- [DistributedSystems][basic] 服务为什么需要限流、熔断和降级？
- [DistributedSystems][intermediate] 消息队列如何避免消息丢失和重复消费？
- [DistributedSystems][intermediate] 分布式锁需要满足哪些正确性条件？
- [DistributedSystems][advanced] 如何在可用性与一致性之间做业务取舍？
  关联: BackendNetworking · Database

## BackendNetworking

### API 与网络
- [BackendNetworking][basic] HTTP 的幂等性是什么，哪些方法通常应保持幂等？
- [BackendNetworking][basic] Cookie、Session 与 Token 的区别是什么？
- [BackendNetworking][intermediate] REST API 如何设计分页、错误码和版本管理？
- [BackendNetworking][intermediate] TCP 长连接需要如何处理心跳和断线重连？
- [BackendNetworking][advanced] 如何设计一个支持超时、重试和链路追踪的服务调用？
  关联: DistributedSystems
