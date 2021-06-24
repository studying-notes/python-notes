---
date: 2021-01-16T07:42:11+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Python schedule 定时任务"  # 文章标题
# description: "文章描述"
url:  "posts/py/libraries/tripartite/serial"  # 设置网页永久链接
tags: [ "python", "串口" ]  # 自定义标签
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
pip install schedule
```

```python
import schedule
import time

def job():
    print("I'm working...")

schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)
schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
```

默认情况下，schedule 按顺序执行所有作业，可以通过在自己的线程中运行每个作业来绕过这个限制:

```python
import threading
import time
import schedule


def job():
    print("I'm running on thread %s" % threading.current_thread())


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


schedule.every(10).seconds.do(run_threaded, job)
schedule.every(10).seconds.do(run_threaded, job)
schedule.every(10).seconds.do(run_threaded, job)
schedule.every(10).seconds.do(run_threaded, job)
schedule.every(10).seconds.do(run_threaded, job)


while 1:
    schedule.run_pending()
    time.sleep(1)
```

更严格地控制线程数，可以使用共享的 jobqueue 和一个或多个工作线程：

```python
import time
import threading
import schedule


def job():
    print("I'm working")


def worker_main():
    while 1:
        job_func = jobqueue.get()
        job_func()
        jobqueue.task_done()

jobqueue = Queue.Queue()

schedule.every(10).seconds.do(jobqueue.put, job)
schedule.every(10).seconds.do(jobqueue.put, job)
schedule.every(10).seconds.do(jobqueue.put, job)
schedule.every(10).seconds.do(jobqueue.put, job)
schedule.every(10).seconds.do(jobqueue.put, job)

worker_thread = threading.Thread(target=worker_main)
worker_thread.start()

while 1:
    schedule.run_pending()
    time.sleep(1)
```

## 只运行一次

```python
def job_that_executes_once():
    # Do some work ...
    return schedule.CancelJob

schedule.every().day.at('22:30').do(job_that_executes_once)
```

## 随机间隔时间

```python
def my_job():
    # This job will execute every 5 to 10 seconds.
    print('Foo')

schedule.every(5).to(10).seconds.do(my_job)
```

```python

```
```python

```
```python

```
```python

```
```python

```
```python

```
```python

```
```python

```
```python

```
```python

```




