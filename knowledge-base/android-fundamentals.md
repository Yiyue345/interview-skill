# Android 原生开发基础题库

## Kotlin

### 语言与协程
- [Kotlin][basic] val 与 var 的语义有什么区别？
- [Kotlin][basic] 可空类型如何减少空指针异常？
- [Kotlin][basic] Kotlin 相比 Java 在 Android 开发中有哪些主要优势？
- [Kotlin][basic] Kotlin 的安全调用、Elvis 和非空断言操作符分别有什么语义？
- [Kotlin][intermediate] data class 自动生成了哪些能力？
- [Kotlin][intermediate] suspend 函数与普通函数有什么区别？
- [Kotlin][intermediate] Kotlin 协程与操作系统线程有什么区别？
- [Kotlin][intermediate] Dispatchers.Main、IO 与 Default 分别适合什么任务？
- [Kotlin][intermediate] suspend 函数在编译后如何通过状态机实现挂起与恢复？
- [Kotlin][advanced] Kotlin 协程的结构化并发解决了什么问题？

## AndroidLifecycle

### 组件生命周期
- [AndroidLifecycle][basic] Activity 的主要生命周期回调有哪些？
- [AndroidLifecycle][basic] Fragment 的视图生命周期为什么独立存在？
- [AndroidLifecycle][basic] Android 四大组件分别承担什么职责？
- [AndroidLifecycle][basic] standard、singleTop、singleTask 与 singleInstance 启动模式有什么区别？
- [AndroidLifecycle][intermediate] 配置变化时如何保存和恢复界面状态？
- [AndroidLifecycle][intermediate] 进程被系统回收后应用应如何恢复？
- [AndroidLifecycle][intermediate] ViewModel 生命周期与 Activity 生命周期有什么区别？
- [AndroidLifecycle][intermediate] Handler、Looper 与 MessageQueue 如何协作完成消息调度？
- [AndroidLifecycle][intermediate] Binder 相比传统 IPC 方案有哪些特点？
- [AndroidLifecycle][advanced] 如何避免生命周期与异步任务错配导致泄漏或崩溃？
  关联: AndroidUI · AndroidData

## AndroidUI

### View 与 Compose
- [AndroidUI][basic] dp、sp 与 px 分别适合什么场景？
- [AndroidUI][basic] RecyclerView 的复用机制解决了什么问题？
- [AndroidUI][basic] Android View 的 measure、layout 和 draw 分别负责什么？
- [AndroidUI][basic] 一帧超过刷新周期时为什么会出现掉帧或卡顿？
- [AndroidUI][intermediate] Compose 重组在什么情况下发生？
- [AndroidUI][intermediate] 如何避免列表滚动中的重复布局和图片抖动？
- [AndroidUI][intermediate] 过度绘制是什么，如何检测和减少？
- [AndroidUI][intermediate] 为什么层级过深的布局会增加测量和布局成本？
- [AndroidUI][intermediate] DiffUtil 相比 notifyDataSetChanged 有什么优势？
- [AndroidUI][intermediate] RecyclerView 嵌套、复杂动画或视频条目会带来哪些性能风险？
- [AndroidUI][advanced] 如何设计同时支持无障碍和多尺寸屏幕的 UI？
  关联: AndroidArchitecture · AndroidPerformance

## AndroidData

### 数据与网络
- [AndroidData][basic] SharedPreferences 与数据库分别适合存储什么？
- [AndroidData][basic] Android 网络请求为什么需要在后台执行？
- [AndroidData][basic] Room 的 Entity、DAO 与 Database 分别承担什么职责？
- [AndroidData][basic] Room 相比直接使用 SQLiteOpenHelper 有哪些优势？
- [AndroidData][basic] Retrofit、OkHttp 与序列化库在网络请求链路中如何分工？
- [AndroidData][intermediate] Room 如何处理数据库版本迁移？
- [AndroidData][intermediate] Retrofit 为什么能通过声明式接口发起网络请求？
- [AndroidData][intermediate] Moshi 与 Gson 在类型安全、代码生成和反射方面有什么差异？
- [AndroidData][intermediate] OkHttp 拦截器适合统一处理哪些事情，例如认证、日志和缓存？
- [AndroidData][intermediate] Room 查询为什么默认禁止在主线程执行？
- [AndroidData][intermediate] Room 数据不断增长时，如何通过索引、分页和只查询所需字段提升速度？
- [AndroidData][intermediate] 如何避免频繁数据库读写阻塞页面或放大耗电？
- [AndroidData][advanced] 如何设计同时支持分页、失败重试和离线读取的数据层？
  关联: AndroidArchitecture

## AndroidArchitecture

### Jetpack 架构
- [AndroidArchitecture][basic] ViewModel 为什么能够跨配置变化保留状态？
- [AndroidArchitecture][basic] 单向数据流对复杂页面有什么帮助？
- [AndroidArchitecture][basic] MVVM 中 View、ViewModel 与 Model 应如何划分职责？
- [AndroidArchitecture][intermediate] StateFlow 与 SharedFlow 如何选择？
- [AndroidArchitecture][intermediate] Repository 层应承担哪些职责？
- [AndroidArchitecture][intermediate] LiveData 与 StateFlow 在生命周期和状态语义上有什么区别？
- [AndroidArchitecture][intermediate] ViewModel 为什么不应持有 Activity 或 View 引用？
- [AndroidArchitecture][advanced] 多模块 Android 工程如何划分依赖边界？
  关联: AndroidPerformance

## AndroidPerformance

### 性能与稳定性
- [AndroidPerformance][basic] ANR 的常见原因有哪些？
- [AndroidPerformance][basic] 如何避免 Bitmap 导致内存峰值？
- [AndroidPerformance][basic] Android 冷启动、温启动和热启动分别是什么？
- [AndroidPerformance][basic] Application 中执行大量同步初始化会产生什么影响？
- [AndroidPerformance][basic] 什么是 Android 内存泄漏，哪些对象持有关系容易引发泄漏？
- [AndroidPerformance][intermediate] 如何定位启动、渲染和 IO 卡顿？
- [AndroidPerformance][intermediate] 如何发现 Activity 或 Fragment 泄漏？
- [AndroidPerformance][intermediate] App 冷启动从进程创建到首帧显示经历哪些阶段？
- [AndroidPerformance][intermediate] 启动窗口白屏或黑屏通常如何产生和优化？
- [AndroidPerformance][intermediate] 第三方 SDK 如何进行延迟、异步或按需初始化？
- [AndroidPerformance][intermediate] 如何分别测量首帧显示时间和页面可操作时间？
- [AndroidPerformance][intermediate] Handler 和非静态内部类为什么容易间接持有 Activity？
- [AndroidPerformance][intermediate] lifecycleScope 与 repeatOnLifecycle 如何降低异步任务泄漏风险？
- [AndroidPerformance][intermediate] LeakCanary 如何找出是谁一直持有本应释放的对象？
- [AndroidPerformance][intermediate] OkHttp 连接池如何减少网络请求延迟和资源开销？
- [AndroidPerformance][intermediate] Android Studio Profiler、Perfetto 与系统日志分别适合定位什么问题？
- [AndroidPerformance][advanced] 如何系统定位一次只在部分设备出现的页面卡顿？
- [AndroidPerformance][advanced] 如何验证启动、内存或渲染优化确实产生了收益？
- [AndroidPerformance][advanced] 如何设计 Android 性能指标采集并控制开销？
