---
date: 2022-05-12T11:32:15+08:00
author: "Rustle Karl"

title: "traceback 打印或读取堆栈的跟踪信息"
url:  "posts/python/libraries/standard/runtime/traceback"  # 永久链接
tags: [ "python" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

> https://docs.python.org/3/library/traceback.html
> https://docs.python.org/zh-cn/3/library/traceback.html

该模块提供了一个标准接口来提取、格式化和打印 Python 程序的堆栈跟踪结果。它完全模仿Python 解释器在打印堆栈跟踪结果时的行为。当您想要在程序控制下打印堆栈跟踪结果时，例如在“封装”解释器时，这是非常有用的。

这个模块使用 traceback 对象 —— 这是存储在 sys.last_traceback 中的对象类型变量，并作为 sys.exc_info() 的第三项被返回。

## traceback.print_tb

```python
traceback.print_tb(tb, limit=None, file=None)
```

如果*limit* 是正整数，那么从 traceback 对象 "tb" 输出最高 limit 个（从调用函数开始的）栈的堆栈回溯条目；

如果 limit 是负数就输出 `abs(limit)` 个回溯条目；又如果 limit 被省略或者为 None，那么就会输出所有回溯条目。

如果 file 被省略或为 `None` 那么就会输出至标准输出 `sys.stderr` 否则它应该是一个打开的文件或者文件类对象来接收输出。

## traceback.print_exception

```python
traceback.print_exception(exc, /, [value, tb, ]limit=None, file=None, chain=True)
```

打印回溯对象 tb 到 file 的异常信息和整个堆栈回溯。这和 `print_tb()` 比有以下方面不同：

- 如果 tb 不为 None，它将打印头部 `Traceback (most recent call last):`
- 在打印堆栈回溯之后还会打印 exception 类型和值
- 如果 type(value) 是 SyntaxError 并且 value 具有适当的格式，它会打印出现语法错误的行，并用插入符号指示错误的大致位置。

从 Python 3.10 开始，可以将异常对象作为第一个参数传递，而不是传递 value 和 tb。如果提供了 value 和 tb，则忽略第一个参数以提供向后兼容性。

可选的 limit 参数与 print_tb() 的含义相同。如果 chain 为真（默认），那么链式异常（异常的 `__cause__` 或 `__context__` 属性）也将被打印，就像解释器本身在打印未处理的异常时所做的那样。

## traceback.print_exc

```python
traceback.print_exc(limit=None, file=None, chain=True)
```

是以下函数的快捷方式：

```python
print_exception(*sys.exc_info(), limit, file, chain)
```

## traceback.print_last

```python
traceback.print_last(limit=None, file=None, chain=True)
```

是以下函数的快捷方式：

```python
print_exception(sys.last_type, sys.last_value, sys.last_traceback, limit, file, chain)
```

这三个变量并非总是有定义，仅当有异常未处理，且解释器打印了错误消息和堆栈回溯时，才会给它们赋值。它们的预期用途，是**允许交互中的用户导入调试器模块，进行事后调试，而不必重新运行导致错误的命令**。这些变量的含义与上述 exc_info() 返回值的含义相同。

## traceback.print_stack

```python
traceback.print_stack(f=None, limit=None, file=None)
```

如果 limit 为正，则打印最多限制堆栈跟踪条目（从调用点开始）。否则，打印最后的 abs(limit) 条目。如果省略限制或无，则打印所有条目。可选的 f 参数可用于指定要启动的备用堆栈帧。可选的文件参数与 print_tb() 的含义相同。

## traceback.extract_tb

```python
traceback.extract_tb(tb, limit=None)
```

返回一个 StackSummary 对象，该对象表示从 traceback 对象 tb 中提取的“预处理”堆栈跟踪条目列表。它对于堆栈跟踪的替代格式很有用。可选的 limit 参数与 print_tb() 的含义相同。 “预处理”堆栈跟踪条目是一个 FrameSummary 对象，其中包含属性文件名、行号、名称和表示通常为堆栈跟踪打印的信息的行。该行是一个字符串，去掉了前导和尾随空格；如果源不可用，则为无。

## traceback.extract_stack

```python
traceback.extract_stack(f=None, limit=None)
```

从当前堆栈帧中提取原始回溯。返回值的格式与 extract_tb() 的格式相同。可选的 f 和 limit 参数与 print_stack() 的含义相同。

## traceback.format_list

```python
traceback.format_list(extracted_list)
```

给定由 extract_tb() 或 extract_stack() 返回的元组或 FrameSummary 对象列表，返回准备打印的字符串列表。结果列表中的每个字符串对应于参数列表中具有相同索引的项。每个字符串都以换行符结尾；对于源文本行不是 None 的项目，字符串也可能包含内部换行符。

## traceback.format_exception_only

使用 sys.last_value 给定的异常值格式化回溯的异常部分。返回值是一个字符串列表，每个字符串都以换行符结尾。通常，列表包含一个字符串；但是，对于 SyntaxError 异常，它包含几行（打印时）显示有关语法错误发生位置的详细信息。指示发生了哪个异常的消息始终是列表中的最后一个字符串。

从 Python 3.10 开始，可以将异常对象作为第一个参数传递，而不是传递值。如果提供了 value，则忽略第一个参数以提供向后兼容性。

## traceback.format_exception

格式化堆栈跟踪和异常信息。这些参数与 print_exception() 的相应参数具有相同的含义。返回值是一个字符串列表，每个字符串都以换行符结尾，一些包含内部换行符。连接并打印这些行时，将打印与 print_exception() 完全相同的文本。

- traceback.format_exc
- traceback.format_tb
- traceback.format_stack
- traceback.clear_frames

## traceback.walk_stack

```python
traceback.walk_stack(f)
```

从给定帧跟随 f.f_back 走一个堆栈，为每一帧产生帧和行号。如果 f 为 None，则使用当前堆栈。此帮助器与 StackSummary.extract() 一起使用。

## traceback.walk_tb

```python
traceback.walk_tb(tb)
```

tb_next 之后进行回溯，为每一帧产生帧和行号。此帮助器与 StackSummary.extract() 一起使用。
