---
date: 2021-01-09T11:59:29+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "importlib - 导入模块"  # 文章标题
url:  "posts/python/libraries/standard/importlib"  # 设置网页永久链接
tags: [ "python", "standard", "importlib" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

# 1 模块简介

Python提供了importlib包作为标准库的一部分。目的就是提供Python中import语句的实现（以及__import__函数）。另外，importlib允许程序员创建他们自定义的对象，可用于引入过程（也称为importer）。

**什么是imp？** 另外有一个叫做imp的模块，它提供给Python import语句机制的接口。这个模块在Python 3.4中被否决，目的就是为了只使用importlib。

这个模块有些复杂，因此我们在这篇博文中主要讨论以下几个主题：

- 动态引入
- 检查模块是否可以被引入
- 引入源文件自身
- 第三方模块 import_from_github_com

# 2 模块使用

## 2.1 动态引入

importlib模块支持传入字符串来引入一个模块。我们创建两个简单的模块来验证这个功能。我们将会给予两个模块相同的接口，让它们打印名字以便我们能够区分它们。创建两个模块，分别为foo.py和bar.py，代码如下所示，

```python
def main():
    print(__name__)
```

现在我们使用importlib来引入它们。让我们看看这段代码如何去做的。确保你已经把这段代码放在与上面创建的两个模块相同的目录下。

```python
#importer.py
import importlib

def dynamic_import(module):
    return importlib.import_module(module)

if __name__ == "__main__":
    module = dynamic_import('foo')
    module.main()

    module_two = dynamic_import('bar')
    module_two()
```

在这段代码中，我们手动引入importlib模块，并创建一个简单的函数dynamic_import。这个函数所做的就是调用importlib模块中的import_module函数，入参就是我们传入的字符串，然后返回调用结果。在代码段的下面，我们调用每个模块的main方法，将会打印出每个模块的名称。在你的代码中，你可能不会大量这样做。当你只有一个字符串时，如果你想引入这个模块，importlib就允许你可以这么做。

## 2.2 模块引入检查

Python有一个编码规范就是EAPP：Easier to ask for forgiveness than permision。意思就是经常假设一些事情是存在的（例如，key在词典中），如果出错了，那么就捕获异常。你可以看 [Python标准模块--import](http://www.cnblogs.com/zhbzz2007/p/6048333.html) 文章中我们尝试引入模块，当它不存在时，我们就会捕获到ImportError。如果我们想检查并观察一个模块是否可以引入而不是仅仅是猜测，该如何去做？你可以使用importlib。代码如下：

```python
#coding:utf-8

import importlib.util
import importlib

def check_module(module_name):
    module_spec = importlib.util.find_spec(module_name)
    if module_spec is None:
        print("Module :{} not found".format(module_name))
        return None
    else:
        print("Module:{} can be imported!".format(module_name))
        return module_spec
    
def import_module_from_spec(module_spec):
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module

if __name__ == "__main__":
    module_spec = check_module("fake_module")
    module_spec = check_module("collections")
    if(module_spec):
        module = import_module_from_spec(module_spec)
        print(dir(module))
```

这里我们引入importlib模块的子模块util。在check_module函数中，我们调用find_spec函数来检查传入的字符串作为模块是否存在。首先，我们传入一个假的名称，然后我们传入一个Python模块的真实名称。如果你运行这段代码，你将会看到你传入一个没有安装的模块的名称，find_spec函数将会返回None，我们的代码将会打印出这个模块没有找到。如果找到了，我们就会返回模块的说明。我们可以获取到模块的说明，然后使用它来真正的引入模块。或者你可以将字符串传入到import_module函数中，正如我们在2.1节中所学习到的一样。但是我们已经学习到如何使用模块的说明。让我们看一下上述代码中的import_module_from_spec函数。它接受由check_module函数返回的模块说明。我们将其传入到module_from_spec函数，它将会返回引入的模块。Python的官方文档推荐，在引入模块后执行它，所以我们下一步做的就是调用exec_module函数。最后我们返回这个模块，并且运行Python的dir函数来确认这个我们就是我们所期望的。

## 2.3 从源文件中引入

在这一节中，我想说明importlib的子模块util还有另外一个技巧。你可以使用util通过模块名和文件路径来引入一个模块。示例如下所示，

```python
#coding:utf-8

import importlib.util

def import_source(module_name):
    module_file_path = module_name.__file__
    module_name = module_name.__name__
    
    module_spec = importlib.util.spec_from_file_location(module_name,module_file_path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    print(dir(module))

    msg = "The {module_name} module has the following methods:{methods}"
    print(msg.format(module_name = module_name,methods = dir(module)))
    
if __name__ == "__main__":
    import logging
    import_source(logging)
```

上述代码中，我们实际引入了logging模块，并将它传入到import_source函数。在这个函数中，我们首先获取到模块的实际路径和名称。然后我们将这些信息传入到util的spec_from_file_location函数中，这个将会返回模块的说明。一旦我们获取到模块的说明，我们就可以使用与2.2节相同的importlib机制来实际引入模块。

现在让我们来看一个精巧的第三方库，Python的__import__()函数直接引入github中的包。

## 2.4 import_from_github_com

这个精巧的包叫做import_from_github_com，它可以用于发现和下载github上的包。为了安装他，你需要做的就是按照如下命令使用pip，

```shell
pip install import_from_github_com
```

这个包使用了PEP 302中新的引入钩子，允许你可以从github上引入包。这个包实际做的就是安装这个包并将它添加到本地。你需要Python 3.2或者更高的版本，git和pip才能使用这个包。

一旦这些已经安装，你可以在Python shell中输入如下命令，

```python
>>> from github_com.zzzeek import sqlalchemy
Collecting git+https://github.com/zzzeek/sqlalchemy
Cloning https://github.com/zzzeek/sqlalchemy to /tmp/pip-acfv7t06-build
Installing collected packages: SQLAlchemy
Running setup.py install for SQLAlchemy ... done
Successfully installed SQLAlchemy-1.1.0b1.dev0
>>> locals()
{'__builtins__': <module 'builtins' (built-in)>, '__spec__': None,
'__package__': None, '__doc__': None, '__name__': '__main__',
'sqlalchemy': <module 'sqlalchemy' from '/usr/local/lib/python3.5/site-packages/\
sqlalchemy/__init__.py'>,
'__loader__': <class '_frozen_importlib.BuiltinImporter'>}
```

你如果看了import_from_github_com的源码，你将会注意到它并没有使用importlib。实际上，它使用了pip来安装那些没有安装的包，然后使用Python的__import__()函数来引入新安装的模块。这段代码非常值得学习。

## 2.5 总结

到这里，你已经了解到在你的代码中如何使用importlib和引入钩子。当然还有很多超出本文所覆盖的知识，如果你需要写一个自定义的引入器或者下载器，你需要花费很多时间来阅读官方文档和源码。
