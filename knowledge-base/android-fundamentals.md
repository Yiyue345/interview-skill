# Android 原生开发基础题库

## Kotlin

### 语言与协程
- [Kotlin][basic] val 与 var 的语义有什么区别？
- [Kotlin][basic] 可空类型如何减少空指针异常？
- [Kotlin][intermediate] data class 自动生成了哪些能力？
- [Kotlin][intermediate] suspend 函数与普通函数有什么区别？
- [Kotlin][advanced] Kotlin 协程的结构化并发解决了什么问题？

## AndroidLifecycle

### 组件生命周期
- [AndroidLifecycle][basic] Activity 的主要生命周期回调有哪些？
- [AndroidLifecycle][basic] Fragment 的视图生命周期为什么独立存在？
- [AndroidLifecycle][intermediate] 配置变化时如何保存和恢复界面状态？
- [AndroidLifecycle][intermediate] 进程被系统回收后应用应如何恢复？
- [AndroidLifecycle][advanced] 如何避免生命周期与异步任务错配导致泄漏或崩溃？
  关联: AndroidUI · AndroidData

## AndroidUI

### View 与 Compose
- [AndroidUI][basic] dp、sp 与 px 分别适合什么场景？
- [AndroidUI][basic] RecyclerView 的复用机制解决了什么问题？
- [AndroidUI][intermediate] Compose 重组在什么情况下发生？
- [AndroidUI][intermediate] 如何避免列表滚动中的重复布局和图片抖动？
- [AndroidUI][advanced] 如何设计同时支持无障碍和多尺寸屏幕的 UI？
  关联: AndroidArchitecture · AndroidPerformance

## AndroidData

### 数据与网络
- [AndroidData][basic] SharedPreferences 与数据库分别适合存储什么？
- [AndroidData][basic] Android 网络请求为什么需要在后台执行？
- [AndroidData][intermediate] Room 如何处理数据库版本迁移？
- [AndroidData][intermediate] 离线缓存与服务端数据冲突时如何处理？
- [AndroidData][advanced] 如何设计支持分页、重试和离线读取的数据仓库？
  关联: AndroidArchitecture

## AndroidArchitecture

### Jetpack 架构
- [AndroidArchitecture][basic] ViewModel 为什么能够跨配置变化保留状态？
- [AndroidArchitecture][basic] 单向数据流对复杂页面有什么帮助？
- [AndroidArchitecture][intermediate] StateFlow 与 SharedFlow 如何选择？
- [AndroidArchitecture][intermediate] Repository 层应承担哪些职责？
- [AndroidArchitecture][advanced] 多模块 Android 工程如何划分依赖边界？
  关联: AndroidPerformance

## AndroidPerformance

### 性能与稳定性
- [AndroidPerformance][basic] ANR 的常见原因有哪些？
- [AndroidPerformance][basic] 如何避免 Bitmap 导致内存峰值？
- [AndroidPerformance][intermediate] 如何定位启动、渲染和 IO 卡顿？
- [AndroidPerformance][intermediate] 如何发现 Activity 或 Fragment 泄漏？
- [AndroidPerformance][advanced] 如何设计 Android 性能指标采集并控制开销？
