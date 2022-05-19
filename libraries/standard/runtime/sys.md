---
date: 2022-05-11T14:33:47+08:00
author: "Rustle Karl"

title: "sys 系统特定参数和函数"
url:  "posts/python/libraries/standard/runtime/sys"  # 永久链接
tags: [ "python" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

> https://docs.python.org/3/library/sys.html
> https://docs.python.org/zh-cn/3/library/sys.html

该模块提供对解释器使用或维护的一些变量以及与解释器进行强交互的函数的访问。

## 判断是否运行在虚拟环境中

```python
sys.base_exec_prefix == sys.exec_prefix
# or
sys.base_prefix == sys.prefix
```

exec_prefix 提供特定域的目录前缀，该目录中安装了与平台相关的 Python 文件，默认也是 '/usr/local'。该目录前缀可以在构建时使用 configure 脚本的 --exec-prefix 参数进行设置。

具体而言，所有配置文件（如 pyconfig.h 头文件）都安装在目录 `exec_prefix/lib/pythonX.Y/config` 中，共享库模块安装在 `exec_prefix/lib/pythonX.Y/lib-dynload` 中，其中 X.Y 是 Python 的版本号，如 3.2。

如果在一个 虚拟环境 中，那么该值将在 site.py 中被修改，指向虚拟环境。Python 安装位置仍然可以用 base_exec_prefix 来获取。

在 site.py 运行之前， Python 启动的时候被设置为跟 exec_prefix 同样的值。如果不是运行在 虚拟环境 中，两个值会保持相同；如果 site.py 发现处于一个虚拟环境中， prefix 和 exec_prefix 将会指向虚拟环境。然而 base_prefix 和 base_exec_prefix 将仍然会指向基础的 Python 环境（用来创建虚拟环境的 Python 环境）。

## 机器字节序

```python
sys.byteorder
```

## 进入调试器

```python
sys.breakpointhook()
```

## 不产生 .pyc 文件

```python
sys.dont_write_bytecode = True
```

## 指定 .pyc 文件目录

```python
sys.pycache_prefix = /path/to/dir
```

命令行运行参数等价：

```
python -X pycache_prefix=/path/to/dir
```

命令行环境变量参数等价：

```
PYTHONPYCACHEPREFIX
```

## Python 可行性文件绝对路径

```python
sys.executable
```

## 退出程序

> 实际是抛出 SystemExit 异常

```python
sys.exit(0)
```

## 命令行标志的状态

这些属性是只读的。

```python
sys.flags
```

## 解释器当前已分配的内存块数

```python
sys.getallocatedblocks()
```

## 默认字符串编码名称

```python
sys.getdefaultencoding()
```

## 获取文件系统编码格式

```python
sys.getfilesystemencoding()
```

## 当前的递归限制值

```python
sys.getrecursionlimit()
# 设置
sys.setrecursionlimit(10000)
```

## 解释器的“线程切换间隔时间”

```python
sys.getswitchinterval()
# 设置
sys.setswitchinterval(0.5)
```

## 当前正在运行的 Windows 版本

```python
sys.getwindowsversion()
```

platform_version 返回当前操作系统的主要版本、次要版本和编译版本号，而不是为该进程所模拟的版本。 它旨在用于日志记录而非特性检测。

>  platform_version 会从 kernel32.dll 获取版本号，这个版本可能与 OS 版本不同。 请使用 platform 模块来获取准确的 OS 版本号。

## 解释器的版本

```python
sys.hexversion

hex(sys.hexversion) == "0x30a04f0" # 3.10.4
```

## 解释器的实现信息

```python
sys.implementation
```

## 驻留字符串表

```python
sys.intern(string)
```

## 系统最大整数值

```python
sys.maxsize
```

## 原始命令行参数列表

```python
sys.orig_argv
```

## 模块的搜索路径

初始化自环境变量 PYTHONPATH，再加上一条与安装有关的默认路径。

```python
sys.path
```

## 平台标识符

```python
sys.platform
```

linux/win32/cygwin/darwin

### 常用系统判断

> form scapy/consts.py

```python
import platform

WINDOWS_XP = platform.release() == "XP"

from sys import byteorder, platform, maxsize

LINUX = platform.startswith("linux")
OPENBSD = platform.startswith("openbsd")
FREEBSD = "freebsd" in platform
NETBSD = platform.startswith("netbsd")
DARWIN = platform.startswith("darwin")
SOLARIS = platform.startswith("sunos")
WINDOWS = platform.startswith("win32")
BSD = DARWIN or FREEBSD or OPENBSD or NETBSD

IS_64BITS = maxsize > 2**32
BIG_ENDIAN = byteorder == 'big'
```

## 标准输入、标准输出和标准错误

```python
sys.stdin
sys.stdout
sys.stderr
```

程序开始时，这些对象存有 stdin、stderr 和 stdout 的初始值。它们在程序结束前都可以使用，且在需要向实际的标准流打印内容时很有用，无论 sys.std* 对象是否已重定向。

如果实际文件已经被覆盖成一个损坏的对象了，那它也可用于将实际文件还原成能正常工作的文件对象。但是，本过程的最佳方法应该是，在原来的流被替换之前就显式地保存它，并使用这一保存的对象来还原。

```python
sys.__stdin__
sys.__stdout__
sys.__stderr__
```

## 解释器启动时显示的字符串

```python
sys.version
```

一个包含 Python 解释器版本号加编译版本号以及所用编译器等额外信息的字符串。 此字符串会在交互式解释器启动时显示。 请不要从中提取版本信息，而应当使用 version_info 以及 platform 模块所提供的函数。

## 解释器的 C API 版本

```python
sys.api_version
```

## 版本号五部分的元组

```python
sys.version_info
```

## 通过 -X 命令行选项传递的旗标

```python
sys._xoptions
```

## 异常错误

```python
sys.exc_info()
```

本函数返回的元组包含三个值，它们给出当前正在处理的异常的信息。返回的信息仅限于当前线程和当前堆栈帧。

如果当前堆栈帧没有正在处理的异常，则信息将从下级被调用的堆栈帧或上级调用者等位置获取，依此类推，直到找到正在处理异常的堆栈帧为止。

此处的“处理异常”指的是“执行 except 子句”。

任何堆栈帧都只能访问当前正在处理的异常的信息。

如果整个堆栈都没有正在处理的异常，则返回包含三个 None 值的元组。否则返回值为 (type, value, traceback)。它们的含义是：

- type 是正在处理的异常类型（它是 BaseException 的子类）；
- value 是异常实例（异常类型的实例）；
- traceback 是一个 回溯对象，该对象封装了最初发生异常时的调用堆栈。
