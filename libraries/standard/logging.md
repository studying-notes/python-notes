---
date: 2020-11-30T09:49:37+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "logging - 日志系统"  # 文章标题
url:  "posts/python/libraries/standard/logging"  # 设置网页永久链接
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

## 介绍

Logging 支持输出不同级别的日志，可以输出到控制台和写入文件，支持 TCP、HTTP、GET/POST、SMTP、Socket 等协议，将日志信息发送到网络等等。

Logging 提供 5 个等级的输出，CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET，如果把 looger 的级别设置为 INFO，那么小于 INFO 级别的日志都不输出，大于等于 INFO 级别的日志都输出。

Logging 库提供了多个组件：Logger、Handler、Filter、Formatter：

Logger 对象提供应用程序可直接使用的接口，供应用代码使用；

- Handler 发送日志到适当的目的地；
- Filter 提供了过滤日志信息的方法，控制输出；
- Formatter 指定日志输出和显示的具体格式。

## 同时输出到控制台和写入文件

```python
import logging
from logging import Logger
import os
from logging.handlers import RotatingFileHandler


def get_logger(name, log_file) -> Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)

    logfile = os.path.join(logs_dir, log_file)

    # 日志文件
    file_handler = RotatingFileHandler(
        logfile, mode='a',
        maxBytes=1024*1024*50,
        backupCount=30
    )
    file_handler.setLevel(logging.INFO)

    # 控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 输出格式
    formatter = logging.Formatter(
        "%(asctime)s [%(filename)s %(lineno)s] %(levelname)s: %(message)s",
        "%Y.%m.%d %H:%M:%S"
    )

    # 为文件输出设定格式
    file_handler.setFormatter(formatter)

    # 控制台输出设定格式
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
```

## 格式化

| %(name)s | Logger 的名字 |
| ------------------- | ------------------- |
| %(levelno)s | 数字形式的日志级别 |
| %(levelname)s | 文本形式的日志级别 |
| %(pathname)s | 调用日志输出函数的模块的完整路径名。可能没有 |
| %(filename)s | 调用日志输出函数的模块的文件名 |
| %(module)s | 调用日志输出函数的模块名 |
| %(funcName)s | 调用日志输出函数的函数名 |
| %(lineno)d | 调用日志输出函数的语句所在的代码行 |
| %(created)f | 当前时间，用 UNIX 标准的表示时间的浮点数表示 |
| %(relativeCreated)d | 输出日志信息时的，自 Logger 创建以来的毫秒数 |
| %(asctime)s | 字符串形式的当前时间。默认格式是“2003-07-08 16:49:45,896”。逗号后面的是毫秒 |
| %(thread)d | 线程 ID。可能没有 |
| %(threadName)s | 线程名。可能没有 |
| %(process)d | 进程 ID。可能没有 |
| %(message)s | 用户输出的消息 |

## 时间日期格式化符号

- %y 两位数的年份表示（00-99）
- %Y 四位数的年份表示（000-9999）
- %m 月份（01-12）
- %d 月内中的一天（0-31）
- %H 24小时制小时数（0-23）
- %I 12小时制小时数（01-12）
- %M 分钟数（00=59）
- %S 秒（00-59）
- %a 本地简化星期名称
- %A 本地完整星期名称
- %b 本地简化的月份名称
- %B 本地完整的月份名称
- %c 本地相应的日期表示和时间表示
- %j 年内的一天（001-366）
- %p 本地A.M.或P.M.的等价符
- %U 一年中的星期数（00-53）星期天为星期的开始
- %w 星期（0-6），星期天为星期的开始
- %W 一年中的星期数（00-53）星期一为星期的开始
- %x 本地相应的日期表示
- %X 本地相应的时间表示
- %Z 当前时区的名称
- %% %号本身

## 计算毫秒

```python
import datetime
import time

print(
    time.strftime('%Y-%m-%d  %H:%M:%S'),
    datetime.datetime.now().strftime('%f')[:3]
)

print(datetime.datetime.now().strftime('%Y%m%d %H:%M:%S.%f'))
```

```python

```
