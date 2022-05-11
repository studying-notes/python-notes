---
date: 2022-05-11T16:54:04+08:00
author: "Rustle Karl"

title: "logging 日志系统"
url:  "posts/python/libraries/standard/os/logging"  # 永久链接
tags: [ "python" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

> https://docs.python.org/3/library/logging.html
> https://docs.python.org/zh-cn/3/library/logging.html

- 记录器 Loggers 暴露了应用程序代码直接使用的接口。
- 处理器 Handlers 将日志记录（由记录器创建）发送到适当的目标。
- 格式器 Formatters 指定最终输出中日志记录的样式。
- 过滤器 Filters 提供了更细粒度的功能，用于确定要输出的日志记录。

## 记录器 Logger 对象

注意永远不要直接实例化记录器，应当通过模块级别的函数 logging.getLogger(name) 。多次使用相同的名字 name 调用 getLogger() 会一直返回相同的 Logger 对象的引用。

name 一般是句点分割的层级值, 像 ``foo.bar.baz`` (尽管也可以只是普通的 foo)。层次结构列表中位于下方的记录器是列表中较高位置的记录器的子级。例如，有个名叫 foo 的记录器，而名字是 foo.bar，foo.bar.baz，和 foo.bam 的记录器都是 foo 的子级。

记录器的名字分级类似 Python 包的层级，如果使用建议的结构 `logging.getLogger(__name__)` 在每个模块的基础上组织记录器，则与之完全相同。这是因为在模块里，`__name__` 是该模块在 Python 包命名空间中的名字。

### 日志级别

| 级别 | 数值 |
| :--- | :--- |
| `CRITICAL` | 50 |
| `ERROR` | 40 |
| `WARNING` | 30 |
| `INFO` | 20 |
| `DEBUG` | 10 |
| `NOTSET` | 0 |

## 处理器 Handler 对象

注意不要直接实例化 Handler ；这个类用来派生其他更有用的子类。

## 格式器 Formatter 对象

负责将 LogRecord 转换为可由人或外部系统解释的字符串。基础的 Formatter 允许指定格式字符串。如果未提供任何值，则使用默认值 '%(message)s' ，它仅将消息包括在日志记录调用中。

格式器可以使用格式化字符串来初始化，该字符串利用 LogRecord 的属性 —— 例如上述默认值，用户的消息和参数预先格式化为 LogRecord 的 message 属性后被使用。此格式字符串包含标准的 Python %-s 样式映射键。

## 过滤器 Filter 对象

Filters 可被 Handlers 和 Loggers 用来实现比按层级提供更复杂的过滤操作。 基本过滤器类只允许低于日志记录器层级结构中低于特定层级的事件。 

例如，一个用 'A.B' 初始化的过滤器将允许 'A.B', 'A.B.C', 'A.B.C.D', 'A.B.D' 等日志记录器所记录的事件。 但 'A.BB', 'B.A.B' 等则不允许。 

如果用空字符串初始化，则所有事件都会通过。

### 三级


## LogRecord 属性

| %(name)s | Logger 的名字 |
| ------------------- | ------------------- |
| %(levelno)s | 数字形式的日志级别 |
| %(levelname)s | 文本形式的日志级别 |
| %(pathname)s | 调用日志输出函数的模块的完整路径名。可能没有 |
| %(filename)s | 调用日志输出函数的模块的文件名 |
| %(module)s | 调用日志输出函数的模块名 |
| %(funcName)s | 调用日志输出函数的函数名 |
| %(lineno)d | 调用日志输出函数的语句所在的代码行 |
| %(created)f | 当前时间，用 UNIX 标准的表示时间的浮点数表示 |
| %(relativeCreated)d | 输出日志信息时的，自 Logger 创建以来的毫秒数 |
| %(asctime)s | 字符串形式的当前时间。默认格式是“2003-07-08 16:49:45,896”。逗号后面的是毫秒 |
| %(thread)d | 线程 ID。可能没有 |
| %(threadName)s | 线程名。可能没有 |
| %(process)d | 进程 ID。可能没有 |
| %(message)s | 用户输出的消息 |

### 时间日期格式化符号

- %y 两位数的年份表示（00-99）
- %Y 四位数的年份表示（000-9999）
- %m 月份（01-12）
- %d 月内中的一天（0-31）
- %H 24小时制小时数（0-23）
- %I 12小时制小时数（01-12）
- %M 分钟数（00=59）
- %S 秒（00-59）
- %a 本地简化星期名称
- %A 本地完整星期名称
- %b 本地简化的月份名称
- %B 本地完整的月份名称
- %c 本地相应的日期表示和时间表示
- %j 年内的一天（001-366）
- %p 本地A.M.或P.M.的等价符
- %U 一年中的星期数（00-53）星期天为星期的开始
- %w 星期（0-6），星期天为星期的开始
- %W 一年中的星期数（00-53）星期一为星期的开始
- %x 本地相应的日期表示
- %X 本地相应的时间表示
- %Z 当前时区的名称
- %% %号本身

### 计算毫秒

```python
import datetime
import time

print(
    time.strftime('%Y-%m-%d  %H:%M:%S'),
    datetime.datetime.now().strftime('%f')[:3]
)

print(datetime.datetime.now().strftime('%Y%m%d %H:%M:%S.%f'))
```

## 线程安全

logging 模块的目标是使客户端不必执行任何特殊操作即可确保线程安全。 它通过使用线程锁来达成这个目标；用一个锁来序列化对模块共享数据的访问，并且每个处理程序也会创建一个锁来序列化对其下层 I/O 的访问。

如果你要使用 signal 模块来实现异步信号处理程序，则可能无法在这些处理程序中使用 logging。 这是因为 threading 模块中的锁实现并非总是可重入的，所以无法从此类信号处理程序发起调用。

## 与警告模块集成

captureWarnings() 函数可用来将 logging 和 warnings 模块集成。
