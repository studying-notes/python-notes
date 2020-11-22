---
date: 2020-11-22T15:27:14+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Selenium 进阶操作"  # 文章标题
url:  "posts/py/arch/selenium/advanced"  # 设置网页永久链接
tags: [ "python", "selenium" ]  # 标签
series: [ "Selenium 自动化测试" ]  # 系列
categories: [ "学习笔记"]  # 分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

## 执行 JavaScript

### 操作页面元素

```python
import traceback
import unittest
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


class Demo(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_execute_script(self):
        url = 'http://www.baidu.com'
        self.driver.get(url)
        search_box = "document.getElementById('kw').value='python';"
        search_button = "document.getElementById('su').click()"
        try:
            self.driver.execute_script(search_box)
            sleep(3)
            self.driver.execute_script(search_button)
            sleep(3)
            self.assertTrue('python' in self.driver.page_source)
        except WebDriverException:
            print(traceback.print_exc())

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
```

### 修改页面元素属性

```python
from selenium import webdriver


def add_attribute(driver, element_obj, attribute, value):
    driver.execute_script(
        "arguments[0].%s=arguments[1]" % attribute, element_obj, value)


def set_attribute(driver, element_obj, attribute, value):
    driver.execute_script(
        "arguments[0].setAttribute(arguments[1], arguments[2])", element_obj, attribute, value)


def get_attribute(element_obj, attribute):
    return element_obj.get_attribute(attribute)


def remove_attribute(driver, element_obj, attribute):
    driver.execute_script(
        "arguments[0].removeAttribute(arguments[1])", element_obj, attribute)


driver = webdriver.Chrome()

driver.get('operate.html')
element = driver.find_element_by_xpath('//input')

add_attribute(driver, element, 'name', 'search')
get_attribute(element, 'name')
get_attribute(element, 'value')
set_attribute(driver, element, 'value', '这是更改后的文字')
```

### 操作滚动条

```python
import traceback
import unittest
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


class Demo(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_scroll(self):
        url = 'http://www.jd.com'
        self.driver.get(url)
        # 将页面的滚动条滑动到页面的最下方
        scroll = "window.scrollTo(100, document.body.scrollHeight);"
        # 将元素滚动到屏幕中间
        scroll_to_center = "document.getElementById('J_cate').scrollIntoView(true);"
        # 将元素滚动到屏幕底部
        scroll_to_bottom = "document.getElementById('J_cate').scrollIntoView(true);"
        # 将页面纵向向下滚动400像素
        scroll_px = "window.scrollBy(0, 400);"
        try:
            self.driver.execute_script(scroll)
            sleep(3)
            self.driver.execute_script(scroll_to_bottom)
            sleep(3)
            self.driver.execute_script(scroll_px)
            sleep(3)
        except WebDriverException:
            print(traceback.print_exc())

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
```

### 高亮元素

`src/advanced/execjs_4.py`


## 结束浏览器进程

```python
import os
import unittest

from selenium import webdriver


class Demo(unittest.TestCase):

    def test_kill_windows_process(self):
        firefox = webdriver.Firefox()
        chrome = webdriver.Chrome()

        return_code = os.system("TASKKILL /F /IM firefox.exe")
        if return_code == 0:
            print('OK')

        return_code = os.system("TASKKILL /F /IM chrome.exe")
        if return_code == 0:
            print('OK')


if __name__ == '__main__':
    unittest.main()
```

## 无人下载文件

`src/advanced/download.py`

## 下载到指定目录

`src/advanced/download_2.py`

## 无人上传文件

### send_keys 方法

`src/advanced/upload_1.py`

### 模拟键盘操作

`src/advanced/upload_2.py`

## 使用配置文件

### Firefox

```python
from selenium import webdriver

pro_path = r'C:\Users\White Turing\AppData\Roaming\Mozilla\Firefox\Profiles\mviet44m.WebDriver'
profile = webdriver.FirefoxProfile(pro_path)
profile.set_preference('browser.startup.homepage', 'http://www.sogou.com')
profile.set_preference('browser.startup.page', 1)
driver = webdriver.Firefox(firefox_profile=profile)
```

## 计算截屏相似度

`src/advanced/screenshot.py`

## 新开标签页

`src/advanced/newtab.py`

## HTML5

### 测试播放器

`src/advanced/player.py`

### 操作存储对象

`src/advanced/storage.py`

## 伪装头部

`src/advanced/header.py`

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

