---
date: 2022-02-07T08:30:40+08:00
author: "Rustle Karl"

title: "Black - Python 代码格式化工具"
url:  "posts/python/docs/others/black"  # 永久链接
tags: [ "python"]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

## 常见格式化工具

- [black](https://github.com/psf/black) star 25.3k
- [autopep8](https://github.com/hhatto/autopep8) star 4k
- [yapf](https://github.com/google/yapf) star 12.3k

## Black 简介

Black 自称“零妥协代码格式化工具（The uncompromising code formatter）”。 Black 是目前最广受好评的 Python 代码格式化工具。

```python
# 格式化前
from seven_dwwarfs import Grumpy, Happy, Sleepy, Bashful, Sneezy, Dopey, Doc
x = {  'a':37,'b':42,

'c':927}

x = 123456789.123456789E123456789

if very_long_variable_name is not None and \
 very_long_variable_name.field > 0 or \
 very_long_variable_name.is_debug:
 z = 'hello '+'world'
else:
 world = 'world'
 a = 'hello {}'.format(world)
 f = rf'hello {world}'
if (this
and that): y = 'hello ''world'#FIXME: https://github.com/python/black/issues/26
class Foo  (     object  ):
  def f    (self   ):
    return       37*-2
  def g(self, x,y=42):
      return y
def f  (   a: List[ int ]) :
  return      37-a[42-u :  y**3]
def very_important_function(template: str,*variables,file: os.PathLike,debug:bool=False,):
    """Applies `variables` to the `template` and writes to `file`."""
    with open(file, "w") as f:
     ...
# fmt: off
custom_formatting = [
    0,  1,  2,
    3,  4,  5,
    6,  7,  8,
]
# fmt: on
regular_formatting = [
    0,  1,  2,
    3,  4,  5,
]
```

```python
# 使用 Black-v21.9b0 格式化后
from seven_dwwarfs import Grumpy, Happy, Sleepy, Bashful, Sneezy, Dopey, Doc

x = {"a": 37, "b": 42, "c": 927}

x = 123456789.123456789e123456789

if (
    very_long_variable_name is not None
    and very_long_variable_name.field > 0
    or very_long_variable_name.is_debug
):
    z = "hello " + "world"
else:
    world = "world"
    a = "hello {}".format(world)
    f = rf"hello {world}"
if this and that:
    y = "hello " "world"  # FIXME: https://github.com/python/black/issues/26


class Foo(object):
    def f(self):
        return 37 * -2

    def g(self, x, y=42):
        return y


def f(a: List[int]):
    return 37 - a[42 - u : y ** 3]


def very_important_function(
    template: str,
    *variables,
    file: os.PathLike,
    debug: bool = False,
):
    """Applies `variables` to the `template` and writes to `file`."""
    with open(file, "w") as f:
        ...


# fmt: off
custom_formatting = [
    0,  1,  2,
    3,  4,  5,
    6,  7,  8,
]
# fmt: on
regular_formatting = [
    0,
    1,
    2,
    3,
    4,
    5,
]
```

经过 Black 重新格式化后，代码立刻就清爽舒适了很多。事实上，Black 有一套经过反复讨论、仔细研究得出的非常详尽的 Python 代码格式化风格。

## 安装

```shell
pip install black
```

如果想在 [Jupyter Notebooks](https://jupyter.org/) 中使用，则可以通过如下代码安装：

```shell
pip install black[jupyter]
```

也可以通过下面的命令从 GitHub 安装：

```shell
pip install git+git://github.com/psf/black
```

## 简单使用

### 作为脚本运行

```shell
black {source_file_or_directory}
```

### 作为 Python 包运行

如果将 Black 作为脚本运行不起作用，您可以尝试将其作为包运行：

```shell
python -m black {source_file_or_directory}
```

### 跳过字符串格式化

Black 会默认将字符串格式化为使用双引号包裹，但有些项目已经使用了单引号的规范且不应修改为双引号，就需要加上一个 `-S` / `--skip-string-normalization` 的选项。

```shell
black -S {source_file_or_directory}
```

## 集成到 IDE / 编辑器中

相比于每次都专门打开一个终端，手动使用命令行调用 Black 格式化代码，我们更希望能把 Black 集成到我们常用的 IDE / 编辑器中，不需要离开写代码的界面即可完成格式化操作。

### 在 PyCahrm 中使用

[Black 官方文档](https://black.readthedocs.io/en/stable/integrations/editors.html#pycharm-intellij-idea)中给出了在 PyCharm（或 IntelliJ IDEA）中配置使用 Black 的方法：

#### 确认 Black 安装位置

在 macOS / Linux / BSD 上：

```shell
$ which black
/usr/local/bin/black  # 可能的位置
```

在 Windows 上：

```shell
$ where black
C:\Developer\anaconda38\Scripts\black.exe  # 可能的位置
```

如果是使用 Pycahrm 建立的虚拟环境，则直接使用 `$PyInterpreterDirectory$/black` 作为程序路径。

#### 在 PyCharm 中添加外部工具

打开 文件 -> 设置 -> 工具 -> 外部工具

File -> Settings -> Tools -> External Tools

![](http://dd-static.jd.com/ddimg/jfs/t1/223395/25/10006/57053/62006a86E1ab720ae/73ba85311c0c4bce.png)

创建工具

- 名称：Black
- 描述：Python 代码格式化工具
- 程序：「上一小节得到的安装位置」
- 参数：`$FilePath$`
- 工作目录：`$ProjectFileDir$`

![](http://dd-static.jd.com/ddimg/jfs/t1/116637/22/20454/31635/62006ab9Ec43d59d4/8e42a2528e6b518b.png)

如果需要[自定义其他选项](https://muzing.top/posts/a29e4743/#命令行选项)，写在 `$FilePath$` 前即可，比如代表「取消格式化字符串为双引号包裹”」的选项 `-S`：

![](http://dd-static.jd.com/ddimg/jfs/t1/140531/11/21176/31274/62006abeEbfc28cb2/1733d010fc7d657b.png)

#### 使用

在已经打开的代码编辑界面（或项目文件树的某个目录上）鼠标右键，找到 External Tools -> Black，点击即可。

![](http://dd-static.jd.com/ddimg/jfs/t1/136414/19/21735/117147/62006ac2Ecaba3b75/5f992b073cdd21e5.png)

#### 设置快捷键

还可以在 设置 -> 键盘映射 -> 外部工具 -> Black 上右键，打开编辑快捷键的菜单，添加键盘快捷键：

![设置快捷键](http://dd-static.jd.com/ddimg/jfs/t1/212020/34/12018/91956/62006ac7E509acc44/5d3fedd1342a69cf.png)

如果已经习惯了 PyCharm 默认的 `Ctrl + Alt + L` 快捷键格式化代码，那么可以这样设置：

1. 在 主菜单 -> 代码 -> 重新格式化代码 中删去快捷键
2. 给 外部工具 -> External Tools -> Black 设置键盘快捷键`Ctrl + Alt + L`

#### 保存文件时自动格式化

1. 确保已经安装了 [File Watchers](https://plugins.jetbrains.com/plugin/7177-file-watchers) 插件
2. 进入 设置 -> 工具 -> File Watchers，点击 + 以添加一个新的 watcher：
   - Name: Black
   - File type: Python
   - Scope: Project Files
   - Program: 上一小节得到的安装位置
   - Arguments: `$FilePath$`
   - Output paths to refresh: `$FilePath$`
   - Working directory: `$ProjectFileDir$`
3. 在高级选项中：
   - 取消勾选 “Auto-save edited files to trigger the watcher”
   - 取消勾选 “Trigger the watcher on external changes”

### 在 VS Code 中使用

[VS Code 官方文档介绍](https://code.visualstudio.com/docs/python/editing#_formatting)

#### 安装 Python 插件

首先确保已经在 VS Code 中安装了 Python 插件。如果没有安装，则在 VS Code 中按下 `Ctrl + P` ，并输入如下命令：

```shell
ext install ms-python.python
```

或者直接在扩展商店中搜索 Python 并安装。

![在 VS Code 中安装 Python 插件](http://dd-static.jd.com/ddimg/jfs/t1/223341/18/10332/229664/62006accE5473b094/ab524e0164129418.png)

#### 配置 Python 扩展

按下 `Ctrl + ,` ，打开 VS Code 设置

![](http://dd-static.jd.com/ddimg/jfs/t1/85096/21/21087/121321/62006ad2Efc00ac57/fdf1c283337ecae3.png)

在「设置」中搜索 python formatting provider ，然后把默认的 autopep8 改为 black 即可。

![](http://dd-static.jd.com/ddimg/jfs/t1/206507/15/16934/45554/62006ad9Ea39f8293/7ab5f186572d09c9.png)

#### 保存文件时自动格式化代码

在「设置」界面搜索 format on save ，可以勾选打开保存时格式化文件的功能。

![](http://dd-static.jd.com/ddimg/jfs/t1/89958/21/21122/80151/62006adcE653e4b24/7a9561ca8e25e4de.png)


#### 取消格式化为双引号包裹字符串

在「设置」界面的右上角打开 `settings.json` 配置文件

![打开 json 配置文件](http://dd-static.jd.com/ddimg/jfs/t1/96071/26/21838/35808/62006ae0Ee18deb10/736880c30dca7313.png)

在配置文件中添加一行

```json
"python.formatting.blackArgs": [
        "--skip-string-normalization"
    ]
```

![](http://dd-static.jd.com/ddimg/jfs/t1/220509/12/11928/25997/62006ae4Ea67645b5/70fdf7706e6facf5.png)

注意每个人的 `settings.json` 配置文件都有所不同，行号不太一样，在文件末尾新建一行添加即可。

## 详细使用

> 摘录翻译自官方文档 [Usage and Configuration - The basics](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html#usage)

Black 是一个工作良好的 Unix 风格命令行工具：

- 当没有原文件传入时什么都不会做
- 如果使用 `-` 作为文件名，则将会从标准输入读取并写入到标准输出
- 只向用户输出标准错误信息
- 当没有内部错误发生时，退出代码为 0 （除非使用了 `--check` 选项）

### 命令行选项

Black 倾向于“独裁”，故意限制并很少添加选项，然而这却反而成了它备受赞赏的一点——既然要统一格式，就不应该有太多个性化选项。

下面列出了 Black 的 Help 输出，并尽我所能做了翻译：

```shell
$ black --help
使用： black [OPTIONS] SRC ...

  零妥协的代码格式化工具。

选项：
  -c, --code TEXT                 将传入的代码作为字符串格式化。
  
  -l, --line-length INTEGER       每行允许的字符数。
                                  [默认值： 88]

  -t, --target-version            [py27|py33|py34|py35|py36|py37|py38|py39]
                                  Black 的输出应该支持的 Python 版本
                                  [默认值：每个文件自动检测]

  --pyi                           不考虑文件扩展名，将所有输入文件格式化为 typing stubs
                                  （当使用来自标准输入的管道时很有用）。

  --ipynb                         不考虑文件扩展名，将所有输入文件格式化为 Jupyter
                                  Notebooks 风格（当使用来自标准输入的管道时很有用）。
  
  -S, --skip-string-normalization 不要标准化字符串引号或前缀。
  
  -C, --skip-magic-trailing-comma 不要将尾随逗号作为分割行的理由。
  
  --check                         不要写回文件，只返回状态。
                                  返回代码 0 意味着没有任何改变。
                                  返回代码 1 意味着有些文件将被重新格式化。
                                  返回代码 123 意味着存在 internal error 内部错误。
  
  --diff                          不要写回文件， 只是使用 stdout 标准输出显示
                                  每个文件的 diff 差异。
  
  --color / --no-color            显示彩色的 diff。 只有当使用了`--diff` 选项才生效。
  
  --fast / --safe                 如果给定了 --fast，则跳过 temporary sanity
                                  检查。 [默认值： --safe]
  
  --required-version TEXT         需要运行特定版本的 Black （用于在不同环境上得到同样的
                                  结果，比如使用一个 pyproject.toml 文件）。
  
  --include TEXT                  匹配递归搜索中应包含的文件和目录的正则表达式。
                                  空值意味着包含所有文件（无论文件名是什么）。
                                  对所有平台上的目录使用正斜杠（在 Windows 上亦是如此）。 
                                  首先匹配要排除的项，然后匹配包含项。
                                  [默认值： (\.pyi?|\.ipynb)$]
  
  --exclude TEXT                  匹配递归搜索中应排除的文件和目录的正则表达式。
                                  空值意味着不排除任何路径。 
                                  对所有平台上的目录使用正斜杠（在 Windows 亦是如此）。
                                  首先匹配要排除的项，然后匹配包含项。
                                  [默认值： /(\.direnv|\.eggs|\.git|\.h
                                  g|\.mypy_cache|\.nox|\.tox|\.venv|venv|\.svn
                                  |_build|buck-out|build|dist)/]
  
  --extend-exclude TEXT           类似 --exclude，但在排除的文件和目录之上
                                  添加了额外的文件和目录。（如果您只是想简单地添加到
                                  默认值，这会很有用）
  
  --force-exclude TEXT            类似 --exclude，但是与此正则表达式匹配的文件和目录
                                  将被排除，即使它们作为参数显式传递。
  
  --stdin-filename TEXT           通过 stdin 标准输入传递时的文件名。
                                  有助于确保 Black 在某些依赖使用 stdin 的编辑器上
                                  尊重 --force-exclude 选项。
  
  -q, --quiet                     不向 stderr 输出非报错信息。
                                  错误信息仍然会被输出； 
                                  使用 2>/dev/null 关闭这些信息。
  
  -v, --verbose                   还向 stderr 输出文件未更改或因为排除模式被忽略的信息。
  
  --version                       显示版本并退出。
  
  --config FILE                   从 FILE 路径读取配置。
  
  -h, --help                      显示本帮助信息并退出。
```

### 代码输入选择

#### 从标准输入读取

Black 支持从 stdin 标准输入中读取并格式化代码，并将结果输出至 stdout 标准输出。只需把 `-` 作为传入路径即可。

```shell
$ echo "print ( 'hello, world' )" | black -
print("hello, world")
reformatted -
All done! ✨ 🍰 ✨
1 file reformatted.
```

**提示**：如果您需要 Black 把 stdin 标准输入视作一个直接通过 CLI 传来的文件，请使用`--stdin-filename` 选项。这有助于确保 Black 在某些依赖使用 stdin 的编辑器上考虑 `--force-exclude` 选项。

#### 作为字符串

您也可以通过 `-c` / `--code` 选项来把代码作为字符串传递

```shell
$ black --code "print ( 'hello, world' )"
print("hello, world")
```

### 写回与报告

默认情况下，Black 会原地重新格式化给定的文件。有时候您只需要知道 Black 将会做什么，而无需真的重新写入 Python 文件中。

有两种方式实现这个效果，分别通过各自的选项独立开启，也可以同时启用。

#### 退出代码

传递 `--check` 参数将使 Black 以如下代码退出：

- 代码 0 ：没有任何文件将被改变
- 代码 1 ：有些文件将被重新格式化
- 代码 123：出现内部错误

```shell
$ black test.py --check
All done! ✨ 🍰 ✨
1 file would be left unchanged.
$ echo $?
0

$ black test.py --check
would reformat test.py
Oh no! 💥 💔 💥
1 file would be reformatted.
$ echo $?
1

$ black test.py --check
error: cannot format test.py: INTERNAL ERROR: Black produced code that is not equivalent to the source.  Please report a bug on https://github.com/psf/black/issues.  This diff might be helpful: /tmp/blk_kjdr1oog.log
Oh no! 💥 💔 💥
1 file would fail to reformat.
$ echo $?
123
```

#### 差异比较

传递 `--diff` 参数以使 Black 打印出差异，表明其将要做出的更改。这将会输出到 stdout 标准输出，因此很容易捕获。

使用 `--color` 来开启彩色差异比较。

```shell
$ black test.py --diff
--- test.py     2021-03-08 22:23:40.848954 +0000
+++ test.py     2021-03-08 22:23:47.126319 +0000
@@ -1 +1 @@
-print ( 'hello, world' )
+print("hello, world")
would reformat test.py
All done! ✨ 🍰 ✨
1 file would be reformatted.
```

### 详细输出

一般来说，Black 尽可能生成适量的输出，在使用性和简洁性之间取得平衡。默认情况下，Black 会输出已修改的文件和错误消息，再加上一个简短的摘要。

```shell
$ black src/
error: cannot format src/black_primer/cli.py: Cannot parse: 5:6: mport asyncio
reformatted src/black_primer/lib.py
reformatted src/blackd/__init__.py
reformatted src/black/__init__.py
Oh no! 💥 💔 💥
3 files reformatted, 2 files left unchanged, 1 file failed to reformat.
```

传递 `-v` / `--verbose` 选项会让 Black 也输出有关未更改的文件或由于排除模式而被忽略的文件的信息。如果 Black 使用了配置文件，则会输出一条蓝色的消息，详细说明它正在使用哪个配置文件。

```shell
$ black src/ -v
Using configuration from /tmp/pyproject.toml.
src/blib2to3 ignored: matches the --extend-exclude regular expression
src/_black_version.py wasn't modified on disk since last run.
src/black/__main__.py wasn't modified on disk since last run.
error: cannot format src/black_primer/cli.py: Cannot parse: 5:6: mport asyncio
reformatted src/black_primer/lib.py
reformatted src/blackd/__init__.py
reformatted src/black/__init__.py
Oh no! 💥 💔 💥
3 files reformatted, 2 files left unchanged, 1 file failed to reformat
```

传递 `-q` / `--quiet` 选项会让 Black 停止输出所有的非严重信息。此时错误信息仍然会输出（这可以通过 `2>dev>null` 关闭）。

```shell
$ black src/ -q
error: cannot format src/black_primer/cli.py: Cannot parse: 5:6: mport asyncio
```

### 版本

您可以使用 `--version` 标志来检查您已经安装的 Black 版本。

```shell
$ black --version
black, version 21.9b0
```

还提供了要求运行特定版本的选项。

```shell
$ black --required-version 21.9b0 -c "format = 'this'"
format = "this"
$ black --required-version 31.5b2 -c "still = 'beta?!'"
Oh no! 💥 💔 💥 The required version does not match the running version!
```

在安装了不一定相同的版本的多个环境中运行 Black 时，这个选项非常有用。 可以在配置文件中设置此选项，以获得跨环境的一致结果。

## 通过文件配置

> 翻译自[官方文档](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html#configuration-via-a-file)

Black 能够从 `pyproject.toml` 文件中读取对于特定项目其命令行选项的默认值。 这对为您的项目指定自定义 `--include` 和 `--exclude/--force-exclude/--extend-exclude` 模式特别有用。

**提示**：当您在问自己“我是否需要配置任何东西”时，回答是否定的。Black 的一切皆为合理的默认值。使用这些默认选项将会使您的代码符合许多其他 Black 格式的项目。

### pyproject.toml 文件

[PEP 518](https://www.python.org/dev/peps/pep-0518/) 定义了 `pyproject.toml` 为用于存储 Python 项目构建系统需求（build system requirements）的配置文件。在 [Poetry](https://python-poetry.org/) 或 [Flit](https://flit.readthedocs.io/en/latest/) 的帮助下，它能够取代 `setup.py` 和 `setup.cfg` 文件。

### 查找路径

默认情况下，Black 将从命令行上传递的所有文件和目录的公共基目录开式查找 `pyproject.toml` 。如果不存在，则查找父目录。当它找到文件，或者一个 `.git` 目录，或一个 `.hg` 目录，或文件系统的根目录时，则停止查找，以先找到的为准。

如果您正在从标准输入进行格式化，Black 将从当前工作目录开始查找配置。

您可以使用一个存储在您的家目录的特定位置的“全局”配置。这是一个备用配置，即当且仅当 Black 未找到上述的任何配置时才会使用。根据您的操作系统，此文件的存储位置应为：

- Windows： `~\.black`
- 类Unix系统 （Linux, MacOS等）： `$XDG_CONFIG_HOME/black` （如果没有设置 `XDG_CONFIG_HOME` 环境变量，则为 `~/.config/black`）

注意，这些是 TOML 文件本身的路径（意味着它们不应该被命名为 `pyproject.toml` ），而不是您存储配置的目录。这里 `~` 代表您的家目录的绝对路径。在 Windows 上，这会是类似于 `C:\\Users\UserName` 的东西。

您还可以使用 `--config` 选项来显示指定您想使用的特定文件。在这种情况下，Black 不会寻找任何其他文件。

如果您在运行时使用了 `--verbose` 选项，如果找到并使用了配置文件，您将会看到一条蓝色的消息。

请注意，`blackd` 将不会使用 `pyproject.toml` 配置。

### 配置格式

如文件扩展名所示，`pyproject.toml` 是一个 [TOML](https://github.com/toml-lang/toml) 文件。它包含不同工具对应的不同的部分。Black 使用 `[tool.black]` 部分。选项的键与命令行选项中的长名称相同。

请注意，对于正则表达式，您必须在 TOML 中使用单引号字符串。它相当于 Python 中的 r-strings 。Black 将多行字符串视为冗长的正则表达式。使用 `[]` 标明重要的空格字符。

一个 `pyproject.toml` 的例子：

```ini
[tool.black]
line-length = 88
target-version = ['py37']
include = '\.pyi?$'
extend-exclude = '''
# A regex preceded with ^/ will apply only to files and directories
# in the root of the project.
^/foo.py  # exclude a file named foo.py in the root of the project (in addition to the defaults)
'''
```

### 配置项使用层级关系

命令行选项具有默认值，可以在 `--help` 中查看（见本文[上一小节](https://muzing.top/posts/a29e4743/#命令行选项)）。`pyproject.toml` 会覆盖默认配置。而用户通过命令行输入的选项具有最高优先级，将覆盖前两者。

Black 在整个运行过程中只会使用一个 `pyproject.toml` 文件。 它不会查找多个文件，也不会从文件层次结构的不同级别组合配置。

## The Black Code Style

我将 [The *Black* code style - Current style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) 英文文档全部做了翻译，感兴趣的小伙伴可以仔细阅读一下。

### 代码风格

Black 原地重新格式化整个文件（即直接将重新格式化的结果写回并覆盖原文件）。代码风格配置可选项故意限制得很少，且很少添加新选项。除了神奇的尾随逗号（trailing comma）和保留换行符，它不会考虑以前的代码格式。以 `# fmt: off` 开头并以 `# fmt: on` 结尾的代码块，或以 `# fmt: skip` 结尾的行不会被重新格式化。`# fmt: on/off` 必须在相同级别的缩进位置。出于礼貌，它也对 [YAPF](https://github.com/google/yapf) 的块注释具有相同的效果。

#### 换行方式

Black 会忽略先前的格式，并对代码应用统一的空格和换行方式。空格的风格可以总结为：取悦 `pycodestyle` 。Black 使用的代码风格可以视为是 PEP 8 的严格子集。

对于换行，Black 试着让每一行都只有一个完整的表达式或简单语句。如果这符合指定的行长度就更好了。

```python
# in:

j = [1,
     2,
     3
]

# out:

j = [1, 2, 3]
```

否则，Black 将查看第一个外部括号匹配的内容，并将其放在单独的缩进行中。

```python
# in:

ImportantClass.important_method(exc, limit, lookup_lines, capture_locals, extra_argument)

# out:

ImportantClass.important_method(
    exc, limit, lookup_lines, capture_locals, extra_argument
)
```

如果这仍然不符合要求，它将使用相同的规则进一步分解内部表达式，每次在匹配的括号处缩进。 如果匹配括号对的内容是逗号分隔的（如参数列表，字典文字等），那么 Black 将首先尝试将它们与对应匹配的括号保持在同一行。 如果仍然不行，它会将这些内容放在单独的行中。

```python
# in:

def very_important_function(template: str, *variables, file: os.PathLike, engine: str, header: bool = True, debug: bool = False):
    """Applies `variables` to the `template` and writes to `file`."""
    with open(file, 'w') as f:
        ...

# out:

def very_important_function(
    template: str,
    *variables,
    file: os.PathLike,
    engine: str,
    header: bool = True,
    debug: bool = False,
):
    """Applies `variables` to the `template` and writes to `file`."""
    with open(file, "w") as f:
        ...
```

Black 更喜欢括号而不是反斜杠，如果找到反斜杠则会删除：

```python
# in:

if some_short_rule1 \
  and some_short_rule2:
      ...

# out:

if some_short_rule1 and some_short_rule2:
  ...


# in:

if some_long_rule1 \
  and some_long_rule2:
    ...

# out:

if (
    some_long_rule1
    and some_long_rule2
):
    ...
```

反斜杠和多行字符串是 Python 语法中最主要的破坏缩进的两项。永远不要使用反斜杠，它们用于强制换行（即在原本换行将引起语法错误的地方换行），这使得它们令人困惑且难以修改。所以 Black 极力避免反斜杠。

如果您在您的代码中使用了反斜杠，这表明您只要稍作重构就可以明显优化代码。希望上面的例子能有所启发。

右括号总是缩进，并且添加一个尾随逗号。这种格式产生更小的差异：当添加或删除一个元素时，总是只占一行。此外，使右括号在代码的两个不同部分，而不是相同的缩进级别（比如上面那个例子中的参数列表和文档字符串），使得分隔更清晰。

如果组合数据结构（元组、列表、集合、字典），或者一行 “from” 导入无法适应分配的长度，则 Black 总是把每一项拆分到单独的一行中。这最大限度地减小了差异，同时使得阅读代码的人能够找到引入特定条目的 commit 。这还使得 Black 和带有现成的 `black` 配置文件或手动配置的 [isort](https://black.readthedocs.io/en/stable/guides/using_black_with_other_tools.html#isort) 兼容。

#### 行长度

Black 默认行长度比较特殊，为每行 88 个字符，恰好比 80 多 10% 。这个行长度下的文件总长度要比坚持使用 80（最流行的），或者甚至 79 （标准库使用的）要短的多。总的来说，90 似乎是明智之选。

如果您按照自己的代码规范限制行长度，您可以通过 `--line-length` 传递一个较小的数字。 Black 会尽量尊重该选项。 但是，有时这会造成冲突。 在极少数情况下，自动格式化的代码行长度将超出您设置的限制。

您也可以增加行长度，但请记住，有视力障碍的人阅读超过 100 个字符的行会很困难。 这还会对典型屏幕分辨率下的并排差异审查造成不便。 太长的行也使得在文档或幻灯片中整齐地呈现代码变得更加困难。

如果您在使用 Flake8 ，您可以将 `max-line-length` 提高到88，然后几乎忘掉这些。但是更好的选择是使用 [Bugbear](https://github.com/PyCQA/flake8-bugbear) 的 B950 警告替代 E501，然后提高行最大长度到 88（或者您在 Black 上使用的 `--line-length`），这会更和 Black 的 *“尽可能尊重 `--line-length` ，但是达不到也不要强求”* 保持一致。您会这样做：

```python
[flake8]
max-line-length = 88
...
select = C,E,F,W,B,B950
extend-ignore = E203, E501
```

可以在本文档中进一步了解 E203 被禁用的原因。如果您对 B950 背后的原因感到好奇，[Bugbear 的文档](https://github.com/PyCQA/flake8-bugbear#opinionated-warnings)对此进行了解释。“就像高速公路上的限速，超速几迈不会有什么麻烦。”

**一个最精简的、兼容 Black 的 Flake8 配置：**

```ini
[flake8]
max-line-length = 88
extend-ignore = E203
```

#### 空白行

Black 避免使用无用的空行。这是符合 PEP 8 精神的，即函数内的空行应该谨慎使用。

Black 允许在函数内有单空行，以及原编辑器中在模块级别中使用的单空行和双空行（除非它们在括号内的表达式中）。由于这些表达式总是被重新格式化以占用最小空间，所以这些空行会丢失。

Black 还会在函数定义之前和之后插入适当的空行。内部函数前后一行，模块级别的函数和类前后两行。Black 不会在函数 / 类定义和紧挨着给定函数 / 类之前的独立注释之间插入空行。

Black 将在类级别的文档字符串和第一个后续字段或方法之间强行控制为一个空行，这符合 [PEP 257](https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings) 。

Black 不会在函数文档字符串后插入空行，除非由于内部函数紧随其后，需要空行分隔。

#### 注释

Black 不格式化注释内容，但它会在同一行的代码和注释之间强制使用两个空格，并在注释文本开始之前添加一个空格。Black 会考虑某些需要特定间距规则的注释类型：文档注释（`#: comment`）、section comments with long runs of hashes、Spyder 的 cell 。有时可能因为格式更改而移动注释，这可能会破坏为其分配特殊含义的工具的执行效果。哈希运算后的不间断空格也被保留。更多讨论，请看[格式化前后的 AST](https://muzing.top/posts/a29e4743/#格式化前后的-ast) 一节。

#### 尾随逗号

Black 将向由逗号分隔的表达式添加尾随逗号，每个元素占据单独的一行。这包括函数声明。

添加尾随逗号的一个例外情况是，函数声明包括 `*`， `*args`，或 `**kwargs`。在这种情况下，尾随逗号只能在 Python 3.6 上安全使用。Black 将会检测您的文件是否已经是只兼容 3.6+ 并在这种情况下使用尾随逗号。 Black 的判断方法是，它会在带有星号的函数声明中查找 f-strings和尾随逗号的现有用法。换言之，如果您想在这种情况下使用尾随逗号而 Black 没有意识到这是安全的，那么在那里手动添加，Black 会保留它。

已经存在的尾随逗号提示 Black 始终将当前括号对的内容分解为每行一个项目。在下一小节中的[神奇的尾随逗号](https://muzing.top/posts/a29e4743/#神奇的尾随逗号)获取更多关于此的信息。

#### 字符串

相比于单引号（ `'` 和 `'''`）， Black 更倾向于双引号（`"` 和 `"""`）。只要不会导致出现更多的反斜杠转义，Black 就会用双引号替换单引号。

Black 还标准化了字符串前缀，使它们始终小写。最重要的是，如果您的代码已经是只用于 Python 3.6+ ，或者使用了 `unicode_literals` 未来导入，Black 将会从字符串前缀中删除 `u` ，因为它在这些情况下毫无意义。

美观是标准化到一个单一形式的引用的主要原因。在各处都使用相同风格的引用可以减少读者注意力分散。这还将使 Black 的未来版本能够合并以同一行结尾的连续字符串文字（详细有关信息，请参阅 [#26](https://github.com/psf/black/issues/26)）

为何选用双引号？他们估计在英文文本中会有撇号。它们符合 [PEP 257](https://www.python.org/dev/peps/pep-0257/#what-is-a-docstring) 中描述的文档字符串标准。无论使用何种字体和语法高亮，双引号（`""`）中的空字符串都不可能与单引号混淆。最重要的是，字符串使用双引号，与 Python 经常与之交互的 C 语言一致。

在某些键盘布局（如美国英语）上，键入单引号比双引号（需要使用 Shift 键）更容易一些。 我的建议是继续使用更快的输入方式，让 Black 去处理转换。

如果您在一个存在预先已有字符串约定（例如很流行的[在数据上使用单引号，人类阅读的字符串上使用双引号](https://stackoverflow.com/a/56190)）的大型项目上使用 Black ，您可以在命令行上传递 `--skip-string-normalization` 参数。这旨在采纳意见，应该避免将其用在新项目上。

作为一个实验选项（可以通过 `--experimental-string-processing` 启用），Black 拆分长字符串（在适当的情况下使用括号），并合并短字符串。拆分时，不需要格式化的 f-字符串部分将转换为纯字符串。当用户创建的分割不超过行长度限制时，它们将会被保留。用于表示行继续的反斜杠将被转换为带括号的字符串。不必要的括号将被删除。由于该功能是实验性的，故强烈建议您提供反馈和问题报告！

Black 还会处理文档字符串。首先会针对引用和其中的文本更正文档字符串的缩进，但是文本中的相对缩进会被保留。每行多余的尾随空格和文档字符串末尾的不必要的新行都会被删除。所有前导制表符都转换为空格，但保留文本内的制表符。删除单行文档字符串的前导/尾随空格。

#### 数字文字量

Black 将大多数数字文字量（numeric literals）标准化为语法部分使用小写字母，数字本身使用大写字母：`0xAB` 替换 `0XAB` 、`1e10` 替换 `1E10`。

#### 二元运算符与换行

在将代码块拆分为多行时， Black 将在二元运算符之前换行。这是为了符合 [PEP 8](https://www.python.org/dev/peps/pep-0008/#should-a-line-break-before-or-after-a-binary-operator) 中最近的更改：强调这种方法提高了可读性。

#### 切片类型

[PEP 8 推荐](https://www.python.org/dev/peps/pep-0008/#whitespace-in-expressions-and-statements)将切片中的 `:` 视为具有最低优先级的二元运算符，并在两边留下相同数量的空格，除非一个参数被省略（例如`ham[1 + 1 :]`）。它建议对于“简单表达式”，`:` 运算符周围不要加空格（`ham[lower:upper]`）；对于“复杂表达式”则添加额外空格（`ham[lower : upper + offset]`）。Black 把变量名之外的东西都视为“复杂”（`ham[lower : upper + 1]`）。它还指出，对于扩展的切片操作，除非省略了一个参数（`ham[1 + 1 ::]`），两个 `:` 运算符必须拥有相同的间距。Black 始终强制执行这些规则。

这些行为可能会在 Flake8 等强制风格指导工具中引发 `E203 whitespace before ':'` 警告。由于 `E203` 不符合 PEP 8，您应该设置 Flake8 忽略这些警告。

#### 括号

在 Python 语法中，有些括号是可有可无的。任何表达式都可以用一对括号包裹组成一个原子。下面是几个有趣的例子：

- `if (...):`
- `while (...):`
- `assert (...), (...)`
- `from X import (...)`
- 赋值，比如：
  - `target = (...)`
  - `target: type = (...)`
  - `some, *un, packing = (...)`
  - `augmented += (...)`

在这些情况下，当整个语句适合一行时，或者如果内部表达式没有任何分隔符、可以进一步拆分，则会删除括号。如果只有一个分隔符，并且表达式以括号开头或结尾，括号也可以直接省略，因为现有的括号对无论如何都会整齐地组织表达式。否则，将添加括号。

请注意，Black 不会添加或删除任何额外的嵌套括号，为了清晰或进一步组织代码，您可能会希望使用这些括号。例如，这些括号不会被删除：

```python
return not (this or that)
decision = (maybe.this() and values > 0) or (maybe.that() and values < 0)
```

#### 调用链

许多流行的 API（比如 ORM）使用调用链。这种 API 风格以流畅的接口闻名。Black 通过将调用或索引操作后面的点视作优先级非常低的分隔符来格式化这些代码。啰嗦无益，直接看代码：

```python
def example(session):
    result = (
        session.query(models.Customer.id)
        .filter(
            models.Customer.account_id == account_id,
            models.Customer.email == email_address,
        )
        .order_by(models.Customer.id.asc())
        .all()
    )
```

#### 存根文件

[PEP 484](https://www.python.org/dev/peps/pep-0484) 描述了 Python 中类型提示的语法。类型的用例之一是，为不能直接包含它们的模块提供类型注释（它们可能是用 C 编写的，或者它们可能是第三方的，或者它们的实现可能过于动态，等等）。

为了解决这个问题，可以使用[以`.pyi`为文件扩展名的存根文件](https://www.python.org/dev/peps/pep-0484/#stub-files)来描述外部模块的类型信息。这些存根文件省略了它们描述的类和函数的实现，而是只包含文件的结构（列出全局变量、函数和类及其成员）。这些文件的推荐代码风格比 PEP 8 更简洁：

- 倾向于让 `...` 与类/函数签名处于同一行；
- 避免在单个类中的连续模块级函数、名称或方法和字段之间出现垂直空白；
- 在顶级类定义之间使用一个空行，如果类非常小，则不使用。

Black 执行上述规则。目前尚未有强制性的格式化 `.pyi` 文件的指南，但可能会出现在格式化程序的未来版本中：

- 所有的函数体都应该是空的（包含 `...` 而不是函数体）；
- 不使用文档字符串；
- 相比 `pass` 更倾向于使用 `...` ；
- 对于带有默认值的参数，使用 `...` 而不是实际的默认值；
- 避免在类型注释中使用字符串文字，存根文件本身支持前向引用（如带有 `from __future__ import annotations` 的 Python 3.7 代码）；
- 使用变量注释而不是类型注释，即使是针对旧版本 Python 的存根；
- 对于默认为 `None` 的参数，显式使用 `Optional[]` ；
- 使用 `float` 替换 `Union[int, float]` 。

### 实用主义

早期版本的 Black 在某些方面是绝对主义者，紧跟最初作者的步伐。这在当时很好，使实现更简单，而且当时本来也没有多少用户。没有收到很多边缘案例的报告。作为一个成熟的工具，Black 确实对它的规则做了一些例外处理。本节记录了这些例外，以及其发生的原因。

#### 神奇的尾随逗号

Black 在进行格式化时，通常不考虑已有的格式。

然而在某些情况下，您在代码中写了一个简短的集合或函数调用，但您估计未来会添加新的项，例如：

```python
TRANSLATIONS = {
    "en_us": "English (US)",
    "pl_pl": "polski",
}
```

早期版本的 Black 通常会简单粗暴直接将它们折成一行（这很合适！）。现在。您可以通过自己在集合中放一个尾随逗号来表明您不希望这样。当您这样做时，Black 会总是将集合的每一项放在单独的一行中。

停用该特性的方法也很简单，只要删去尾随逗号，Black 就会在合适的情况下把您的集合折叠到一行中。

如果有必要，您可以使用 `--skip-magic-trailing-comma` / `-C` 选项来使得 Black 恢复早期版本的处理方式。

#### r”strings” 与 R”strings”

Black 将字符串引号和字符串前缀标准化并使其小写。 此规则的一个例外是 r-strings 。 事实证明，非常流行的 [MagicPython](https://github.com/MagicStack/MagicPython/) 语法高亮器（GitHub、VS Code 等默认使用的都是这个），区分 r-strings 和 R-strings。 前者是作为正则表达式突出显示的语法，而后者被视为没有特殊语义的真正原始字符串。

#### 格式化前后的 AST

> 译者注：[AST](https://docs.python.org/zh-cn/3/library/ast.html)，即 **A**bstract **s**yntax **T**rees，抽象语法树

当使用了 `--safe` 选项运行时，Black 会检查前后的代码在语义上是否相同。此检查是通过将源 AST 与目标 AST 进行比较来完成的。在三种有限的情况下，AST 确实有所不同：

1. Black 清除文档字符串的前导和尾随空格，在必要情况下重新缩进。这是格式化程序最流行的用户报告功能之一，用于修复文档字符串的空白问题。虽然结果在技术上是 AST 差异，但由于形成文档字符串的各种可能性，我们知道的所有实时使用文档字符串都会清理缩进和前导/尾随空格。
2. Black 管理某些语句的可选括号。在 `del` 声明情况下，包装括号的有无会改变结果的 AST，但在解释器中语义是等效的。
3. Black 可能会移动注释，包括类型注释。这是 Python 3.8 中 AST 的一部分。虽然 Black 为这些注释实现了许多特殊情况，但不能保证它们将保持在源代码中的位置。注意这不会改变源代码运行时的行为。

从长远来看，代码等价性检查是 Black 的一个特性，其他格式化程序根本没有实现这个特性。对我们来说，确保代码在重新格式化之前的行为方式至关重要。我们将此视为一项特性，并且未来也不会懈怠。上面列举的例外来自于用户反馈或工具的实现细节。在每种情况下，我们都进行了审慎检查，以确保 AST 差异没有实际影响。

## 其他

### 在 README 中展示

如果你的项目使用了 Black 工具，可以在 [README.md](http://readme.md/) 中加入下面一行

```
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
```

这样就可以显示一个 shields 图标了：[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### 吃瓜：单引号？双引号！

关于字符串应该用单引号还是双引号包裹，Black 的开发组成员和一些用户有不同的意见。在早先的版本中，Black 强制使用双引号，且用户无法自行修改。于是他们足足在 Issue 里“吵”了一百多楼，各种引经据典，据理力争……终于开发组不得不妥协，勉为其难的给出了一个不格式化字符串引号的选项。

[GitHub 原楼请戳](https://github.com/psf/black/issues/118)

### 关于代码风格格式化的一点讨论

作为一个比较好学的 Python 小白，我从很早的时候就已经仔细阅读了 PEP 8，并利用 PyCharm 中自动检查规范自己的代码，深信代码首先是写给人看的，其次才是写给机器运行的。

在阅读 Black 文档时，我看到了这样一段话：

> **Pro-tip**: If you’re asking yourself “Do I need to configure anything?” the answer is “No”. *Black* is all about sensible defaults. Applying those defaults will have your code in compliance with many other *Black* formatted projects.
>
> **进阶提示**：当您在问自己“我是否需要配置任何东西”时，回答是否定的。Black 的一切皆为合理的默认值。使用这些默认选项将会使您的代码符合许多其他 Black 格式的项目。

Black 的精神似乎是 “less is more”，首先制定一套非常详细完备的标准，然后大家只需要使用该标准即可（还是傻瓜式操作），不需要也非常不建议搞“自定义”而破坏统一性。对于我这种一共也没写过几万行代码，也谈不上个人代码风格的小白是很大的福音：已经有人替我斟酌考虑好了细节，直接使用即可获得美观度一流的代码，何乐而不为呢？
