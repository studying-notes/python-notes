---
date: 2021-05-27T10:28:28+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Python UUID 标准库"  # 文章标题
url:  "posts/py/libraries/standard/uuid"  # 设置网页永久链接
tags: [ "python", "standard", "uuid" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

UUID 是 128 位的全局唯一标识符，通常由 32 字节的字符串表示。

它可以保证时间和空间的唯一性，也称为 GUID，全称为：

   UUID Universally unique IDentifier python 中叫 UUID
   GUID Globally Unique IDentifier C#中叫 GUID

它是通过 MAC 地址、时间戳、命名空间、随机数、伪随机数来保证生成 ID 的唯一性。

UUID 主要有 5 个算法，也就是 5 中方法来实现：

  uuid1() --- 基于时间戳
  由 MAC 地址、当前时间戳、随机数生成。可以保证全球范围内的唯一性，但 MAC 的使用同时带来了安全性问题，局域网中可以使用 IP 来代替 MAC。

  uuid2() -- 基于分布式计算环境 DCE（python 中没有这个函数）
  算法与 uuid1 相同，不同的是把时间戳的前 4 位置换为 POSIX 的 UID。实际中很少使用

  uuid3() --- 基于名字的 MD5 散列值
  通过计算名字和命名空间的 MD5 散列值得到，保证了同一命名空间中不同名字的唯一性，和不同命名空间的唯一性，但同一命名空间的同一名字生成相同的 uuid。

  uuid4() --- 基于随机数
  由伪随机数得到，有一定的重复概率，该概率可以计算出来。

  uuid5() --- 基于名字的 SHA-1 散列值
  算法与 uuid3 相同，不同的是使用 secure Hash Algorithm 1 算法。

使用方面：

   python 中没有基于 DCE 的，所有 uuid2 可以忽略；
   uuid4 存在概率性重复，由无映射性，最好不用；
  在 Global 的分布式计算环境下，最好用 uuid1 ；
  有名字的唯一性要求，最好用 uuid3 或 uuid5

```python
def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])
```


