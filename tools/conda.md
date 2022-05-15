---
date: 2022-05-10T12:39:17+08:00
author: "Rustle Karl"

title: "Anaconda 与 Conda 基本用法"
url:  "posts/shell/tools/conda"  # 永久链接
tags: [ "shell" ]  # 自定义标签
series: [ "shell 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

Anaconda 是 shell 的发行版，集成了大量的科学计算第三方库。Conda 是其包管理器，比 Pip 强大的一点是可以安装编译好的 C 库，有时候 Pip 无法安装的，就可以用 Conda 试一下。

## 安装

https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/

Linux 也只能从安装包安装。

## 环境变量

```shell
c:\tools\anaconda3;c:\tools\anaconda3\library\mingw-w64\bin;c:\tools\anaconda3\library\usr\bin;c:\tools\anaconda3\library\bin;c:\tools\anaconda3\scripts;
```

## 卸载

官方推荐：

```shell
rm -rf ~/anaconda3
```

## 从旧版本升级

```shell
#update the conda package manager to the latest version
conda update conda

#use conda to update Anaconda to the latest version
conda update anaconda
```

## 升级包

```shell
# This updates all packages in the current environment to the latest version. In doing so, it drops all the version constraints from the history and tries to make everything as new as it can.
conda update --all

# only update the selected environment.
conda update -n environment --all
```

## 包管理器命令

### 已安装列表

```shell
conda list
```

### 搜索包

```shell
conda search package
```

### 安装包

```shell
conda install package
```

### 创建虚拟环境

```shell
conda create -n environment ipython-notebook numpy
```

`-n` 虚拟环境名称，后面跟的都是需要安装的依赖包。

### 激活虚拟环境

```shell
conda activate environment
```

### 退出当前虚拟环境

```shell
conda deactivate
```
