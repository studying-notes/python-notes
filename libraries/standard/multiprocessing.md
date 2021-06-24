---
date: 2021-03-06T20:18:10+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Python multiprocessing 多进程管理"  # 文章标题
url:  "posts/py/libraries/standard/multiprocessing"  # 设置网页永久链接
tags: [ "python", "standard", "multiprocessing" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

## 线程可以修改当前的值，进程不能

```python
from multiprocessing import Process
from threading import Thread

x = {"1": 1, "2": 2}


def play(n):
    x["3"] = 3
    print(x)
    print("play", n)


if __name__ == '__main__':
    # p = Process(target=play, args=("music",))
    p = Thread(target=play, args=("music",))
    p.start()
    p.join()
    print(x)
```

## shared_memory

https://docs.python.org/zh-cn/3/library/multiprocessing.shared_memory.html

> 可从进程直接访问的共享内存

这种类型的的共享内存允许不同进程读写一片公共（或者共享）的易失性存储区域。一般来说，进程被限制只能访问属于自己进程空间的内存，但是共享内存允许跨进程共享数据，从而避免通过进程间发送消息的形式传递数据。与通过磁盘、套接字或者其他要求序列化、反序列化和复制数据的共享形式相比，直接通过内存共享数据拥有更出色的性能。


```python
import array
from multiprocessing import shared_memory

shm_a = shared_memory.SharedMemory(create=True, size=10)
type(shm_a.buf)

buffer = shm_a.buf
len(buffer)

buffer[:4] = bytearray([22, 33, 44, 55])  # Modify multiple at once
buffer[4] = 100  # Modify single byte at a time
# Attach to an existing shared memory block
shm_b = shared_memory.SharedMemory(shm_a.name)

bytes(shm_a.buf)
bytes(shm_b.buf)

array.array('b', shm_b.buf[:5])  # Copy the data into a new array.array

shm_b.buf[:5] = b'howdy'  # Modify via shm_b using bytes
bytes(shm_a.buf[:5])  # Access via shm_a

shm_b.close()  # Close each SharedMemory instance
shm_a.close()
shm_a.unlink()  # Call unlink only once to release the shared memory
```












