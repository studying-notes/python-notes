---
date: 2022-04-03T16:07:58+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Python 学习笔记"  # 文章标题
description: "纸上得来终觉浅，学到过知识点分分钟忘得一干二净，今后无论学什么，都做好笔记吧。"
url:  "posts/python/README"  # 设置网页永久链接
tags: [ "Python", "README" ]  # 标签
series: [ "Python 学习笔记" ]  # 系列
categories: [ "学习笔记" ]  # 分类

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

# Python 学习笔记

> 纸上得来终觉浅，学到过知识点分分钟忘得一干二净，今后无论学什么，都做好笔记吧。

## 目录结构

- `assets/images`: 笔记配图
- `assets/templates`: 笔记模板
- `docs`: 基础语法
- `libraries`: 库
  - `libraries/standard`: 标准库
  - `libraries/tripartite`: 第三方库
- `quickstart`: 基础用法
- `src`: 源码示例
  - `src/docs`: 基础语法源码示例
  - `src/libraries/standard`: 标准库源码示例
  - `src/libraries/tripartite`: 第三方库源码示例
  - `src/quickstart`: 基础用法源码示例

## 基础用法

- [Centos 升级安装 Python](quickstart/install/centos.md)
- [Python 打包分发](quickstart/dist.md)
- [Black - Python 代码格式化工具](docs/others/black.md)
- [运算符优先级](docs/others/priority.md)
- [内置数据结构的复杂度](docs/others/complexity.md)
- [下划线命名变量区别](docs/others/variable.md)
- [逆向编译](docs/others/decompile.md)
- [Jupyter Lab 排错指南](docs/others/jupyterlab.md)

## 基础语法

## 库

## 标准库

- [queue - 线程安全的队列实现](libraries/standard/queue.md)
- [subprocess - 子进程管理](libraries/standard/subprocess.md)
- [struct - 将字节串解读为打包的二进制数据](libraries/standard/struct.md)
- [tempfile - 生成临时文件和目录](libraries/standard/tempfile.md)
- [enum - 枚举](libraries/standard/enum.md)
- [concurrent.futures - 异步管理](libraries/standard/concurrent_futures.md)
- [hashlib - 安全散列和消息摘要](libraries/standard/hashlib.md)
- [importlib - 导入模块](libraries/standard/importlib.md)
- [logging - 日志系统](libraries/standard/logging.md)

## 第三方库

- [Scapy 简介](libraries/tripartite/scapy/README.md) 
