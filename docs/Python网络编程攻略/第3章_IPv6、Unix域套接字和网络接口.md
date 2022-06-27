---
date: 2022-04-08T20:39:29+08:00
author: "Rustle Karl"

title: "第3章_IPv6、Unix域套接字和网络接口"
url:  "posts/python/docs/Python网络编程攻略/第3章_IPv6、Unix域套接字和网络接口"  # 永久链接
tags: [ "python"]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

## 把本地端口转发到远程主机

有时，你需要创建一个本地端口转发器，把本地端口发送的流量全部重定向到特定的远程主机上。利用这个功能，可以让用户只能访问特定的网站，而不能访问其他网站。

见 `src\docs\Python网络编程攻略\CH03\CH0301.py`

我们创建了一个端口转发类 PortForwarder，继承自 asyncore.dispatcher。asyncore.dispatcher 类包装了一个套接字对象，还提供了一些帮助方法用于处理特定的事件，例如连接成功或客户端连接到服务器套接字。你可以选择重定义这些方法，在上面的脚本中我们只重定义了 handle_accept() 方法。

另外两个类也继承自 asyncore.dispatcher。Receiver 类处理进入的客户端请求，Sender 类接收一个 Receiver 类实例，把数据发送给客户端。如你所见，这两个类都重定义了 handle_read()、handle_write() 和 writeable() 三个方法，目的是实现远程主机和本地客户端之间的双向通信。

概括来说，PortForwarder 类在一个本地套接字中保存进入的客户端请求，然后把这个套接字传给 Sender 类实例，再使用 Receiver 类实例发起与远程主机指定端口之间的双向通信。

## 通过ICMP查验网络中的主机

```python

```

## 等待远程网络服务上线

```python

```

## 枚举设备中的接口

```python

```

## 找出设备中某个接口的IP地址

```python

```

## 探测设备中的接口是否开启

```python

```

## 检测网络中未开启的设备

```python

```

## 使用相连的套接字执行基本的进程间通信

```python

```

## 使用Unix域套接字执行进程间通信

```python

```

## 确认你使用的Python是否支持IPv6套接字

```python

```

## 从IPv6地址中提取IPv6前缀

```python

```

## 编写一个IPv6回显客户端/服务器

```python

```
