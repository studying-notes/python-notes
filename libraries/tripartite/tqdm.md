---
date: 2021-01-09T12:00:58+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Python Tqdm 进度条"  # 文章标题
# description: "文章描述"
url:  "posts/py/libraries/tripartite/tqdm"  # 设置网页永久链接
tags: [ "python", "进度条" ]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

Tqdm 是一个快速，可扩展的 Python 进度条，可以在 Python 长循环中添加一个进度提示信息，用户只需要封装任意的迭代器。

```python
pip install tqdm
```

## 基本用法

```python
from tqdm import tqdm

for i in tqdm(range(10000)):
    sleep(0.01) 
```

当然除了 tqdm，还有 trange，使用方式完全相同

```python
for i in trange(100):
    sleep(0.1) 
```

只要传入 list 都可以：

```python
pbar = tqdm(["a", "b", "c", "d"])

for char in pbar:
  pbar.set_description("Processing %s" % char)
```

也可以手动控制更新

```python
with tqdm(total=100) as pbar:
  for i in range(10):
    pbar.update(10) 
```

也可以这样：

```python
pbar = tqdm(total=100)
for i in range(10):
  pbar.update(10)
pbar.close() 
```

## 核心函数

通过看示范的代码，我们能发现使用的核心是 tqdm 和 trange 这两个函数，从代码层面分析 tqdm 的功能，那首先是 init.py。

```python
__all__ = ['tqdm', 'tqdm_gui', 'trange', 'tgrange', 'tqdm_pandas',
      'tqdm_notebook', 'tnrange', 'main', 'TqdmKeyError', 'TqdmTypeError',
      '__version__']
```

跟踪到 _tqdm.py，能看到 tqdm 类的声明，首先是初始化

```python
def __init__(self, iterable=None, desc=None, total=None, leave=True,
         file=sys.stderr, ncols=None, mininterval=0.1,
         maxinterval=10.0, miniters=None, ascii=None, disable=False,
         unit='it', unit_scale=False, dynamic_ncols=False,
         smoothing=0.3, bar_format=None, initial=0, position=None,
         gui=False, **kwargs):
```
