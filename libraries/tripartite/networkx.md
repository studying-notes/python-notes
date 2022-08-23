---
date: 2022-08-23T15:10:51+08:00  # 创建日期
author: "Rustle Karl"  # 作者

title: "Networkx 复杂网络关系分析"  # 文章标题
url:  "posts/python/libraries/tripartite/networkx"  # 设置网页永久链接
tags: [ "python", "networkx" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

> https://github.com/networkx/networkx

## 文档

https://networkx.org/documentation/latest/tutorial.html

## 安装

```shell
pip install networkx
```

### 最短路径示例

```python
import networkx as nx

G = nx.Graph()

G.add_edge("A", "B", weight=4)
G.add_edge("B", "D", weight=2)
G.add_edge("A", "C", weight=3)
G.add_edge("C", "D", weight=4)

nx.shortest_path(G, "A", "D", weight="weight")
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


