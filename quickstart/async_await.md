---
date: 2022-03-07T08:51:29+08:00
author: "Rustle Karl"

title: "异步"
url:  "posts/python/quickstart/async_await"  # 永久链接
tags: [ "python"]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

## 二级

### time.sleep VS asyncio.sleep

```python
import asyncio
import time


async def hello():
    print("Hello ...")
    time.sleep(1)
    print("... World!")


async def main():
    await asyncio.gather(hello(), hello())


async def hello_async():
    print("Hello ...")
    await asyncio.sleep(1)
    print("... World!")


async def main_async():
    await asyncio.gather(hello_async(), hello_async())


print("time.sleep")
asyncio.run(main())

print("asyncio.sleep")
asyncio.run(main_async())
```

```shell
time.sleep
Hello ...
... World!
Hello ...
... World!
asyncio.sleep
Hello ...
Hello ...
... World!
... World!
```

只有遇到 await 语句，才会不阻塞，否则执行完了才会执行下一个，与多线程是不一样的。

### 后台执行，而不是 await

await 仍会阻塞当前的函数，希望后台执行某个函数，则可用

```python
asyncio.create_task(func())
```

```shell

```


## 二级

### 三级

```python

```

```shell

```


## 二级

### 三级

```python

```

```shell

```


## 二级

### 三级

```python

```

```shell

```


