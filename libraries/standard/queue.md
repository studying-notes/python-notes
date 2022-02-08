---
date: 2020-12-19T08:41:24+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "queue - 线程安全的队列实现"  # 文章标题
url:  "posts/python/libraries/standard/queue"  # 设置网页永久链接
tags: [ "python", "standard", "logging" ]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

[`queue`](https://docs.python.org/zh-cn/3/library/queue.html#module-queue) 模块实现了多生产者、多消费者队列。

这特别适用于消息必须安全地在多线程间交换的线程编程。

模块中的 [`Queue`](https://docs.python.org/zh-cn/3/library/queue.html#queue.Queue) 类实现了所有所需的锁定语义。

模块实现了三种类型的队列，它们的区别仅仅是条目取回的顺序。

在 FIFO 队列中，先添加的任务先取回。

在 LIFO 队列中，最近被添加的条目先取回(操作类似一个堆栈)。

优先级队列中，条目将保持排序( 使用 [`heapq`](https://docs.python.org/zh-cn/3/library/heapq.html#module-heapq) 模块 ) 并且最小值的条目第一个返回。

在内部，这三个类型的队列使用锁来临时阻塞竞争线程；然而，它们并未被设计用于线程的重入性处理。

```python
import threading, queue

q = queue.Queue()

def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        q.task_done()

# turn-on the worker thread
threading.Thread(target=worker, daemon=True).start()

# send thirty task requests to the worker
for item in range(30):
    q.put(item)
print('All task requests sent\n', end='')

# block until all tasks are done
q.join()
print('All work completed')
```
