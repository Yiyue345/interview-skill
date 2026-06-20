# 通用计算机网络题库

## ComputerNetworking

### 网络分层与传输
- [ComputerNetworking][basic] TCP/IP 模型各层分别解决什么问题？
- [ComputerNetworking][basic] TCP 和 UDP 的主要区别是什么？
- [ComputerNetworking][basic] IP 地址和端口分别标识什么？
- [ComputerNetworking][basic] DNS 如何把域名解析为 IP 地址？
- [ComputerNetworking][intermediate] TCP 为什么需要三次握手建立连接？
- [ComputerNetworking][intermediate] TCP 关闭连接时为什么通常需要四次挥手？
- [ComputerNetworking][intermediate] TCP 如何通过确认、重传和排序保证可靠传输？
- [ComputerNetworking][advanced] TCP 的流量控制和拥塞控制分别解决什么问题？

### HTTP 与长连接
- [ComputerNetworking][basic] HTTP 和 HTTPS 的主要区别是什么？
- [ComputerNetworking][basic] 常见 HTTP 状态码分别表示什么？
- [ComputerNetworking][basic] Cookie、Session 和 Token 分别如何保存登录状态？
- [ComputerNetworking][intermediate] HTTP 长连接和连接池为什么能减少请求耗时？
- [ComputerNetworking][intermediate] HTTP/1.1、HTTP/2 和 HTTP/3 的主要差异是什么？
- [ComputerNetworking][intermediate] WebSocket 与普通 HTTP 请求有什么区别？
- [ComputerNetworking][advanced] TLS 握手如何建立加密连接并验证服务器身份？
- [ComputerNetworking][advanced] HTTP/3 为什么基于 QUIC，而不是直接使用 TCP？

### 请求可靠性与安全
- [ComputerNetworking][basic] 请求超时和连接超时有什么区别？
- [ComputerNetworking][basic] 哪些 HTTP 方法通常应当保持幂等？
- [ComputerNetworking][intermediate] 网络请求失败后，什么情况下适合重试？
- [ComputerNetworking][intermediate] 重试请求时为什么要逐步增加等待时间？
- [ComputerNetworking][intermediate] 客户端如何避免重复提交同一个操作？
- [ComputerNetworking][advanced] 如何设计同时支持超时、取消和重试的请求链路？

### 服务端网络模型
- [ComputerNetworking][intermediate] 阻塞 IO、非阻塞 IO 和 IO 多路复用有什么区别？
- [ComputerNetworking][advanced] 高并发服务器为什么常使用 epoll 或类似的事件通知机制？
