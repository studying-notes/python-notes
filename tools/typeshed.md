---
date: 2022-05-10T13:39:39+08:00
author: "Rustle Karl"

title: "静态类型存根 typeshed"
url:  "posts/python/tools/typeshed"  # 永久链接
tags: [ "python" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

https://github.com/python/typeshed

## 简介

Typeshed 包含 Python 标准库和 Python 内置函数的外部类型注释，以及由这些项目外部人员贡献的第三方包。可以用于静态分析、类型检查或类型推断。

## 用法

如果只是使用 mypy（或 pytype 或 PyCharm，可能自带？待求证），而不是开发它，则根本不需要与 typeshed repo 交互：typeshed 的标准库部分的副本与 mypy 捆绑在一起。

第三方包和模块的类型存根可以从 PyPI 安装。例如，six 和 requests，则可以使用安装类型存根：

```python
pip install types-six types-requests
```
