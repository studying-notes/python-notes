---
date: 2022-09-09T14:55:45+08:00  # 创建日期
author: "Rustle Karl"  # 作者

title: "subprocess 子进程管理"  # 文章标题
url:  "posts/python/libraries/standard/ConcurrentExecution/subprocess"  # 设置网页永久链接
tags: [ "python", "subprocess" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

> https://docs.python.org/zh-cn/3/library/subprocess.html

```python
import subprocess
```

## 启动可执行文件

启动资源管理器，不等待命令终止：

```python
subprocess.Popen(
    [
        "explorer.exe",
        ".",
    ]
)
```

启动一个控制台窗口，然后控制台打开另一个控制台，等待命令终止：

```python
p = subprocess.Popen(
    [
        "cmd",
        "/c",
        "start",
        "cmd",
    ]
)

code = p.wait()
```

可以跳出一个独立的控制台窗口，方便调试命令输出。

```python

```
