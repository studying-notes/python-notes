---
date: 2021-01-09T10:02:39+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Python SVG 图片转 PNG 格式"  # 文章标题
url:  "posts/py/libraries/tripartite/cairosvg"  # 设置网页永久链接
tags: [ "python", "SVG", "cairosvg" ]  # 自定义标签
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
import cairosvg
import os
from wand.image import Image

imgs_list = [
    'logo-apple.svg',
    'logo-apple-1024.png',
    'logo-apple-128.png',
    'logo-apple-16.png',
    'logo-apple-175.png',
    'logo-apple-256.png',
    'logo-apple-512.png',
    'logo-apple-56.png',
]

src = 'storage/logo-avatar.svg'
output = 'storage/output'

for img in imgs_list:
    n, e = os.path.splitext(img)
    size = 32
    try:
        size = int(n[n.index('e-')+2:])
    except ValueError:
        pass
    if e == '.png':
        cairosvg.svg2png(
            url=src,
            output_height=size, output_width=size,
            write_to=os.path.join(output, img)
        )

```