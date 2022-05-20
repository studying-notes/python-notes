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

- [记录器 Logger 对象](#记录器-logger-对象)
  - [logging.Logger](#logginglogger)
    - [propagate](#propagate)
    - [setLevel(level)](#setlevellevel)
    - [isEnabledFor(level)](#isenabledforlevel)
    - [getEffectiveLevel()](#geteffectivelevel)
    - [getChild(suffix)](#getchildsuffix)
    - [debug(msg, *args, **kwargs)](#debugmsg-args-kwargs)
    - [makeRecord(name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None)](#makerecordname-level-fn-lno-msg-args-exc_info-funcnone-extranone-sinfonone)
  - [日志级别](#日志级别)
- [处理器 Handler 对象](#处理器-handler-对象)
- [格式器 Formatter 对象](#格式器-formatter-对象)
- [过滤器 Filter 对象](#过滤器-filter-对象)
- [LogRecord 属性](#logrecord-属性)
  - [时间日期格式化符号](#时间日期格式化符号)
  - [计算毫秒](#计算毫秒)
- [线程安全](#线程安全)
- [与警告模块集成](#与警告模块集成)

## 记录器 Logger 对象

注意永远不要直接实例化记录器，应当通过模块级别的函数 logging.getLogger(name) 。多次使用相同的名字 name 调用 getLogger() 会一直返回相同的 Logger 对象的引用。

name 一般是句点分割的层级值, 像 ``foo.bar.baz`` (尽管也可以只是普通的 foo)。层次结构列表中位于下方的记录器是列表中较高位置的记录器的子级。例如，有个名叫 foo 的记录器，而名字是 foo.bar，foo.bar.baz，和 foo.bam 的记录器都是 foo 的子级。

记录器的名字分级类似 Python 包的层级，如果使用建议的结构 `logging.getLogger(__name__)` 在每个模块的基础上组织记录器，则与之完全相同。这是因为在模块里，`__name__` 是该模块在 Python 包命名空间中的名字。

### logging.Logger

#### propagate 

如果这个属性为真，**记录到这个记录器的事件**除了会**发送到此记录器的所有处理程序**外，还会传递给**更高级别（祖先）记录器的处理器**，以及其他任何关联到这个记录器的处理器。消息会直接传递给祖先记录器的处理器 —— 不考虑祖先记录器的级别和过滤器。

如果为假，记录消息将不会传递给当前记录器的祖先记录器的处理器。

构造器将这个属性初始化为 True。

如果将一个处理器附加到一个记录器和其一个或多个祖先记录器，它**可能发出多次相同的记录**。

通常不需要将一个处理器附加到一个以上的记录器上，如果将它附加到记录器层次结构中最高的适当记录器上，则它将看到所有后代记录器记录的所有事件，前提是它们的传播设置保留为 True。

一种常见的方案是仅将处理器附加到根记录器，通过传播来处理其余部分。

#### setLevel(level)

给记录器设置阈值为 level 。日志等级小于 level 会被忽略（不发给任何处理器）。

严重性为 level 或更高的日志消息将由该记录器的任何一个或多个处理器发出，除非将处理器的级别设置为比 level 更高的级别。

创建记录器时，级别默认设置为 NOTSET （当记录器是根记录器时，将处理所有消息；如果记录器不是根记录器，则将委托给父级）。

但标准库的根记录器的默认级别为 WARNING 。

委派给父级的意思是如果一个记录器的级别设置为 NOTSET，将遍历其祖先记录器，直到找到级别不是 NOTSET 的记录器，或者到根记录器为止。

如果发现某个父级的级别不是 NOTSET ，那么该父级的级别将被视为发起搜索的记录器的有效级别，并用于确定如何处理日志事件。

如果搜索到达根记录器，并且其级别为 NOTSET，则将处理所有消息。否则，将使用根记录器的级别作为有效级别。

#### isEnabledFor(level)

指示此记录器是否将处理级别为 level 的消息。此方法首先检查由 logging.disable(level) 设置的模块级的级别，然后检查由 getEffectiveLevel() 确定的记录器的有效级别。

#### getEffectiveLevel()

指示此记录器的有效级别。如果通过 setLevel() 设置了除 NOTSET 以外的值，则返回该值。否则，将层次结构遍历到根，直到找到除 NOTSET 以外的其他值，然后返回该值。返回的值是一个整数，通常为 logging.DEBUG、 logging.INFO 等等。

#### getChild(suffix)

返回由后缀确定的该记录器的后代记录器。 因此，`logging.getLogger('abc').getChild('def.ghi')` 与 `logging.getLogger('abc.def.ghi')` 将返回相同的记录器。 这是一个便捷方法，当使用如 `__name__` 而不是字符串字面值命名父记录器时很有用。

#### debug(msg, *args, **kwargs)

在此记录器上记录 DEBUG 级别的消息。 msg 是消息格式字符串，而 args 是用于字符串格式化操作合并到 msg 的参数。（这意味着您可以在格式字符串中使用关键字以及单个字典参数。）当未提供 args 时，不会对 msg 执行 ％ 格式化操作。

在 kwargs 中会检查四个关键字参数： exc_info ，stack_info ，stacklevel 和 extra 。

如果 exc_info 的求值结果不为 false ，则它将异常信息添加到日志消息中。如果提供了一个异常元组（按照 sys.exc_info() 返回的格式）或一个异常实例，则它将被使用；否则，调用 sys.exc_info() 以获取异常信息。

第二个可选关键字参数是 stack_info，默认为 False。如果为 True，则将堆栈信息添加到日志消息中，包括实际的日志调用。请注意，这与通过指定 exc_info 显示的堆栈信息不同：**前者是从堆栈底部到当前线程中的日志记录调用的堆栈帧**，而**后者是在搜索异常处理程序时，跟踪异常而打开的堆栈帧的信息**。

您可以独立于 exc_info 来指定 stack_info，例如，即使在未引发任何异常的情况下，也可以显示如何到达代码中的特定点。堆栈帧在标题行之后打印：

```
Stack (most recent call last):
```

这模仿了显示异常帧时所使用的 Traceback (most recent call last): 。

第三个可选关键字参数是 stacklevel ，默认为 1 。如果大于 1 ，则在为日志记录事件创建的 LogRecord 中计算行号和函数名时，将跳过相应数量的堆栈帧。可以在记录帮助器时使用它，以便记录的函数名称，文件名和行号不是帮助器的函数/方法的信息，而是其调用方的信息。此参数是 warnings 模块中的同名等效参数。

第四个关键字参数是 extra ，传递一个字典，该字典用于填充为日志记录事件创建的、带有用户自定义属性的 LogRecord 中的 `__dict__` 。然后可以按照需求使用这些自定义属性。例如，可以将它们合并到已记录的消息中：

```python
FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
logger = logging.getLogger('tcpserver')
logger.warning('Protocol problem: %s', 'connection reset', extra=d)
```

输出类似于

```
2006-02-08 22:20:02,165 192.168.0.1 fbloggs  Protocol problem: connection reset
```

extra 中传入的字典的键不应与日志系统使用的键冲突。

如果在已记录的消息中使用这些属性，则需要格外小心。例如，在上面的示例中，Formatter 已设置了格式字符串，其在 LogRecord 的属性字典中键值为 “clientip” 和 “user”。如果缺少这些内容，则将不会记录该消息，因为会引发字符串格式化异常。因此，在这种情况下，您始终需要使用 extra 字典传递这些键。

尽管这可能很烦人，但此功能旨在用于特殊情况，例如在多个上下文中执行相同代码的多线程服务器，并且出现的有趣条件取决于此上下文（例如在上面的示例中就是远程客户端IP地址和已验证用户名）。在这种情况下，很可能将专门的 Formatter 与特定的 Handler 一起使用。

info/warning/error/critical/log/exception 等参数同上。

#### makeRecord(name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None)

这是一种工厂方法，可以在子类中对其进行重写以创建专门的 LogRecord 实例。

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

```python
class logging.Filter()
```

```python
# 是否要过滤指定的记录
logging.Filte.filter(record)
```

请注意**关联到处理器**的过滤器会在事件由处理器发出之前被查询，而**关联到日志记录器**的过滤器则会在有事件被记录的的任何时候（使用 debug(), info() 等等）**在将事件发送给处理器之前被查询**。 这意味着由后代日志记录器生成的事件将不会被父代日志记录器的过滤器设置所过滤，除非该过滤器也已被应用于后代日志记录器。

有点晕了，简而言之，后代日志记录器-> 后代日志记录器过滤器->后代/父代日志处理器->后代/父代日志处理器过滤器。这个过程中不会经过父代日志记录器的过滤器。

你实际上不需要子类化 Filter ：你可以传入任何一个包含有相同语义的 filter 方法的实例。

尽管过滤器主要被用来构造比层级更复杂的规则以过滤记录，但它们可以查看由它们关联的处理器或记录器所处理的每条记录：当你想要执行统计特定记录器或处理器共处理了多少条记录，或是在所处理的 LogRecord 中添加、修改或移除属性这样的任务时该特性将很有用处。 显然改变 LogRecord 时需要相当小心，但将上下文信息注入日志确实是被允许的。

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
