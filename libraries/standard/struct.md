---
date: 2022-02-05T15:15:21+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "struct - 将字节串解读为打包的二进制数据"  # 文章标题
# description: "文章描述"
url:  "posts/py/libraries/standard/struct"  # 设置网页永久链接
tags: [ "python", "standard", "struct"]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

## 字节顺序

| 字符 | 字节顺序      | 大小     | 对齐方式 |
| :--- | :------------ | :------- | :------- |
| `@`  | 按原字节      | 按原字节 | 按原字节 |
| `=`  | 按原字节      | 标准     | 无       |
| `<`  | 小端          | 标准     | 无       |
| `>`  | 大端          | 标准     | 无       |
| `!`  | 网络（=大端） | 标准     | 无       |

## 类型大小

| 格式 | C 类型             | Python 类型       | 标准大小 | 备注     |
| :--- | :----------------- | :---------------- | :------- | :------- |
| `x`  | 填充字节           | 无                |          |          |
| `c`  | char               | 长度为 1 的字节串 | 1        |          |
| `b`  | signed char        | 整数              | 1        | (1), (2) |
| `B`  | unsigned char      | 整数              | 1        | (2)      |
| `?`  | _Bool              | bool              | 1        | (1)      |
| `h`  | short              | 整数              | 2        | (2)      |
| `H`  | unsigned short     | 整数              | 2        | (2)      |
| `i`  | int                | 整数              | 4        | (2)      |
| `I`  | unsigned int       | 整数              | 4        | (2)      |
| `l`  | long               | 整数              | 4        | (2)      |
| `L`  | unsigned long      | 整数              | 4        | (2)      |
| `q`  | long long          | 整数              | 8        | (2)      |
| `Q`  | unsigned long long | 整数              | 8        | (2)      |
| `n`  | `ssize_t`          | 整数              |          | (3)      |
| `N`  | `size_t`           | 整数              |          | (3)      |
| `e`  | (6)                | float             | 2        | (4)      |
| `f`  | float              | float             | 4        | (4)      |
| `d`  | double             | float             | 8        | (4)      |
| `s`  | char[]             | 字节串            |          |          |
| `p`  | char[]             | 字节串            |          |          |
| `P`  | void*              | 整数              |          | (5)      |

## 实例

```python
>>> from struct import *
>>> pack('hhl', 1, 2, 3)
b'\x00\x01\x00\x02\x00\x00\x00\x03'
>>> unpack('hhl', b'\x00\x01\x00\x02\x00\x00\x00\x03')
(1, 2, 3)
>>> calcsize('hhl')
8
```

```python
>>> record = b'raymond   \x32\x12\x08\x01\x08'
>>> name, serialnum, school, gradelevel = unpack('<10sHHb', record)

>>> from collections import namedtuple
>>> Student = namedtuple('Student', 'name serialnum school gradelevel')
>>> Student._make(unpack('<10sHHb', record))
Student(name=b'raymond   ', serialnum=4658, school=264, gradelevel=8)
```
