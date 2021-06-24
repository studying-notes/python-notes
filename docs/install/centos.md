---
date: 2021-03-02T13:12:18+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Centos 升级安装 Python"  # 文章标题
# description: "文章描述"
url:  "posts/py/doc/install/centos"  # 设置网页永久链接
tags: [ "python", "centos"]  # 标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

```shell
wget https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tar.xz
```

```shell
xz -d Python-3.8.5.tar.xz && tar xvf Python-3.8.5.tar
```

```shell
mkdir /usr/local/python3/
```

```shell
yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc  libffi-devel
```

```shell
cd Python-3.8.5 
```

```shell
./configure --prefix=/usr/local/python3 --enable-optimizations
```

```shell
make
```

```shell
make install
```

```shell
cp /usr/bin/python /usr/bin/python2
cp /usr/bin/pip /usr/bin/pip2
```

```shell
rm /usr/bin/python
rm /usr/bin/pip

ln -s /usr/local/python3/bin/python3.8 /usr/bin/python
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip
```

```shell
sed -i '1s/python/python2/' /usr/bin/yum
sed -i '1s/python/python2/' /usr/libexec/urlgrabber-ext-down
sed -i '1s/python/python2/' /usr/sbin/firewalld
sed -i '1s/python/python2/' /usr/bin/firewall-cm
```

```shell

```

```shell

```
