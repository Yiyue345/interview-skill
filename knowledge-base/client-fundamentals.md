# 通用客户端基础题库

## C++

### 资源与并发
- [C++][basic] RAII 如何帮助管理客户端资源？
- [C++][basic] unique_ptr 与 shared_ptr 应如何选择？
- [C++][intermediate] UI 线程为什么不能执行耗时任务？
- [C++][intermediate] 线程间传递对象时如何明确所有权？
- [C++][advanced] 如何排查客户端中的悬空指针和内存破坏？

## C#

### 运行时与异步
- [C#][basic] 值类型与引用类型在传参时有什么差异？
- [C#][basic] IDisposable 模式解决了什么问题？
- [C#][intermediate] async 与 await 如何影响线程和执行上下文？
- [C#][intermediate] 委托、事件与观察者模式有什么联系？
- [C#][advanced] 如何减少高频交互中的 GC 压力？

## Android

### 生命周期与系统
- [Android][basic] Activity 的主要生命周期回调有哪些？
- [Android][basic] dp、sp 与 px 分别适合什么场景？
- [Android][intermediate] 配置变化时如何保存和恢复界面状态？
- [Android][intermediate] 主线程 ANR 的常见原因和定位方式是什么？
- [Android][advanced] Android 进程被系统回收后应用应如何恢复？
  关联: ClientArchitecture · ClientPerformance

## Flutter

### Widget 与状态
- [Flutter][basic] StatelessWidget 与 StatefulWidget 如何选择？
- [Flutter][basic] BuildContext 表示什么？
- [Flutter][intermediate] Widget、Element 与 RenderObject 的关系是什么？
- [Flutter][intermediate] 如何选择局部状态与全局状态管理方案？
- [Flutter][advanced] Flutter 一帧的构建、布局和绘制流程是什么？
  关联: ClientArchitecture · ClientPerformance

## ClientArchitecture

### 架构与数据流
- [ClientArchitecture][basic] MVC、MVP 与 MVVM 的职责划分有什么区别？
- [ClientArchitecture][basic] 客户端为什么需要明确的单向数据流？
- [ClientArchitecture][intermediate] 离线缓存与服务端数据冲突时如何处理？
- [ClientArchitecture][intermediate] 如何设计可替换的网络层和持久化层？
- [ClientArchitecture][advanced] 大型客户端如何进行模块化和依赖治理？
  关联: ClientPerformance

## ClientPerformance

### 性能与稳定性
- [ClientPerformance][basic] 客户端冷启动时间由哪些部分组成？
- [ClientPerformance][basic] 如何避免图片加载导致内存峰值？
- [ClientPerformance][intermediate] 如何定位卡顿发生在 CPU、GPU 还是 IO？
- [ClientPerformance][intermediate] 崩溃日志需要包含哪些诊断信息？
- [ClientPerformance][advanced] 如何设计性能指标采集并控制采集开销？
