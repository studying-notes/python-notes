---
date: 2020-12-24T08:59:43+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "hashlib - 安全散列和消息摘要"  # 文章标题
url:  "posts/python/libraries/standard/hashlib"  # 设置网页永久链接
tags: [ "python", "standard", "hashlib"]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

```py
hash.digest()
```

返回二进制数据，字节

```py
hash.hexdigest()
```

返回十六进制数据，字符串

```py
import hashlib

md5 = hashlib.md5()
md5.update("I'm a loser.".encode('utf-8'))

print(u"digest: %s" % md5.digest())
print(u"hexdigest: %s" % md5.hexdigest())
```
