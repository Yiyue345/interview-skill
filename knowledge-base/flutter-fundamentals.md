# Flutter 开发基础题库

## Dart

### 语言与异步
- [Dart][basic] final 与 const 的语义有什么区别？
- [Dart][basic] Dart 的空安全如何表达可空与非空类型？
- [Dart][intermediate] Future 与 Stream 分别适合什么异步场景？
- [Dart][intermediate] mixin 与继承应如何选择？
- [Dart][intermediate] Dart 事件循环如何调度微任务队列与事件队列？
- [Dart][intermediate] Stream 订阅未取消会造成哪些资源和生命周期问题？
- [Dart][advanced] Isolate 的内存隔离对并发设计有什么影响？
- [Dart][advanced] Dart GC 与 Android Runtime 的 Java/Kotlin GC 有哪些关键差异？

## FlutterWidgets

### Widget 与渲染
- [FlutterWidgets][basic] StatelessWidget 与 StatefulWidget 如何选择？
- [FlutterWidgets][basic] BuildContext 表示什么？
- [FlutterWidgets][basic] StatefulWidget 的主要生命周期回调有哪些？
- [FlutterWidgets][basic] Flutter 的 Framework、Engine 与 Embedder 分别承担什么职责？
- [FlutterWidgets][basic] Flutter 为什么能够在多个平台复用 UI 代码？
- [FlutterWidgets][intermediate] Widget、Element 与 RenderObject 的关系是什么？
- [FlutterWidgets][intermediate] Key 在节点复用和状态保持中有什么作用？
- [FlutterWidgets][intermediate] setState 调用后，框架如何找到并重建需要更新的节点？
- [FlutterWidgets][intermediate] 为什么 BuildContext 不应在异步间隙后直接使用？
- [FlutterWidgets][intermediate] Widget 为什么可以保持轻量且被频繁创建？
- [FlutterWidgets][intermediate] Flutter 与 Android View 的布局和渲染机制有什么区别？
- [FlutterWidgets][advanced] Flutter 一帧的构建、布局、绘制和合成流程是什么？
- [FlutterWidgets][advanced] UI isolate 与 Raster 线程如何协作生成一帧画面？
- [FlutterWidgets][advanced] Skia 或 Impeller 在 Flutter 渲染链路中承担什么职责？
  关联: FlutterState · FlutterPerformance

## FlutterState

### 状态管理
- [FlutterState][basic] setState 适合管理什么范围的状态？
- [FlutterState][basic] 局部状态与全局状态应如何划分？
- [FlutterState][intermediate] Provider、Riverpod 与 BLoC 的核心差异是什么？
- [FlutterState][intermediate] 如何避免状态变化引起大范围重建？
- [FlutterState][intermediate] Builder、Consumer、Selector 与局部监听分别适合什么场景？
- [FlutterState][intermediate] ValueListenableBuilder 适合管理哪类局部高频状态？
- [FlutterState][intermediate] 如何发现页面中被频繁重建的 Widget？
- [FlutterState][intermediate] 为什么拆分大型 Widget 有助于缩小重建范围？
- [FlutterState][advanced] 为什么不可变状态更容易追踪变化并编写测试？
  关联: FlutterArchitecture

## FlutterPlatform

### 平台集成
- [FlutterPlatform][basic] MethodChannel 解决了什么问题？
- [FlutterPlatform][basic] Flutter 插件通常包含哪些平台部分？
- [FlutterPlatform][intermediate] 如何处理 Android 与 iOS 生命周期差异？
- [FlutterPlatform][intermediate] 后台任务和通知能力为什么需要平台适配？
- [FlutterPlatform][intermediate] MethodChannel 在数据编码和线程切换时会产生哪些性能开销？
- [FlutterPlatform][intermediate] Flutter 页面频繁调用原生能力时应如何批处理或降低通信次数？
- [FlutterPlatform][advanced] Flutter 页面嵌入原生应用时需要关注哪些启动、内存和生命周期风险？
- [FlutterPlatform][advanced] 如何设计可测试且支持多平台的原生能力抽象？
  关联: FlutterArchitecture · FlutterPerformance

## FlutterArchitecture

### 应用架构
- [FlutterArchitecture][basic] 页面、领域逻辑和数据访问应如何分层？
- [FlutterArchitecture][basic] 为什么要将导航和业务状态解耦？
- [FlutterArchitecture][intermediate] 如何设计可替换的网络层与本地存储层？
- [FlutterArchitecture][intermediate] 大型 Flutter 工程如何按 feature 模块化？
- [FlutterArchitecture][intermediate] Flutter 列表分页时如何协调首次加载、刷新和追加状态？
- [FlutterArchitecture][intermediate] 如何避免滚动触底或重复监听造成分页请求堆积？
- [FlutterArchitecture][advanced] 多 package 工程如何治理依赖与版本？
  关联: FlutterPerformance

## FlutterPerformance

### 性能与稳定性
- [FlutterPerformance][basic] const Widget 如何减少无效对象创建？
- [FlutterPerformance][basic] 如何避免大图造成内存峰值？
- [FlutterPerformance][basic] ListView 与 ListView.builder 在子节点创建方式上有什么区别？
- [FlutterPerformance][basic] Flutter 控制器为什么需要在不再使用时调用 dispose？
- [FlutterPerformance][intermediate] 如何定位 UI 线程与 Raster 线程卡顿？
- [FlutterPerformance][intermediate] RepaintBoundary 在什么情况下有效？
- [FlutterPerformance][intermediate] build 方法频繁执行是否一定意味着存在性能问题？
- [FlutterPerformance][intermediate] itemExtent 与 prototypeItem 如何减少长列表布局成本？
- [FlutterPerformance][intermediate] 如何优化长列表中的复杂条目、图片和动画？
- [FlutterPerformance][intermediate] Flutter 图片内存缓存如何工作，何时需要磁盘缓存？
- [FlutterPerformance][intermediate] Flutter 为什么可能出现着色器编译卡顿，如何缓解？
- [FlutterPerformance][intermediate] Flutter DevTools 如何分别排查卡顿、内存和界面布局问题？
- [FlutterPerformance][intermediate] Image.asset、Image.network 与缓存图片组件在资源管理上有什么区别？
- [FlutterPerformance][intermediate] 如何分析并减少 Flutter 应用包体积？
- [FlutterPerformance][advanced] 如何定位 Flutter 应用中持续增长的内存占用？
- [FlutterPerformance][advanced] 如何比较 Flutter 与 Android 原生在启动和渲染性能上的差异？
- [FlutterPerformance][advanced] 如何验证一次 rebuild、列表或图片优化取得了真实收益？
- [FlutterPerformance][advanced] 如何设计 Flutter 崩溃、卡顿和启动指标监控？
