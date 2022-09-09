---
date: 2022-09-09T13:34:35+08:00  # 创建日期
author: "Rustle Karl"  # 作者

title: "访问 Windows 注册表"  # 文章标题
url:  "posts/python/libraries/standard/MSWindowsSpecificServices/winreg"  # 设置网页永久链接
tags: [ "python", "winreg" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

> https://docs.python.org/zh-cn/3/library/winreg.html

## 注册表句柄对象

> 即下文的 handle 对象。

该对象封装了 Windows HKEY 对象，对象销毁时会自动关闭。

为确保资源得以清理，可调用 Close() 方法或 CloseKey() 函数。

本模块中的所有注册表函数都会返回注册表句柄对象。

本模块中所有接受注册表句柄对象的注册表函数，也能接受一个整数。

注册表句柄对象支持 `__bool__()` 语义 —— 因此如果当前句柄有效（未关闭或断开连接）：

```python
if handle:
    print("Yes")
```

将会打印出 Yes 。

句柄对象还支持比较语义，因此若多个句柄对象都引用了同一底层 Windows 句柄值，那么比较操作结果将为 True。

句柄对象可转换为整数（如利用内置函数 int()），这时会返回底层的 Windows 句柄值。用 Detach() 方法也可返回整数句柄，同时会断开与 Windows 句柄的连接。

### PyHKEY.Close()

关闭底层的 Windows 句柄。

如果句柄已关闭，不会引发错误。

### PyHKEY.Detach()

断开与 Windows 句柄的连接。

结果为一个整数，存有被断开连接之前的句柄值。如果该句柄已断开连接或关闭，则返回 0。

调用本函数后，注册表句柄将被迅速禁用，但并没有关闭。当需要底层的 Win32 句柄在句柄对象的生命周期之后仍然存在时，可以调用这个函数。

引发一条 审计事件 winreg.PyHKEY.Detach，附带参数 key。

### PyHKEY.__enter__() & PyHKEY.__exit__(*exc_info)

HKEY 对象实现了 `__enter__()` 和 `__exit__()` 方法，因此支持 with 语句的上下文协议：

```python
with OpenKey(HKEY_LOCAL_MACHINE, "foo") as key:
    ...  # work with key
```

在离开 with 语句块时，key 会自动关闭。

## 常用函数

### winreg.CloseKey(hkey)

关闭之前打开的注册表键。参数 hkey 指之前打开的键。

### winreg.CreateKey(key, sub_key)

创建或打开特定的键，返回一个 handle 对象。

key 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

sub_key 是用于命名该方法所打开或创建的键的字符串。

如果 key 是预定义键之一，sub_key 可能会是 None。该情况下，返回的句柄就是传入函数的句柄。

**如果键已经存在，则该函数打开已经存在的该键。**

返回值是所开打键的句柄。如果函数失败，则引发一个 OSError 异常。

引发一个 审计事件 winreg.CreateKey，附带参数 key, sub_key, access。

引发一个 审计事件 winreg.OpenKey/result，附带参数 key。

### winreg.DeleteKey(key, sub_key)

删除指定的键。

key 为某个已经打开的键，或者预定义的 HKEY_* 常量 之一。

sub_key 这个字符串必须是由 key 参数所指定键的一个子项。该值项不可以是 None，同时键也不可以有子项。

该方法不能删除带有子项的键。

如果方法成功，则整个键，包括其所有值项都会被移除。如果方法失败，则引发一个 OSError 异常。

引发一个 审计事件 winreg.DeleteKey，附带参数 key, sub_key, access。

```python

```
