---
date: 2020-11-22T11:54:01+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Selenium 入门"  # 文章标题
url:  "posts/py/arch/selenium/quickstart"  # 设置网页永久链接
tags: [ "python", "quickstart", "selenium" ]  # 标签
series: [ "Selenium 自动化测试" ]  # 系列
categories: [ "学习笔记"]  # 分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

## 安装 Selenium 包

```shell
pip install selenium
```

## 下载浏览器驱动

### Chrome

https://sites.google.com/a/chromium.org/chromedriver/home

### Edge

https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver

> 加入 PATH

## 入门示例

```python
from selenium import webdriver

driver = webdriver.Chrome()

driver.get('http://www.sogou.com')
ele = driver.find_element_by_id('query')
ele.clear()
ele.send_keys('自动化测试')
driver.find_element_by_id('stb').click()

driver.quit()
```

## 单元测试

```python
import unittest

from selenium import webdriver


class AutoSogou(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_sogou(self):
        self.driver.get('http://www.sogou.com')
        print(self.driver.current_url)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
```

```python

```

```python

```

```python

```

```python

```
