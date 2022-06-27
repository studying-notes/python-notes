---
date: 2022-04-08T21:33:14+08:00
author: "Rustle Karl"

title: "shlex - 简单的词法分析"
url:  "posts/python/libraries/standard/shlex"  # 永久链接
tags: [ "python"]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

https://docs.python.org/zh-cn/3/library/shlex.html

shlex 类可用于编写类似 Unix shell 的简单词法分析程序。通常可用于编写“迷你语言”（如 Python 应用程序的运行控制文件）或解析带引号的字符串。

> shlex 模块 仅适用于 Unix shell。

```shell
command_line = "ping -c 1 www.google.com"
print(shlex.split(command_line))
```

```python
from shlex import join
print(join(['echo', '-n', 'Multiple words']))
```


## 二级

### 三级

```python

```

```shell

```


## 二级

### 三级

```python

```

```shell

```


## 二级

### 三级

```python

```

```shell

```


## 二级

### 三级

```python

```

```shell

```


