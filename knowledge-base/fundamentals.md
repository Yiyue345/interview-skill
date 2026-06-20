# 八股知识库

> 标签格式：`[技术栈][难度]`
> 技术栈：`C++` `C#` `Lua` `Unity` `Graphics` `Algorithms` `Networking` `DesignPatterns` `GameDesign` `Performance`
> 按技术栈 → 子话题分组，每子话题内 basic 在前、进阶在后

---

## C++

### 基本类型
- [C++][basic] int 和 long 的区别，long long 的大小
- [C++][basic] 指针在不同位系统下的字节数（32 位 4 字节，64 位 8 字节，兼容模式仍为 4 字节）

### 类与对象
- [C++][basic] struct和class的区别 在开发中如何使用
- [C++][basic] 三种继承方式对成员访问权限的影响
- [C++][basic] C++ 和 C 的区别
- [C++][basic] 空类占多大内存
- [C++][basic] 如何调用父类的虚函数？
- [C++][intermediate] 继承（内存长什么样，有/无虚函数时又长什么样）
- [C++][advanced] 菱形继承（有什么问题、虚继承、内存长什么样）
- [C++][intermediate] 菱形问题怎么解决
- [C++][advanced] 如果类中添加了静态成员变量、函数、虚函数，类的内存布局会怎样

### 多态
关联: C#
- [C++][basic] 函数重载 vs 函数重写
- [C++][advanced] 虚函数的实现原理（虚表 / 多态）
- [C++][intermediate] 多态（静态/动态多态，虚函数，虚表，原理）
- [C++][intermediate] 虚函数指针存储在哪里
- [C++][advanced] 虚函数表存储在哪里
- [C++][advanced] 虚函数表指针什么时候创建的
- [C++][advanced] 虚函数表存储在内存中的哪个区域？
- [C++][advanced] 多态里的虚函数底层是怎么实现的？
- [C++][advanced] 假如有十个同一个类的对象，虚函数表有几份
- [C++][intermediate] 构造函数能声明为虚函数吗？析构函数呢
- [C++][intermediate] 父类构造函数调用父类 virtual 时，调用的是哪个函数（父的还是子类重写的）

### 内存管理
关联: C#
- [C++][basic] C++ 内存分区有哪些？
- [C++][basic] 栈和堆的区别（举例）
- [C++][basic] 使用堆/栈的注意事项：堆需手动释放（C++）或避免 GC（C#），栈避免递归太深或过大局部变量导致溢出
- [C++][basic] 堆和栈有什么区别？为什么要有栈？为什么要有堆？
- [C++][basic] 堆和栈开辟内存
- [C++][basic] 全局变量存在哪
- [C++][basic] const 修饰的全局常量存储在哪里（常量存储区 / data 段）
- [C++][basic] 函数调用栈上存储了哪些内容（参数、局部变量、返回地址、调用约定信息）
- [C++][basic] 函数参数的入栈顺序（从右至左）
- [C++][basic] A a；和 A *p = new a；的区别（a 存在哪，p 存在哪，new a 存在哪）
- [C++][basic] 局部数组 / new 分配分别在哪？
- [C++][basic] new/malloc 区别
- [C++][basic] 内存布局（堆、栈等）
- [C++][advanced] 内存对齐原理 + 计算
- [C++][intermediate] 内存对齐的规则
- [C++][intermediate] 类大小计算（内存对齐）
- [C++][intermediate] 栈什么情况会爆
- [C++][advanced] 内存碎片，怎么设计一个内存管理系统避免内存碎片
- [C++][intermediate] delete 是怎么知道要 delete 多少字节
- [C++][intermediate] new int() 和 new int 的区别
- [C++][intermediate] placement new
- [C++][advanced] 如何检查内存泄漏
- [C++][advanced] 如何通过重载 new 和 delete 检测内存泄漏
- [C++][advanced] C++ 的内存模型
- [C++][intermediate] 类的成员变量存储位置：类定义本身在代码区，实例化对象的成员在堆/栈上取决于对象分配方式

### STL 容器
关联: C# · Algorithms
- [C++][basic] STL 有哪几个部分？
- [C++][basic] 介绍平时使用的容器
- [C++][basic] STL 你常用哪些容器？
- [C++][intermediate] vector 是如何动态扩容的？
- [C++][intermediate] vector 扩容机制
- [C++][intermediate] vector 和 list 的区别（局部性、性能、结构）
- [C++][intermediate] vector 中去重（erase 会有什么问题、迭代器）
- [C++][advanced] 如果自己实现一个 vector，你会怎么考虑
- [C++][advanced] map 的底层是什么，复杂度（红黑树）
- [C++][advanced] unordered_map / map（底层结构、哈希冲突怎么解决）
- [C++][intermediate] STL 的排序算法用的是什么？
- [C++][basic] vector 是被声明在栈上还是堆上
- [C++][basic] list&lt; T &gt; 底层结构
- [C++][advanced] 遍历数组和链表哪个更快（局部性、cache 命中、cacheline）
- [C++][advanced] 其他键值对存储结构：unordered_map，底层用哈希表
- [C++][advanced] 哈希表底层，map 底层存储结构，为什么要用红黑树？
- [C++][basic] emplace_back 和 push_back 的区别（emplace_back 直接在容器内构造，避免临时对象拷贝）
- [C++][intermediate] map 迭代遍历结果是有序的（红黑树中序遍历）

### 模板
- [C++][basic] 模板有什么好处
- [C++][advanced] 模板的特化与偏特化
- [C++][intermediate] 模板能不能声明定义分开写
- [C++][intermediate] 模板什么时候知道 T 的具体类型
- [C++][advanced] 模板在编译后在代码中是什么样子

### Lambda 与函数对象
- [C++][advanced] Lambda 表达式编译后的结果（编译为匿名类，捕获的变量转为成员变量）

### 智能指针
- [C++][basic] 智能指针的原理及使用场景（shared_ptr、unique_ptr、weak_ptr）
- [C++][basic] auto_ptr 被弃用的原因：operator= 转移管理权限，函数传参导致意外释放
- [C++][advanced] 智能指针的引用计数原理，循环引用怎么解决
- [C++][advanced] shared_ptr 的引用计数是线程安全的吗（控制块线程安全，指向的对象不保证）

### 构造与析构
- [C++][basic] 构造函数、析构函数在继承下的调用顺序
- [C++][intermediate] 构造函数能不能为 virtual
- [C++][intermediate] 析构函数为什么要是虚函数
- [C++][intermediate] 如果不通过 delete，离开作用域时自动销毁，会调用派生类的析构函数吗
- [C++][intermediate] 析构时先析构子还是父

### 类型与转换
- [C++][basic] 指针和引用的区别
- [C++][basic] const 常常用来处理哪些字段？
- [C++][basic] 常量指针和指针常量
- [C++][basic] static / const 用法
- [C++][basic] const 常量能用 const_cast 修改值吗？在什么场景下可以
- [C++][basic] 引用返回值的注意事项：不能返回局部变量的引用，参数需为引用类型才能返回其引用
- [C++][intermediate] C++ 四种 cast
- [C++][intermediate] static_cast 和 dynamic_cast 转换失败的区别（编译报错 / 指针返 null / 引用抛 bad_cast）
- [C++][intermediate] 两个无关联的 class 如何互相转换（需提供构造函数或类型转换运算符）
- [C++][basic] 引用传参传的是什么
- [C++][intermediate] i++ 和 ++i 哪个是左值哪个是右值
- [C++][intermediate] 左值右值、移动语义
- [C++][intermediate] 移动构造后需要将原对象的指针置空

### 多线程与并发
关联: Networking
- [C++][basic] 进程和线程的区别
- [C++][basic] 进程间有哪些通讯方式
- [C++][basic] 线程间的通讯方式
- [C++][advanced] 原子操作与无锁队列：将取改写合并为一步，适用于高性能场景
- [C++][advanced] 多线程下避免频繁访问同一内存（缓存一致性导致缓存行失效，增加访问延迟）
- [C++][basic] 讲讲死锁
- [C++][basic] 讲讲虚拟内存
- [C++][basic] 什么是系统调用
- [C++][advanced] 系统调用会发生栈切换吗（用户态→内核态上下文切换需要切换栈）
- [C++][intermediate] 死锁，线程同步
- [C++][intermediate] 进程崩溃和线程崩溃有什么区别
- [C++][intermediate] 进程访问的内存地址是实际的真实的内存地址吗
- [C++][intermediate] 有没有使用过多线程编程

### 编译与底层
- [C++][basic] 编译语言与非编译语言的区别
- [C++][basic] C++ 编译过程
- [C++][basic] 静态链接库和动态链接库的区别
- [C++][advanced] 动态链接库能被多个进程共享吗（代码段共享，数据段独立）
- [C++][advanced] 动态链接库分配的内存属于哪个进程（属于调用进程的堆空间）

## C#

### 值类型与引用类型
- [C#][basic] 值类型和引用类型的区别
- [C#][basic] struct 和 class 的区别
- [C#][basic] string 是值类型还是引用类型，如何避免 GC
- [C#][basic] C# 的堆和栈
- [C#][basic] static 和 const 的区别
- [C#][basic] 装箱 / 拆箱
- [C#][intermediate] 结构体是否可以继承 / 实现接口？
- [C#][intermediate] 把一个实现接口的结构体实例赋值给接口变量可以吗？如果可以会产生什么问题？
- [C#][intermediate] 一个值类型可以存储在堆上吗

### 委托与事件
关联: DesignPatterns
- [C#][basic] 委托和事件的关系，如何用 Action 编写一个简单的事件订阅系统
- [C#][basic] 你对 C# 的委托理解
- [C#][intermediate] 委托和事件的区别是什么？在实际项目中如何选择使用
- [C#][intermediate] 委托怎么删除某个方法

### GC 与内存管理
关联: C++ · Unity · Performance · DesignPatterns
- [C#][basic] C# GC 的触发机制和常见优化手段
- [C#][basic] 内存泄漏有了解过吗？怎么会产生内存泄漏？
- [C#][advanced] C# GC 的分代回收机制（0/1/2 三代，存活升级），大对象堆（LOH）单独管理、回收频率低
- [C#][intermediate] 假如有一个算法需要多次生成数组（每个 ~20 元素），如何避免频繁 GC
- [C#][intermediate] GC 触发与实践中怎么避免？
- [C#][intermediate] C# 的 GC 是什么，平时有什么编码习惯可以减少 GC
- [C#][intermediate] C# 非托管内存
- [C#][intermediate] 如果对象 A 和对象 B 相互依赖并且确定要被 GC 收集，会发生什么
- [C#][advanced] GC 原理，Unity GC 和 C# GC 有什么不同，循环引用，可达性分析，举例说明哪些场景能被 GC 清除

### 泛型与集合
关联: Algorithms
- [C#][basic] 说说数组和列表的区别
- [C#][basic] C# 的 array 和 list 区别，LinkedList、Stack、Dictionary
- [C#][intermediate] 泛型委托使用的方法
- [C#][advanced] C# 中 List 的底层实现，增删改的时间复杂度，不保证顺序时怎么优化删除
- [C#][intermediate] C# List 和 C++ vector 扩容区别：C# 不立即释放原数组（依赖 GC），C++ 立即 delete
- [C#][intermediate] C# Dictionary 对标 C++ unordered_map（哈希表 O(1)），C++ map 为红黑树 O(logn)
- [C#][advanced] Unity 字典 Dictionary 的底层实现
- [C#][advanced] StringBuilder 底层是怎么实现拼接的

### 接口与抽象类
关联: C++
- [C#][basic] 接口与抽象类的区别

### 反射
关联: Unity
- [C#][advanced] C# 反射的原理，怎么在实际项目中使用

## Lua

> Lua 常用于游戏热更新，与 Unity 深度绑定

### 闭包与 upvalue
- [Lua][basic] Lua 闭包的概念（函数 + 环境引用）
- [Lua][intermediate] Lua 闭包的实现机制（upvalue，open 状态引用栈变量、close 状态拷贝到自身结构体）

### 元表与元方法
- [Lua][basic] 元表的作用和常见元方法（__index、__add、__tostring 等）
- [Lua][intermediate] Lua 如何用 table + 元表实现面向对象（__index 实现继承，重写元方法实现多态）

## Unity

### 生命周期
- [Unity][basic] Unity 生命周期
- [Unity][basic] Awake 和 Start 的区别
- [Unity][intermediate] 为什么 Awake 访问对象会是 null
- [Unity][intermediate] 如何解决初始化顺序问题

### 协程
关联: C++ · Unity
- [Unity][basic] 协程是什么？它和多线程有什么本质区别？
- [Unity][basic] 协程会在什么时候执行
- [Unity][basic] return null 和 return 0 的区别是什么
- [Unity][basic] 协程套协程的应用场景是什么
- [Unity][intermediate] Unity 的协程和线程、进程有啥区别？
- [Unity][intermediate] 100 个协程被挂起，现在有 10 个协程满足条件，应该先执行哪一个

### UGUI
关联: DesignPatterns
- [Unity][basic] Image 和 RawImage 的区别
- [Unity][basic] RectTransform 和 Transform 的区别
- [Unity][basic] 你比较常用的 UGUI 组件是什么？
- [Unity][basic] 手机不同型号分辨率不同，怎么保障 UI 一直维持在正确位置？图片呢？
- [Unity][basic] UGUI 锚点的作用（基于父对象的相对定位，影响位置计算和自适应）
- [Unity][advanced] UGUI 的理解（底层 / 怎么用）
- [Unity][intermediate] UGUI 如何从屏幕点击找到目标 UI，并触发对应的事件回调？
- [Unity][intermediate] Mask 和 RectMask2D 的区别
- [Unity][intermediate] UGUI 中的 Mask 遮罩是怎么实现的
- [Unity][intermediate] UGUI 重绘
- [Unity][intermediate] Text 和 TextMeshPro 的区别是什么？TextMeshPro 是如何渲染一个汉字的？
- [Unity][intermediate] 动态循环列表是怎么实现的？为什么要用？有什么优点？

### UI 优化
- [Unity][basic] UI 为什么要分多个 Canvas
- [Unity][basic] 一百个小兵一百个血条，只有一个小兵在动，为什么不把血条分在 100 个 Canvas 下实现完全动静分离
- [Unity][basic] 比如说有个 UI 会一直播放缩放效果，很多时候会把它单独拆成一个 Canvas，为什么
- [Unity][intermediate] UGUI 优化的方法
- [Unity][advanced] UI 合批条件：不能被打断、不能穿插、要一个图集
- [Unity][advanced] UI 元素重叠（图片+文字）会打断合批，增加 DrawCall
- [Unity][intermediate] UI Rebuild 优化：减少 Canvas 网格重新构建，避免 CPU 频繁计算
- [Unity][intermediate] 一个复杂的 UI 场景里，两个静态 UI 之间有很多动态 UI 且有遮挡，按动静分离是不是要打很多子 Canvas

### 物理系统
关联: Graphics · GameDesign
- [Unity][basic] Collider 和 Trigger 的区别
- [Unity][basic] 如何使用 2D 射线检测到一个玩家
- [Unity][basic] 如何实现检测碰撞
- [Unity][intermediate] 在 2D AI 物理移动时，为什么通常将逻辑写在 FixedUpdate 而不是 Update 中
- [Unity][intermediate] FixedUpdate 是如何执行的？如果 FixedUpdate 的间隔特别短，如何保证严格根据物理时间执行
- [Unity][intermediate] 高速移动下的物体，如何避免穿模
- [Unity][intermediate] Unity 物理系统的原理
- [Unity][advanced] 射线检测的原理，如何自己实现

### 资源管理与 AB 包
关联: C# · Performance · GameDesign
- [Unity][basic] 资源加载的方法
- [Unity][basic] 同步加载和异步加载的区别
- [Unity][intermediate] AB 包（打包注意什么、加载卸载要注意什么、引用计数）
- [Unity][intermediate] Unity 预制体记录资源引用的方式
- [Unity][intermediate] 打包时如何获取到资源在哪个 AB 上面
- [Unity][intermediate] 读取 AB 时，如何知道资源属于哪个 AB
- [Unity][intermediate] AB 包的颗粒度是怎么拆分的
- [Unity][intermediate] 同步加载和异步加载都会产生内存方面的问题，怎么优化？异步产生的内存用什么方式释放
- [Unity][intermediate] Unity 打包的流程和注意事项（AssetBundle 构建、资源冗余如何处理）
- [Unity][intermediate] Unity 什么操作会产生大量 GC
- [Unity][advanced] 类似 AssetBundle，什么操作会产生内存泄漏

### 合批与渲染优化
关联: Graphics · Performance · DesignPatterns
- [Unity][basic] 图集是怎么分类的？
- [Unity][basic] 静态图集和动态图集的区别是什么
- [Unity][advanced] 介绍一下 UI 合批
- [Unity][advanced] 静态 / 动态合批及条件（动态小物体，不超过 300 顶点）
- [Unity][advanced] 合批（静态 / 动态 / UI）

### 动画系统
- [Unity][basic] Animator 和 Animation 的区别
- [Unity][intermediate] Unity 动画系统的原理
- [Unity][intermediate] Animation 和 Animator 的区别，在只有几个简单动画切换情况下哪种性能更好，为什么
- [Unity][intermediate] Unity 的 Animator 中的动画会全部加载到内存中吗？怎么优化
- [Unity][intermediate] Playable 相关

### 寻路与 NavMesh
关联: Algorithms · GameDesign
- [Unity][basic] NavMesh 是离线状态下烘焙好寻路网格的，遇到移动的障碍物如何让 NPC 不撞墙
- [Unity][intermediate] 假设有两层楼，二楼有一个洞，如何让 NPC 从洞掉到一楼还能继续正常寻路
- [Unity][intermediate] Unity Navigation 寻路的原理

### ScriptableObject
关联: C#
- [Unity][basic] 什么是 ScriptableObject？相比于在 Prefab 的 MonoBehaviour 面板上直接配置数值有什么优势
- [Unity][intermediate] ScriptableObject 的优劣势，什么情况下用，什么情况下不用

### 碰撞检测
关联: Graphics · Algorithms
- [Unity][basic] AABB 包围盒和 OBB 包围盒的区别，在 Unity 中如何使用它们进行碰撞检测
- [Unity][basic] 除了 AABB 和 OBB 还有什么碰撞检测方式？优缺点？适合什么情况
- [Unity][advanced] 在 Unity 中实现一个简单的碰撞检测系统，要求能检测球体、盒子、胶囊等碰撞体并处理响应

### JobSystem / Burst / ECS
关联: Performance
- [Unity][advanced] JobSystem
- [Unity][advanced] Burst
- [Unity][advanced] GPU Instancing，JobSystem，Burst，Drawcall 具体优化了多少？适合什么场景？依据什么判断的
- [Unity][advanced] ECS 架构的原理，Component 在内存中的布局方式

### 摄像机
关联: Graphics
- [Unity][intermediate] 在 3D 角色到墙角后，怎么调试可以让摄像机不被挤到外面或穿模
- [Unity][intermediate] 摄像机避开障碍物的实现

### 技能与系统设计
- [Unity][advanced] 注：原「Unity 中的 Skill（技能系统）通常如何设计和实现」已归入 GameDesign

## Graphics

### 渲染管线
关联: Unity
- [Graphics][basic] 渲染管线的流程
- [Graphics][basic] 渲染管线，光栅化后输出的是什么
- [Graphics][basic] 图形渲染管线的各个阶段是什么？每个阶段的作用是什么
- [Graphics][basic] 什么是渲染管线？Unity 的 SRP 是什么？与传统渲染管线有什么区别
- [Graphics][basic] 什么是双缓存
- [Graphics][basic] 为什么有了 VAO 和 VBO 之后还有 IBO
- [Graphics][basic] 光栅化流程
- [Graphics][advanced] CPU 和 GPU 间的通信
- [Graphics][advanced] 渲染管线的各阶段在 Unity 中是如何实现的

### 光照模型
- [Graphics][basic] 图形学中常见的光照模型
- [Graphics][basic] 经典光照模型（漫反射-兰伯特/半兰伯特，高光反射-Phong/Blinn-Phong）与现代 PBR 的区别
- [Graphics][basic] Blinn-Phong 光照模型
- [Graphics][basic] Phong 光照模型和 Blinn-Phong 的区别是什么？为什么 Blinn-Phong 更快
- [Graphics][basic] 光照模型

### PBR
关联: Unity
- [Graphics][basic] 辐射度量学的基本概念
- [Graphics][basic] BRDF 的定义及作用
- [Graphics][basic] 渲染方程
- [Graphics][basic] 反射方程
- [Graphics][basic] PBR 基础理念概括，PBR 的基本概念，BRDF
- [Graphics][advanced] PBR 的原理，金属度
- [Graphics][advanced] PBR 光照模型的核心原理

### 阴影
- [Graphics][advanced] 阴影（Light Map、Shadow Map 原理）

### 抗锯齿
- [Graphics][basic] 锯齿产生的原因
- [Graphics][basic] SSAA、MSAA、FXAA
- [Graphics][basic] MSAA 的原理
- [Graphics][basic] 什么是抗锯齿？常见算法有哪些？优缺点是什么

### 变换与坐标
关联: Unity
- [Graphics][basic] 向量点乘、叉乘相关
- [Graphics][basic] MVP 变换矩阵
- [Graphics][basic] MVP 矩阵的作用及推导
- [Graphics][basic] 如何解决屏幕 2D 点击坐标转换成 3D 世界坐标的问题
- [Graphics][intermediate] 欧拉角、四元数、旋转矩阵的区别和联系

### 深度测试
- [Graphics][basic] 什么是深度测试？在渲染管线的哪个阶段进行
- [Graphics][basic] 深度测试是在什么阶段实现的
- [Graphics][intermediate] Early-Z 什么时候会失效

### 透明混合
- [Graphics][basic] 透明混合
- [Graphics][intermediate] 如果要实现半透明的话 Shader 代码怎么写

### 前向 / 延迟渲染
- [Graphics][basic] 前向渲染和延迟渲染的区别、各自优缺点、适用场景
- [Graphics][intermediate] 延迟渲染的原理、优缺点

### 光线追踪
- [Graphics][advanced] 光线追踪是什么？原理？与传统光栅化对比的优缺点？游戏中的应用场景

### 几何与检测
关联: Unity
- [Graphics][basic] AABB 包围盒和 OBB 包围盒的区别
- [Graphics][intermediate] 判断点在三角形内（叉积、重心坐标、面积法）
- [Graphics][intermediate] 判断点是否在三角形内部
- [Graphics][advanced] 射线检测的原理，如何自己实现

### 法线贴图
- [Graphics][basic] 什么是法线贴图？它是如何工作的？为什么通常看起来是蓝色的
- [Graphics][intermediate] 法线贴图（法线怎么存的、为什么多为蓝色）

### 其他
- [Graphics][basic] 什么是 Mipmap？如何工作？为什么能提高渲染性能和图像质量？Unity 中如何生成和使用

## GameAlgorithms

### A* 与寻路
关联: Unity · GameDesign
- [GameAlgorithms][basic] 游戏寻路中常用哪些最短路径算法？
- [GameAlgorithms][intermediate] A* 如何使用已走距离和预估距离选择下一个节点？
- [GameAlgorithms][intermediate] A* 在什么条件下能够找到最短路径？
- [GameAlgorithms][advanced] A* 与流场寻路分别适合什么规模和类型的场景？

### 空间划分
关联: Performance
- [GameAlgorithms][intermediate] 如何快速找出一定半径内的游戏对象？
- [GameAlgorithms][intermediate] 四叉树和八叉树分别适合划分什么空间？
- [GameAlgorithms][advanced] 分离轴定理（SAT）如何判断两个凸多面体是否相交？
- [GameAlgorithms][advanced] SAT 与 GJK 碰撞检测算法各有什么特点？

## Networking

### 游戏网络传输
关联: GameDesign
- [Networking][intermediate] 游戏中的登录、聊天和战斗同步应如何选择 TCP 或 UDP？
- [Networking][advanced] 一个轻量级可靠 UDP 协议需要实现哪些机制？

### 弱网与可靠性
关联: GameDesign
- [Networking][intermediate] 游戏客户端如何处理丢包、乱序和网络抖动？
- [Networking][intermediate] 多次重传仍然失败时，客户端应如何恢复连接和游戏状态？

## DesignPatterns

### 观察者模式
关联: C# · Unity
- [DesignPatterns][basic] 了解哪些设计模式
- [DesignPatterns][intermediate] 观察者模式什么时候使用、怎么使用、方法封装使用哪些 API
- [DesignPatterns][intermediate] 观察者和单例，优缺点，在项目中的应用

### 单例模式
- [DesignPatterns][intermediate] 观察者和单例，优缺点，在项目中的应用
- [DesignPatterns][intermediate] 单例模式有什么缺点

### 享元模式
关联: Unity
- [DesignPatterns][intermediate] 享元模式怎么实现
- [DesignPatterns][intermediate] 享元模式的其他数据存在哪里

### 对象池
关联: C# · Performance
- [DesignPatterns][intermediate] 对象池要提供哪些接口

### MVC / MVVM
关联: C# · Unity
- [DesignPatterns][basic] MVC
- [DesignPatterns][intermediate] MVC 与 MVVM 区别
- [DesignPatterns][intermediate] MVVM 怎么做到 UI 绑定的

### 工厂模式
- [DesignPatterns][intermediate] 工厂模式的使用场景和实现方式

### 事件系统
关联: C#
- [DesignPatterns][basic] 简单说一下你们的事件管理是怎么做的
- [DesignPatterns][intermediate] 数据驱动

## GameDesign

### FSM 与行为树
关联: Unity · Algorithms
- [GameDesign][basic] 介绍一下有限状态机
- [GameDesign][basic] 有限状态机的好处：同一时间单一状态，节点跳转逻辑清晰，增删节点方便
- [GameDesign][intermediate] FSM 和行为树的差异，实现简单的巡逻保安 AI 会选择什么模式
- [GameDesign][intermediate] 多层级 FSM

### 攻击判定
关联: Networking
- [GameDesign][basic] 获取攻击目标的方法是怎样的
- [GameDesign][intermediate] 两种近战攻击判定机制：碰撞器检测 vs 帧动画关键帧范围检测，优缺点
- [GameDesign][intermediate] 如果攻击判定依赖帧实现，网络波动导致攻击丢失怎么办
- [GameDesign][intermediate] 如果实现类似《空洞骑士》里面怪物遇到墙壁或走到平台边缘掉头，实现方法是什么

### 背包系统
- [GameDesign][intermediate] 背包系统的实现
- [GameDesign][intermediate] 背包中使用了一个物品的逻辑

### Buff 系统
- [GameDesign][intermediate] Buff 系统怎么设计

### 防作弊
关联: Networking
- [GameDesign][intermediate] 如果有人用外挂篡改客户端数据，怎么保证外挂无法得逞

### 场景与内存
关联: Unity
- [GameDesign][intermediate] 一个跑酷游戏不断生成场景，怎么设置让内存不崩溃

### 技能系统
- [GameDesign][advanced] 技能系统通常如何设计和实现

### 大世界
关联: Unity
- [GameDesign][advanced] 大世界中应该怎么去做碰撞检测

### 帧同步与状态同步
关联: Networking · Unity
- [GameDesign][advanced] 帧同步和状态同步
- [GameDesign][advanced] 帧同步和状态同步向服务器端发送的内容

## Performance

### DrawCall 优化
关联: Unity
- [Performance][advanced] DrawCall 优化的方法
- [Performance][intermediate] 一个游戏场景中有一百个人，要怎么渲染才能不卡顿
- [Performance][advanced] 战斗场景性能排查流程：Profiler 定位热点 → 针对性优化（渲染/物理/CPU）

### CPU / GPU 瓶颈
关联: Unity · C#
- [Performance][basic] 导致游戏卡顿的因素有哪些？如何定位和解决
- [Performance][advanced] 游戏开发中常见的 CPU 瓶颈原因
- [Performance][intermediate] 我们要上线一个手游，在低端机上运行会发热，怎么解决

### GC 优化
关联: C# · DesignPatterns
- [Performance][intermediate] Lua GC

### 场景管理
关联: Algorithms · Unity
- [Performance][advanced] 碰撞检测优化：BVH / 空间划分（八叉树）
- [Performance][advanced] CPU 预裁剪：不提交视锥体外物体的 DrawCall




