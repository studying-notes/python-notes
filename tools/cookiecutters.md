---
date: 2022-06-03T21:39:42+08:00
author: "Rustle Karl"

title: "cookiecutters 基于模板生成项目脚手架"
url:  "posts/python/tools/cookiecutters"  # 永久链接
tags: [ "python" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

Cookiecutter 是一个通过项目模板创建项目的命令行工具。

> https://cookiecutter.readthedocs.io/en/latest/

## 安装

```shell
pip install cookiecutter
```

## 使用

官方删掉了可用的模板列表，让用户自行搜索。

https://github.com/search?q=cookiecutter&type=Repositories

比如使用官方维护的 PyPi 模板：

```shell
cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git
```

如此庞大而复杂的一个项目结构，融合了作者对一个开源 PyPI 项目的理解。 虽然未必适用于任何一个人。

## 基本原理

cookiecutter 的工作原理，是先下载一个模板项目，然后替换模板项目的某些内容，生成新的项目。 

使用过模板的项目，默认都已经被下载到~/.cookiecutter目录下。 如果需要再次使用，而又无需更新，可以直接用项目名。

```shell
cookiecutter cookiecutter-pypackage
```

## 配置文件

默认情况下，~/.cookiecutterrc 就是配置文件。

```shell
code ~/.cookiecutterrc
```

```yaml
default_context:
  full_name: "Rustle Karl"
  email: "fu.jiawei@outlook.com"
  github_username: "fujiawei-dev"
cookiecutters_dir: "~/.cookiecutters/"
abbreviations:
  pypkg: https://github.com/audreyr/cookiecutter-pypackage.git
  gh: https://github.com/{0}.git
```

## 自定义模块

我之前也基于 Jinjia2 搞了一个自己的项目工程模板生成器，之后可能迁移到 cookiecutter 上。
