# Flutter 开发基础题库

## Dart

### 语言与异步
- [Dart][basic] final 与 const 的语义有什么区别？
- [Dart][basic] Dart 的空安全如何表达可空与非空类型？
- [Dart][intermediate] Future 与 Stream 分别适合什么异步场景？
- [Dart][intermediate] mixin 与继承应如何选择？
- [Dart][advanced] Isolate 的内存隔离对并发设计有什么影响？

## FlutterWidgets

### Widget 与渲染
- [FlutterWidgets][basic] StatelessWidget 与 StatefulWidget 如何选择？
- [FlutterWidgets][basic] BuildContext 表示什么？
- [FlutterWidgets][intermediate] Widget、Element 与 RenderObject 的关系是什么？
- [FlutterWidgets][intermediate] Key 在节点复用和状态保持中有什么作用？
- [FlutterWidgets][advanced] Flutter 一帧的构建、布局、绘制和合成流程是什么？
  关联: FlutterState · FlutterPerformance

## FlutterState

### 状态管理
- [FlutterState][basic] setState 适合管理什么范围的状态？
- [FlutterState][basic] 局部状态与全局状态应如何划分？
- [FlutterState][intermediate] Provider、Riverpod 与 BLoC 的核心差异是什么？
- [FlutterState][intermediate] 如何避免状态变化引起大范围重建？
- [FlutterState][advanced] 如何用不可变状态设计可回放、可测试的数据流？
  关联: FlutterArchitecture

## FlutterPlatform

### 平台集成
- [FlutterPlatform][basic] MethodChannel 解决了什么问题？
- [FlutterPlatform][basic] Flutter 插件通常包含哪些平台部分？
- [FlutterPlatform][intermediate] 如何处理 Android 与 iOS 生命周期差异？
- [FlutterPlatform][intermediate] 后台任务和通知能力为什么需要平台适配？
- [FlutterPlatform][advanced] 如何设计可测试且支持多平台的原生能力抽象？
  关联: FlutterArchitecture · FlutterPerformance

## FlutterArchitecture

### 应用架构
- [FlutterArchitecture][basic] 页面、领域逻辑和数据访问应如何分层？
- [FlutterArchitecture][basic] 为什么要将导航和业务状态解耦？
- [FlutterArchitecture][intermediate] 如何设计可替换的网络层与本地存储层？
- [FlutterArchitecture][intermediate] 大型 Flutter 工程如何按 feature 模块化？
- [FlutterArchitecture][advanced] 多 package 工程如何治理依赖与版本？
  关联: FlutterPerformance

## FlutterPerformance

### 性能与稳定性
- [FlutterPerformance][basic] const Widget 如何减少无效对象创建？
- [FlutterPerformance][basic] 如何避免大图造成内存峰值？
- [FlutterPerformance][intermediate] 如何定位 UI 线程与 Raster 线程卡顿？
- [FlutterPerformance][intermediate] RepaintBoundary 在什么情况下有效？
- [FlutterPerformance][advanced] 如何设计 Flutter 崩溃、卡顿和启动指标监控？
