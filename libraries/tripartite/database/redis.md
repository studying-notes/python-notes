---
date: 2022-06-05T12:41:29+08:00
author: "Rustle Karl"  # 作者

title: "Redis 客户端"  # 文章标题
url:  "posts/python/libraries/tripartite/database/redis"  # 设置网页永久链接
tags: [ "python", "redis" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

> https://github.com/redis/redis-py

> https://redis-py.readthedocs.io/en/stable/index.html

## 安装

```shell
pip install redis
```

## 基础操作

```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

r.set('foo', 'bar')
r.get('foo')
```

## 发布订阅

```python
import redis

r = redis.Redis(host="localhost", port=6379, db=0)

# 订阅
p = r.pubsub()
p.subscribe(dev=lambda msg: print(msg))
p.run_in_thread()

# 发布
for i in range(10):
    r.publish("dev", i)
```

## 集群模式

```python
import redis

r = redis.cluster.RedisCluster(
    host="localhost",
    port=6371,
    password="120e204105de1345fda9f27911c02f66",
)

r.set("foo", "bar")
r.get("foo")
```

```python

```
