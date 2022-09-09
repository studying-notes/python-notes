---
date: 2022-09-09T15:57:50+08:00  # 创建日期
author: "Rustle Karl"  # 作者

title: "socket 底层网络接口常用示例"  # 文章标题
url:  "posts/python/libraries/standard/NetworkingAndInterprocessCommunication/socket_examples"  # 设置网页永久链接
tags: [ "python", "socket-examples" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

## UDP

### UDP 客户端

```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # 发送数据包
    s.sendto(b"get", ("localhost", 6688))

    # 接收数据包
    data, addr = s.recvfrom(1024)
    print(data.decode('utf-8'))
```

## TCP

### TCP 客户端

```python

```

```python

```
