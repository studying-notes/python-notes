---
date: 2021-01-15T23:08:49+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Python Base64"  # 文章标题
url:  "posts/py/libraries/standard/base64"  # 设置网页永久链接
tags: [ "python", "standard", "base64" ]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

Base64 编码格式提供了以下六种接口：

1. b64encode(s, altchars=None)
2. b64decode(s, altchars=None)
3. standard_b64encode(s)
4. standard_b64decode(s)
5. urlsafe_b64encode(s)
6. urlsafe_b64decode(s)

其中以 "encode" 结尾的方法用于将二进制串转为 base64 编码格式的字符串，以 “decode” 结尾的方法用于将 base64 格式的字符串重新转为二进制串。

前两个方法 b64encode() 和 b64decode() 接收同样形式的参数。其中 s 是要编 / 解码的字符串；默认参数 altchars 的可选值必须是长度至少两字节的字符串（第二个字符后的内容将被忽略），该方法表示在编 / 解码过程中将使用参数 altchars 中的前两个字符替换标准 Base64 字符集中的 '+' 和 '/'。

因此方法 3 和 4 中的 base64.standard_b64encode(s) 和 base64.standard_b64decode(s) 等价于 base64.b64encode(s) 和 base64.b64decode(s)。而方法 5 和 6 中的 base64.urlsafe_b64encode(s) 和 base64.urlsafe_b64decode(s) 分别等价于 base64.b64encode(s, '-\_') 和 base64.b64decode(s, '-\_')，即在编 / 解码过程中使用 '-' 和 '_' 替代标准 Base64 字符集中的 '+' 和 '/'，生成可以在 URL 中使用的 Base64 格式文本。

```shell
>>> import base64
>>> print base64.b64encode('Hello, I am Darren!')
SGVsbG8sIEkgYW0gRGFycmVuIQ==
>>>
>>> print base64.b64decode('SGVsbG8sIEkgYW0gRGFycmVuIQ==')
Hello, I am Darren!
>>>
>>> print base64.b64encode('i\xb7\x1d\xfb\xef\xff')
abcd++//
>>>
>>> print base64.b64encode('i\xb7\x1d\xfb\xef\xff', '-_')
abcd--__
>>>
>>> print base64.urlsafe_b64encode('i\xb7\x1d\xfb\xef\xff')
abcd--__
>>>
>>> base64.urlsafe_b64decode('adcd--__')
'i\xb7\x1d\xfb\xef\xff'
```
