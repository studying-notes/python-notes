---
date: 2021-01-16T12:46:32+08:00  # 创建日期
author: "Rustle Karl"  # 作者

title: "Python Enlighten 进度条"  # 文章标题
# description: "文章描述"
url:  "posts/py/libraries/tripartite/enlighten"  # 设置网页永久链接
tags: [ "python", "进度条" ]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类


# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

```python
import time
import enlighten

pbar = enlighten.Counter(total=100, desc='Basic', unit='ticks')
for num in range(100):
    time.sleep(0.1)  # Simulate work
    pbar.update()
```

```python
import time
import enlighten

manager = enlighten.get_manager()
ticks = manager.counter(total=100, desc='Ticks', unit='ticks')
tocks = manager.counter(total=20, desc='Tocks', unit='tocks')

for num in range(100):
    time.sleep(0.1)  # Simulate work
    print(num)
    ticks.update()
    if not num % 5:
        tocks.update()

manager.stop()
```


```python

```


```python

```


```python

```


```python

```


```python

```


