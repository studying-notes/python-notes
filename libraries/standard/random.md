---
date: 2021-01-09T11:57:35+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Python random 随机"  # 文章标题
url:  "posts/py/libraries/standard/random"  # 设置网页永久链接
tags: [ "python", "standard", "random" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类


# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

**1.random.random()**

 \#用于生成一个0到1的

随机浮点数：0<= n < 1.0

```javascript
import random  
a = random.random()
print (a)  
```

![img](https://ask.qcloudimg.com/http-save/5426480/fibgwyi9so.jpeg?imageView2/2/w/1620)

**2.random.uniform(a,b)** 

\#用于生成一个指定范围内的随机符点数，两个参数其中一个是上限，一个是下限。如果a > b，则生成的随机数n: a <= n <= b。如果 a <b， 则 b <= n <= a。

```javascript
import random  
print(random.uniform(1,10))  
print(random.uniform(10,1)) 
```

![img](https://ask.qcloudimg.com/http-save/5426480/nu7vjdpdkx.jpeg?imageView2/2/w/1620)

**3.random.randint(a, b)**

 \#用于生成一个指定范围内的整数。其中参数a是下限，参数b是上限，生成的随机数n: a <= n <= b

```javascript
import random  
print(random.randint(1,10))  
```

![img](https://ask.qcloudimg.com/http-save/5426480/4td2tr6cp4.jpeg?imageView2/2/w/1620)

**4.random.randrange([start], stop[, step])**

 \#从指定范围内，按指定基数递增的集合中 获取一个随机数。

random.randrange(10, 30, 2)，结果相当于从[10, 12, 14, 16, ... 26, 28]序列中获取一个随机数。

random.randrange(10, 30, 2)在结果上与 random.choice(range(10, 30, 2) 等效。

```javascript
import random  
print(random.randrange(10,30,2)) 
```

![img](https://ask.qcloudimg.com/http-save/5426480/9rrrh7sza9.jpeg?imageView2/2/w/1620)

**5.random.choice(sequence)**

\#random.choice从序列中获取一个随机元素。其函数原型为：random.choice(sequence)。

参数sequence表示一个有序类型。这里要说明 一下：sequence在python不是一种特定的类型，而是泛指一系列的类型。list, tuple, 字符串都属于sequence。

```javascript
import random  
lst = ['python','C','C++','javascript']  
str1 = ('I love python')  
print(random.choice(lst))
print(random.choice(str1))  
```

![img](https://ask.qcloudimg.com/http-save/5426480/yubryfp23w.jpeg?imageView2/2/w/1620)

**6.random.shuffle(x[, random])**

\#用于将一个列表中的元素打乱,即将列表内的元素随机排列。

```javascript
import random
p = ['A' , 'B', 'C', 'D', 'E' ]
random.shuffle(p)  
print (p)  
```

![img](https://ask.qcloudimg.com/http-save/5426480/2xaqglpm1y.jpeg?imageView2/2/w/1620)

**7.random.sample(sequence, k)**

\#从指定序列中随机获取指定长度的片断并随机排列。注意：sample函数不会修改原有序列。

```javascript
import random   
lst = [1,2,3,4,5]  
print(random.sample(lst,4))  
print(lst) 
```