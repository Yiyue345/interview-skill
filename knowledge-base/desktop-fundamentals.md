# 桌面客户端开发基础题库

## C++

### 资源与并发
- [C++][basic] RAII 如何帮助管理窗口、文件和系统句柄？
- [C++][basic] unique_ptr 与 shared_ptr 在桌面客户端中应如何选择？
- [C++][intermediate] UI 线程为什么不能执行耗时任务？
- [C++][intermediate] 线程间传递对象时如何明确所有权？
- [C++][advanced] 如何排查悬空指针和跨模块内存释放问题？

## C#

### 运行时与异步
- [C#][basic] IDisposable 模式解决了什么问题？
- [C#][basic] 委托与事件在桌面 UI 中分别承担什么职责？
- [C#][intermediate] async 与 await 如何避免阻塞 UI 线程？
- [C#][intermediate] SynchronizationContext 如何影响异步回调？
- [C#][advanced] 如何定位桌面应用中的托管内存泄漏？

## DesktopUI

### UI 与交互
- [DesktopUI][basic] 保留模式 UI 与立即模式 UI 有什么区别？
- [DesktopUI][basic] 数据绑定可以减少哪些界面代码？
- [DesktopUI][intermediate] 大型列表如何使用虚拟化避免卡顿？
- [DesktopUI][intermediate] 高 DPI 与多显示器环境需要处理哪些问题？
- [DesktopUI][advanced] 如何设计可测试且不依赖具体 UI 框架的交互逻辑？
  关联: DesktopArchitecture · DesktopPerformance

## DesktopSystem

### 操作系统集成
- [DesktopSystem][basic] 进程与线程的资源隔离有什么区别？
- [DesktopSystem][basic] 文件锁和进程间互斥分别适合什么场景？
- [DesktopSystem][intermediate] 桌面应用如何实现单实例启动？
- [DesktopSystem][intermediate] 进程间通信方案应如何选择？
- [DesktopSystem][advanced] 自动更新程序如何保证完整性与失败回滚？
  关联: DesktopArchitecture · DesktopPerformance

## DesktopArchitecture

### 架构与模块化
- [DesktopArchitecture][basic] MVC、MVP 与 MVVM 的职责划分有什么区别？
- [DesktopArchitecture][basic] 为什么要将业务状态与窗口生命周期解耦？
- [DesktopArchitecture][intermediate] 如何设计可替换的网络层和持久化层？
- [DesktopArchitecture][intermediate] 插件系统如何隔离接口、版本和故障？
- [DesktopArchitecture][advanced] 大型桌面客户端如何治理跨模块依赖？
  关联: DesktopPerformance

## DesktopPerformance

### 性能与稳定性
- [DesktopPerformance][basic] 桌面应用冷启动时间由哪些部分组成？
- [DesktopPerformance][basic] 如何避免图片和文档预览造成内存峰值？
- [DesktopPerformance][intermediate] 如何区分 UI 卡顿来自 CPU、GPU 还是 IO？
- [DesktopPerformance][intermediate] 崩溃转储需要包含哪些诊断信息？
- [DesktopPerformance][advanced] 如何设计低开销的性能与稳定性监控？
