---
date: 2022-05-23T22:34:34+08:00
author: "Rustle Karl"

title: "venv 创建虚拟环境"
url:  "posts/python/libraries/standard/packaging/venv"  # 永久链接
tags: [ "python" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

venv 模块支持使用自己的站点目录创建轻量级“虚拟环境”，可选择与系统站点目录隔离。每个虚拟环境都有自己的 Python 二进制文件（与用于创建此环境的二进制文件的版本相匹配），并且可以在其站点目录中拥有自己独立的已安装 Python 软件包集。

## 安装

必须单独安装：

```shell
apt install -y python3.10-venv
```

## 创建虚拟环境

```shell
python3 -m venv /path/to/new/virtual/environment
```

运行此命令将创建目标目录（父目录若不存在也将创建），并放置一个 pyvenv.cfg 文件在其中，文件中有一个 home 键，它的值指向运行此命令的 Python 安装（目标目录的常用名称是 .venv）。它还会创建一个 bin 子目录（在 Windows 上是 Scripts），其中包含 Python 二进制文件的副本或符号链接（视创建环境时使用的平台或参数而定）。它还会创建一个（初始为空的） lib/pythonX.Y/site-packages 子目录（在 Windows 上是 Lib\site-packages）。如果指定了一个现有的目录，这个目录就将被重新使用。

## 激活环境

```shell
source venv/bin/activate

source venv/bin/activate.fish

source venv/bin/activate.csh

source venv/bin/activate.ps1
```
