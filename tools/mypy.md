---
date: 2022-05-10T13:57:51+08:00
author: "Rustle Karl"

title: "Python 可选静态类型 mypy"
url:  "posts/shell/tools/mypy"  # 永久链接
tags: [ "shell" ]  # 自定义标签
series: [ "shell 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

https://mypy.readthedocs.io/en/stable/index.html

mypy 是 shell 中的静态类型检查器。mypy 具有强大且易于使用的类型系统，具有很多优秀的特性，例如类型推断、泛型、可调用类型、元组类型、联合类型和结构子类型。

## 数据类型

系统在存储数据之前，需要知道程序使用的数据需要多少内存空间。为此，编程语言会使用 类型 来进行确定。类型会匹配必须为程序分配用以存储数据的内存大小。几种最常见的类型包括整数、浮点数和字符串。

动态类型语言会在运行时检查程序中的类型。Python 即为动态类型语言（原文中写道：Python 有一个「弱」类型系统。为避免歧义，译者进行了修改。——译者注），这意味着解释器不强制进行类型检查。

静态类型语言在程序运行之前通过对源代码的分析来检查类型。如果程序可以通过静态类型检查，那就可以确保其满足某些类型安全性。静态类型检查会在运行前检测应用程序代码中可能的错误。这便是 mypy（Python 应用程序的静态类型检查）的价值所在。

## 安装

```shell
pip install mypy
```

然后把我们之前写的 python 代码，例如：

```python
def greeting(name):
    return 'Hello ' + name
```

只需要稍加改造，添加类型注释即可：

```python
def greeting(name: str) -> str:
    return 'Hello ' + name
```

然后运行：

```shell
mypy greeting.py
```

如果不想检查这一行，可以使用 `#type:ignore` 忽略：

```python
import frobnicate  # type: ignore
```

## 类型

### 内置类型

| 类型 | 描述 |
| -------- | -------- |
| int | 整数 |
| float | 浮点数 |
| bool | 布尔值 |
| str | 字符串 |
| bytes | 8-bit 字符串 |
| object | 对象 |
| Any | 任意类型 |
| list[str] | 字符串数组 |
| tuple[int, int] | 2 个整数元素的元祖 |
| tuple[int,...] | 任意数量整数元素的元祖 |
| dict[str, int] | key 为字符串，value 是整数的字典 |
| Iterable[int] | 可迭代类型，元素为整数 |
| Sequence[bool] | 布尔值序列 |
| Mapping[str, int] | key 是字符串，value 是整数的映射 |

### Class 类型

使用自定义类作为类型注释：

```python
class A:
    def f(self) -> int:  # Type of self inferred (A)
        return 2

class B(A):
    def f(self) -> int:
         return 3
    def g(self) -> int:
        return 4

def foo(a: A) -> None:
    print(a.f())  # 3
    a.g()         # Error: "A" has no attribute "g"

foo(B())  # OK (B is a subclass of A)
```

### Callable 类型

是否可调用：

```python
from typing import Callable

def arbitrary_call(f: Callable[..., int]) -> int:
    return f('x') + f(y=2)  # OK

arbitrary_call(ord)   # No static error, but fails at runtime
arbitrary_call(open)  # Error: does not return an int
arbitrary_call(1)     # Error: 'int' is not callable
```

### Union 类型

联合类型，也可以写为 type1 | type2：

```python
from typing import Union

def f(x: Union[int, str]) -> None:
    x + 1     # Error: str + int is not valid
    if isinstance(x, int):
        # Here type of x is int.
        x + 1      # OK
    else:
        # Here type of x is str.
        x + 'a'    # OK

f(1)    # OK
f('x')  # OK
f(1.1)  # Error
Note
```

### Optional 类型

可选类型, `Optional[X]` 相当于 `Union[X,None]`：

```python
from typing import Optional

def strlen(s: str) -> Optional[int]:
    if not s:
        return None  # OK
    return len(s)

def strlen_invalid(s: str) -> int:
    if not s:
        return None  # Error: None not compatible with int
    return len(s)
```

### NamedTuple 类型

```python
from typing import NamedTuple

Point = NamedTuple('Point', [('x', int), ('y', int)])
p = Point(x=1, y='x')  # Argument has incompatible type "str"; expected "int"
```

### TypeVar 任意类型

```python
from typing import TypeVar

T = TypeVar('T') # 任意类型
A = TypeVar('A', int, str) # A类型只能为int或str
def test(t: A) -> None:
    print(t)
test(1)
```

### Generator 生成器类型

```python
def echo_round() -> Generator[int, float, str]:
    sent = yield 0
    while sent >= 0:
        sent = yield round(sent)
    return 'Done'
```

### NoReturn 类型

函数永不返回：

```python
from typing import NoReturn

def stop() -> NoReturn:
    raise Exception('no way')
```

### NewType类型

声明一个不同的类型而又不实际执行创建新类型，在运行时，将返回一个仅返回其参数的虚拟函数：

```python
from typing import NewType

UserId = NewType('UserId', int)

def name_by_id(user_id: UserId) -> str:
    ...

UserId('user')          # Fails type check

name_by_id(42)          # Fails type check
name_by_id(UserId(42))  # OK

num = UserId(5) + 1     # type: int
```

### Overload 类型

给同一个函数多个类型注释来更准确地描述函数的行为：

```python
from typing import Union, overload

# Overload *variants* for 'mouse_event'.
# These variants give extra information to the type checker.
# They are ignored at runtime.

@overload
def mouse_event(x1: int, y1: int) -> ClickEvent: ...
@overload
def mouse_event(x1: int, y1: int, x2: int, y2: int) -> DragEvent: ...

# The actual *implementation* of 'mouse_event'.
# The implementation contains the actual runtime logic.
#
# It may or may not have type hints. If it does, mypy
# will check the body of the implementation against the
# type hints.
#
# Mypy will also check and make sure the signature is
# consistent with the provided variants.

def mouse_event(x1: int,
                y1: int,
                x2: Optional[int] = None,
                y2: Optional[int] = None) -> Union[ClickEvent, DragEvent]:
    if x2 is None and y2 is None:
        return ClickEvent(x1, y1)
    elif x2 is not None and y2 is not None:
        return DragEvent(x1, y1, x2, y2)
    else:
        raise TypeError("Bad arguments")
```

### Literal 类型

表明一个表达式等于某个特定的原始值。例如，如果我们用 type 注释一个变量 `Literal["foo"]`，mypy 将理解该变量不仅是 typestr，而且还特别等于string"foo"。

```python
from typing import overload, Union, Literal

# The first two overloads use Literal[...] so we can
# have precise return types:

@overload
def fetch_data(raw: Literal[True]) -> bytes: ...
@overload
def fetch_data(raw: Literal[False]) -> str: ...

# The last overload is a fallback in case the caller
# provides a regular bool:

@overload
def fetch_data(raw: bool) -> Union[bytes, str]: ...

def fetch_data(raw: bool) -> Union[bytes, str]:
    # Implementation is omitted
    ...

reveal_type(fetch_data(True))        # Revealed type is "bytes"
reveal_type(fetch_data(False))       # Revealed type is "str"

# Variables declared without annotations will continue to have an
# inferred type of 'bool'.

variable = True
reveal_type(fetch_data(variable))    # Revealed type is "Union[bytes, str]"
```

### Final 类型

限定符来指示不应重新分配、重新定义或覆盖名称或属性：

```python
from typing import Final

RATE: Final = 3000

class Base:
    DEFAULT_ID: Final = 0

RATE = 300  # Error: can't assign to final attribute
Base.DEFAULT_ID = 1  # Error: can't override a final attribute
```

## 配置文件

mypy 将按照当前目录下的 `mypy.ini > .mypy.ini > pyproject.toml > setup.cfg` 顺序查找配置文件。或者使用 `--config-file` 指定配置文件。

### 配置文件格式 

- `[mypy]` 全局设置
- `[mypy-PATTERN1,PATTERN2,...]` 特定模块设置

如果是使用 pyproject.toml 文件，则有一些不同的地方：

- `[mypy]` 改写为 `[tool.mypy]`
- 模块特定部分应移入 `[[tool.mypy.overrides]]` 部分，例如，`[mypy-packagename]` 会变成：

```ini
[[tool.mypy.overrides]]
module = 'packagename'
```

多模块特定部分可以移动到单个 `[[tool.mypy.overrides]]` 部分中，并将模块属性设置为模块数组，例如，`[mypy-packagename,packagename2]` 会变成：

```ini
[[tool.mypy.overrides]]
module = [
    'packagename',
    'packagename2'
]
```

字符串必须用双引号括起来，如果字符串包含特殊字符，则必须用单引号括起来，布尔值应全部小写

### 常见配置项

- files 逗号分隔的路径列表，如果命令行上没有给出，则应由 mypy 检查，支持递归。
- exclude 应忽略检查的文件名、目录名和路径。
- ignore_missing_imports 禁止有关无法解析的导入的错误消息。
- disallow_untyped_defs 不允许定义没有类型注释或类型注释不完整的函数。
- plugins 逗号分隔的 mypy 插件列表。
