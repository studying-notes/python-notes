---
date: 2022-02-10T15:23:50+08:00
author: "Rustle Karl"

title: "Python 打包分发"
url:  "posts/python/quickstart/dist"  # 永久链接
tags: [ "python"]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

## 添加非代码文件

https://setuptools.pypa.io/en/latest/userguide/datafiles.html

https://stackoverflow.com/questions/59071255/python-package-data-vs-data-files-vs-extra-files

对于 Python 的打包， 通常有两种， 一种是对源文件打包， 一种是安装包， 既在上传 pypi 的时候一般会执行

```bash
python setup.py sdist bdist_wheel
```

使用 pip 安装的时候一般是安装 bdist 打包出来的文件。

关于在打包中加入非程序文件，有几种方法，一种是在 `MANIFEST.in` 中加入，对于 setup.py 中也提供了 `package_data` 参数，另外对于 setuptools 还提供了特别的 `include_package_data` 的参数，接下来介绍这些参数的意义和怎么用。

### MANIFEST.in

`MANIFEST.in` 文件是针对 **源文件打包** 的，当需要把非程序文件，包括 README，css 或者 test 文件等加入时，在 `MANIFEST.in` 中指定，用于生成 MANIFEST。

MIANIFEST 会暗中自动寻找以下的文件：

- 所有 py_modules 和 packages 中没有明确说明的 python 文件
- ext_modules 或 libraries 选项中指明的 C 文件
- scripts 指明的文件
- 所有看上去像是 test 文件的，比如 tests/ *.py
- README.txt 或者 README, setup.py, setup.cfg
- package_data 中指明的文件
- data_files 中指明的文件

### package_data

package_data 是在 setup.py 中的参数，用于控制安装包里面包含的文件。

MANIFEST 控制 sdist 包含的内容，package_data 控制 bdist 包含的内容。

一般情况是，对源文件打包里面一般包含 README，tests 这些，但是对于安装包这不需要。所以分开设置。

### include_package_data

坑就是指 include_package_data，这个参数是 setuptools 特有的，但是非常容易让人误解然后勿用。setuptools 的文档中是这样写的

> If set to True, this tells setuptools to automatically include any data files it finds inside your package directories that are specified by your `MANIFEST.in` file.

设为 True 时， 打包时 setuptools 会自动加入在 `MANIFEST.in` 中指定的文件。

原本是 MANIFEST 在 setup.py 中的 package_data 寻找额外的文件的， 现在变成大家以 `MANIFEST.in` 为准了。

这会发生什么事情呢，如果你同时用了 include_package_data 和 package_data，那么 bdist 打包出来的东西会包含 package_data 中的内容，但是源代码打包的时候就会失去在 package_data 中指明的文件。

### 总结

**永远也不要用 include_package_data**

 `MANIFEST.in` 用来给源文件打包， 里面包含许多额外的信息， 比如测试文件之类的。

package_data 用于指定安装时加入的额外的文件， 不需要在 `MANIFEST.in` 中重复定义， 源文件打包的时候回自动包含这里面的文件。

```python
package_data={
      # If any package contains *.txt or *.rst files, include them:
      "": ["*.txt", "*.rst"],
      # And include any *.msg files found in the "hello" package, too:
      "hello": ["*.msg"],
  }
```
