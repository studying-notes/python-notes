---
date: 2020-12-24T13:57:21+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Python 逆向编译"  # 文章标题
url:  "posts/python/docs/others/decompile"  # 设置网页永久链接
tags: [ "python" ]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

Python3

https://github.com/rocky/python-decompile3

get https://gitee.com/fujiawei/python-uncompyle6.git

python setup.py install

decompyle3 -o . raspbot.pyc
