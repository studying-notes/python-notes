---
date: 2022-05-16T11:02:59+08:00
author: "Rustle Karl"

title: "enum 枚举"
url:  "posts/python/libraries/standard/types/enum"  # 永久链接
tags: [ "python" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

> https://docs.python.org/3/library/enum.html
> https://docs.python.org/zh-cn/3/library/enum.html

枚举是与多个唯一常量值绑定的一组符号名（即成员）。枚举中的成员可以进行身份比较，并且枚举自身也可迭代。

本模块定义了四个枚举类，用来定义名称与值的唯一组合: Enum、IntEnum、Flag 和 IntFlag。此外，还定义了一个装饰器，unique()， 和一个辅助类，auto。

## enum.Enum

创建枚举常量的基类。 

## enum.IntEnum

```python
class IntEnum(int, Enum):
    pass
```

创建 int 子类枚举常量的基类。

所提供的第一个变种 Enum 同时也是 int 的一个子类。 IntEnum 的成员可与整数进行比较；通过扩展，不同类型的整数枚举也可以相互进行比较:

```python
from enum import IntEnum

class Shape(IntEnum):
    CIRCLE = 1
    SQUARE = 2

class Request(IntEnum):
    POST = 1
    GET = 2

Shape == 1
# False

Shape.CIRCLE == 1
# True

Shape.CIRCLE == Request.POST
# True
```

不过，它们仍然不可与标准 Enum 枚举进行比较:

```python
class Shape(IntEnum):
    CIRCLE = 1
    SQUARE = 2

class Color(Enum):
    RED = 1
    GREEN = 2

Shape.CIRCLE == Color.RED
# False
```

IntEnum 值在其他方面的行为都如你预期的一样类似于整数:

```python
int(Shape.CIRCLE)

['a', 'b', 'c'][Shape.CIRCLE]

[i for i in range(Shape.SQUARE)]
```

## enum.IntFlag

创建可与位运算符搭配使用，又不失去 IntFlag 成员资格的枚举常量的基类。IntFlag 成员也是 int 的子类。

所提供的下一个 Enum 的变种 IntFlag 同样是基于 int 的，不同之处在于 IntFlag 成员可使用按位运算符 (&, |, ^, ~) 进行组合且结果仍然为 IntFlag 成员。 如果，正如名称所表明的，IntFlag 成员同时也是 int 的子类，并能在任何使用 int 的场合被使用。 IntFlag 成员进行除按位运算以外的其他运算都将导致失去 IntFlag 成员资格。

```python
from enum import IntFlag
class Perm(IntFlag):
    R = 4
    W = 2
    X = 1

Perm.R | Perm.W

Perm.R + Perm.W

RW = Perm.R | Perm.W
Perm.R in RW
```

IntFlag 和 Enum 的另一个重要区别在于如果没有设置任何旗标（值为 0），则其布尔值为 False:

```python
Perm.R & Perm.X

bool(Perm.R & Perm.X)
```

由于 IntFlag 成员同时也是 int 的子类，因此它们可以相互组合:

```python
Perm.X | 8
```

## enum.Flag

创建可与位运算符搭配使用，又不会失去 Flag 成员资格的枚举常量的基类。

与 IntFlag 类似，Flag 成员可使用按位运算符 (&, |, ^, ~) 进行组合，与 IntFlag 不同的是它们不可与任何其它 Flag 枚举或 int 进行组合或比较。 虽然可以直接指定值，但推荐使用 auto 作为值以便让 Flag 选择适当的值。

与 IntFlag 类似，如果 Flag 成员的某种组合导致没有设置任何旗标，则其布尔值为 False:

```python
from enum import Flag, auto
class Color(Flag):
    RED = auto()
    BLUE = auto()
    GREEN = auto()

Color.RED & Color.GREEN

bool(Color.RED & Color.GREEN)
```

单个旗标的值应当为二的乘方 (1, 2, 4, 8, ...)，旗标的组合则无此限制:

```python
class Color(Flag):
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    WHITE = RED | BLUE | GREEN

Color.WHITE
```

对 "no flags set" 条件指定一个名称并不会改变其布尔值:

```python
class Color(Flag):
    BLACK = 0
    RED = auto()
    BLUE = auto()
    GREEN = auto()

Color.BLACK

bool(Color.BLACK)
```

## enum.unique()

确保一个名称只绑定一个值的 Enum 类装饰器。

```python

```

## enum.auto

以合适的值代替 Enum 成员的实例。 初始值默认从 1 开始。

## 创建 Enum

```python
from enum import Enum
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
```

成员值可以是 int、str 等。若无需设定确切值，auto 实例可以自动为成员分配合适 的值。将 auto 与其他值混用时必须要慎重。

## 确保唯一枚举值

默认情况下，枚举允许多个名称作为一个值的别名。如需禁用此行为，下述装饰器可以确保枚举中的值仅能只用一次：

```python
from enum import Enum, unique

@unique
class Mistake(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 3
```

## 使用自动设定的值

```python
from enum import Enum, auto

class Color(Enum):
    RED = auto()
    BLUE = auto()
    GREEN = auto()

list(Color)
```


## 二级

### 三级

```python

```

```python

```


## 二级

### 三级

```python

```

```python

```


## 二级

### 三级

```python

```

```python

```



## 枚举类型

为枚举类型定义一个 class 类型，然后，每个常量都是 class 的一个唯一实例。Python 提供了 `Enum` 类来实现这个功能：

```python
from enum import Enum

Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
```

这样我们就获得了 `Month` 类型的枚举类，可以直接使用 `Month.Jan` 来引用一个常量，或者枚举它的所有成员：

```python
for name, member in Month.__members__.items():
    print(name, '=>', member, ',', member.value)
```

```
Jan => Month.Jan , 1
Feb => Month.Feb , 2 
Mar => Month.Mar , 3 
Apr => Month.Apr , 4 
May => Month.May , 5 
Jun => Month.Jun , 6 
Jul => Month.Jul , 7 
Aug => Month.Aug , 8 
Sep => Month.Sep , 9 
Oct => Month.Oct , 10
Nov => Month.Nov , 11
Dec => Month.Dec , 12
```

`value` 属性则是自动赋给成员的 `int` 常量，默认从 `1` 开始计数。

如果需要更精确地控制枚举类型，可以从 `Enum` 派生出自定义类：

```python
from enum import Enum, unique

@unique
class Weekday(Enum):
    Sun = 0 # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
```

`@unique` 装饰器可以帮助我们检查保证没有重复值。

访问这些枚举类型可以有若干种方法：

```python
>>> day1 = Weekday.Mon
>>> print(day1)
Weekday.Mon
>>> print(Weekday.Tue)
Weekday.Tue
>>> print(Weekday['Tue'])
Weekday.Tue
>>> print(Weekday.Tue.value)
2
>>> print(day1 == Weekday.Mon)
True
>>> print(day1 == Weekday.Tue)
False
>>> print(Weekday(1))
Weekday.Mon
>>> print(day1 == Weekday(1))
True
>>> Weekday(7)
Traceback (most recent call last):
  ...
ValueError: 7 is not a valid Weekday
>>> for name, member in Weekday.__members__.items():
...     print(name, '=>', member)
...
Sun => Weekday.Sun
Mon => Weekday.Mon
Tue => Weekday.Tue
Wed => Weekday.Wed
Thu => Weekday.Thu
Fri => Weekday.Fri
Sat => Weekday.Sat
```

可见，既可以用成员名称引用枚举常量，又可以直接根据 value 的值获得枚举常量。
