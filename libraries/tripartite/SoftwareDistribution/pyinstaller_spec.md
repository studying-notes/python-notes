---
date: 2022-09-09T16:23:11+08:00  # 创建日期
author: "Rustle Karl"  # 作者

title: "Pyinstaller 的 Spec 文件用法"  # 文章标题
url:  "posts/python/libraries/tripartite/SoftwareDistribution/pyinstaller_spec"  # 设置网页永久链接
tags: [ "python", "pyinstaller-spec" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

## 简介

Pyinstaller 打包方式一般分为直接输入指令和利用 spec 文件进行打包。

由于直接输入指令实际就是根据指令生成 spec 文件，再根据 spec 文件的内容进行打包操作。

## 用法

创建一个 main.py 作为启动脚本，在控制台输入

```shell
pyinstaller main.py
```

可以发现路径下多了 main.spec 文件。后续我们可以修改 spec 文件里的内容，然后输入指令来进行打包操作了

```shell
pyinstaller main.spec
```

后续打包的参数越来越多，每次输入一大堆参数显然不如直接使用 spec 来的高效，所以尽量使用 spec 文件进行打包操作。

## 参数

文档示例：

```python
# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
```

| 变量 | 含义 |
| -------- | -------- |
| a | Analysis 类的实例，要求传入各种脚本用于**分析程序的导入和依赖**。a 中内容主要包括以下四部分：**scripts**，即可以在命令行中输入的 Python 脚本； **pure**，程序代码文件中的纯 Python 模块，包括程序的代码文件本身； **binaries**，程序代码文件中需要的非 Python 模块，包括 `–add-binary` 参数指定的内容； **datas**，非二进制文件，包括 `–add-data` 参数指定的内容。|
| pyz | PYZ 的实例，是一个.pyz 文件，包含了所有 pure 中的所有 Python 模块。|
| exe | EXE 类的实例，这个类是用来处理 Analysis 和 PYZ 的结果的，也是用来生成最后的 exe 可执行程序。|
| coll | COLLECT 类的实例，用于创建输出目录。在 -F 模式下，是没有 COLLECT 实例的，并且所有的脚本、模块和二进制文件都包含在了最终生成的 exe 文件中。|
| block_cipher | 加密密钥 |
| Analysis 参数 scripts | 也是第一个参数，它是一个脚本列表，可以传入多个 py 脚本，效果与命令行中指定多 py 文件相同，即 py 文件不止一个时，比如“pyinstaller xxx1.py xxx2.py”，pyinstaller 会依次分析并执行，并把第一个 py 名称作为 spec 和 dist 文件下的文件夹和程序的名称 |
| Analysis 参数 pathex | 默认有一个 spec 的目录，当我们的一些模块不在这个路径下，记得把用到的模块的路径添加到这个 list 变量里。同命令“-p DIR/ -paths DIR”. |
| Analysis 参数 datas | 作用是**将本地文件打包时拷贝到目标路径下**。datas 是一个元素为元组的列表，每个元组有两个元素，都必须是字符串类型，**元组的第一个元素为数据文件或文件夹，元组的第二个元素为运行时这些文件或文件夹的位置**。例如：datas = [( ’./src/a.txt ’, ‘./dst ’ )]，表示打包时将 "./src/a.txt" 文件添加（copy）到相对于 exe 目录下的 dst 目录中。也可以使用通配符：datas = [ ( ’ /mygame/sfx/ *.mp3 ’, ‘ sfx ’ ) ]，表示将 /mygame/sfx/ 目录下的所有.mp3 文件都 copy 到 sfx 文件夹中。也可以添加整个文件夹：datas = [ ( ’ /mygame/data ’, ‘ data ’ ) ]，表示将 /mygame/data 文件夹下所有的文件都 copy 到 data 文件夹下。同命令“-add-data”。|
| Analysis 参数 binaries | 添加二进制文件，也是一个列表，定义方式与 datas 参数一样。没具体使用过。同命令“-add-binary”。|
| Analysis 参数 hiddenimports | 指定脚本中需要隐式导入的模块，比如在 __import__、imp.find_module()、exec、eval 等语句中导入的模块，这些模块 PyInstaller 是找不到的，需要手动指定导入，这个选项可以使用多次。同命令“-hidden-import MODULENAME/ -hiddenimport MODULENAME”。|
| Analysis 参数 hookspath | 指定额外 hook 文件（可以是 py 文件）的查找路径，这些文件的作用是在 PyInstaller 运行时改变一些 Python 或者其他库原有的函数或者变量的执行逻辑（并不会改变这些库本身的代码），以便能顺利的打包完成，这个选项可以使用多次。同命令“-additional-hooks-dir HOOKSPATH”。|
| Analysis 参数 runtime_hooks | 指定自定义的运行时 hook 文件路径（可以是 py 文件），在打好包的 exe 程序中，在运行这个 exe 程序时，指定的 hook 文件会在所有代码和模块之前运行，包括 main 文件，以满足一些运行环境的特殊要求，这个选项可以使用多次。同命令“-runtime-hook RUNTIME_HOOKS”。|
| Analysis 参数 excludes | 指定可以被忽略的可选的模块或包，因为某些模块只是 PyInstaller 根据自身的逻辑去查找的，这些模块对于 exe 程序本身并没有用到，但是在日志中还是会提示“module not found”，这种日志可以不用管，或者使用这个参数选项来指定不用导入，这个选项可以使用多次。同命令“-exclude-module EXCLUDES”。|
| exe 参数 console | 设置是否显示命令行窗口，同命令 -w/-c。 |
| exe 参数 icon | 设置程序图标，默认 spec 是没有的，需要手动添加，参数值就是图片路径的字符串。同命令“命令 -i/ -icon”。|

## 问题

### 加密

变量 block_cipher，主要是防止 exe 被反编译。

```python
block_cipher = pyi_crypto.PyiBlockCipher(key='123456789')
```

[如何安全地进行编译和反编译](https://mp.weixin.qq.com/s?__biz=MzAxMTkwODIyNA==&mid=2247507585&idx=2&sn=49927935a8103123e9138d8dc0665c1c&chksm=9bbb7b6eacccf278ee22791d05804180fddeacd2bcbad4974fb84023985a34b379c262dabc92&xtrack=1&scene=0&subscene=10000&clicktime=1602025341&enterid=1602025341&ascene=7&devicetype=android-29&version=3.0.36.2008&nettype=WIFI&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&exportkey=AaKPf3QPE7vXCst05p67Hzc%3D&pass_ticket=ZEu6DU5vbKl5LzJ%2BB0psE4ZzaQt5Ay8207BKqROAE3QaDt0iwhDRvtvgNurGX1t1&wx_header=1&platform=win)

```python

```

```shell

```
