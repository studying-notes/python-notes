---
date: 2022-05-11T15:54:36+08:00
author: "Rustle Karl"

title: "platform 获取底层平台的标识数据"
url:  "posts/python/libraries/standard/os/platform"  # 永久链接
tags: [ "python" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

> https://docs.python.org/3/library/platform.html
> https://docs.python.org/zh-cn/3/library/platform.html

```python
import platform
```

## 二进制码文件位架构和链接格式

```python
platform.architecture()
```

## 机器类型

```python
platform.machine()
```

## 计算机的网络名称

```python
platform.node()
```

## 标识底层平台的字符串

```python
platform.platform()
```

输出信息的目标是“人类易读”而非机器易解析。 它在不同平台上可能看起来不一致，这是有意为之的。

## 处理器名称

```python
platform.processor()
```

许多平台都不提供此信息或是简单地返回与 machine() 相同的值。

## Python 编译代码和日期

```python
platform.python_build()
```

## 用于编译 Python 的编译器

```python
platform.python_compiler()
```

## 标识 Python 实现的字符串

```python
platform.python_implementation()
```

可能的返回值有: 'CPython', 'IronPython', 'Jython', 'PyPy'。

## Python 版本

```python
platform.python_version()
```

## Python 版本字符串元组

```python
platform.python_version_tuple()
```

## 系统发行信息

```python
platform.release()
```

## 系统平台的名称

```python
platform.system()
```

## 系统的发布版本信息

```python
platform.version()
```

## 平台信息集合

包含六个属性的 namedtuple(): system, node, release, version, machine 和 processor。

```python
platform.uname()
```
