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
sys.base_exec_prefix == sys.base_prefix
```

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
