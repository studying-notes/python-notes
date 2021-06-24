---
date: 2020-10-08T09:22:29+08:00  # 创建日期
author: "Rustle Karl"  # 作者
# cover: "/examples/imgs"  # 封面图，可以是相对于 static 的路径，也可以是相对于当前的路径

# 文章
title: "Python 遍历文件夹下所有文件及目录"  # 文章标题
description: "递归遍历目录、遍历文件夹中的所有子文件夹及子文件"
url:  "posts/2020/10/08/oswalk"  # 设置网页链接，默认使用文件名
tags: [ "python", "os"]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

# 章节
weight: 20 # 文章在章节中的排序优先级，正序排序
chapter: false  # 将页面设置为章节

index: true  # 文章是否可以被索引
draft: true  # 草稿
toc: true  # 是否自动生成目录
---

```python
os.walk(top[, topdown=True[, onerror=None[, followlinks=False]]])
```

- 返回 3 元组 (dirpath, dirnames, filenames)
- top – 根目录
- topdown – 可选，为 True 或者没有指定, 目录自上而下遍历；如果 topdown 为 False, 目录自下而上遍历
- onerror – 可选，一个函数，调用时有一个参数, 一个 OSError 实例，报告这错误后，继续 walk, 或者抛出 exception 终止 walk
- followlinks – 设置为 true，则通过软链接访问目录。

## 示例

```python

```

```python

```

```python

```

```python

```
