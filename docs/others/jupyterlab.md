---
date: 2021-01-08T19:25:37+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Jupyter Lab 排错指南"  # 文章标题
url:  "posts/python/docs/others/jupyterlab"  # 设置网页永久链接
tags: [ "python", "pip", "jupyterlab" ]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

## 系统找不到指定的文件

![img](https://i.loli.net/2021/01/08/veObNBHTRhCaMk6.png)

一般就是 kernels 文件有错，相关文件路径：

```ini
C:\Users\Admin\AppData\Roaming\jupyter\kernels
```

```ini
/usr/local/share/jupyter/kernels
```

```shell
C:\Users\Admin\AppData\Roaming\jupyter\runtime
```

打开其中的文件看一下路径是否正确。

```shell
jupyter lab --allow-root
```

```shell
pip install ipykernel
```

```shell
python -m ipykernel install
```

```shell

```

```shell

```



```shell

```


