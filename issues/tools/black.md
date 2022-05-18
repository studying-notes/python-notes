---
date: 2022-05-10T11:18:03+08:00
author: "Rustle Karl"

title: "black 格式化中的问题"
url:  "posts/python/issues/tools/black"  # 永久链接
tags: [ "python"]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

## GitWildMatchPatternError

```
ImportError: cannot import name 'GitWildMatchPatternError' from 'pathspec.atterns.gitwildmatch' 
```

```shell
pip uninstall pathspec -y
```

```shell
pip install pathspec
```
