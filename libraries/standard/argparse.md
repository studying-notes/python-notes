---
date: 2021-01-09T11:50:25+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Python argparse 命令行程序"  # 文章标题
url:  "posts/py/libraries/standard/argparse"  # 设置网页永久链接
tags: [ "python", "standard", "argparse" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

1、定义：argparse是python标准库里面用来处理命令行参数的库

2、命令行参数分为位置参数和选项参数：

​        位置参数就是程序根据该参数出现的位置来确定的

​                如：[root@openstack_1 /]# ls root/    #其中root/是位置参数

​        选项参数是应用程序已经提前定义好的参数，不是随意指定的

​                如：[root@openstack_1 /]# ls -l    # -l 就是ls命令里的一个选项参数

 3、使用步骤：

（1）import argparse    首先导入模块

（2）parser = argparse.ArgumentParser（）    创建一个解析对象

（3）parser.add_argument()    向该对象中添加你要关注的命令行参数和选项

（4）parser.parse_args()    进行解析

 4、argparse.ArgumentParser（）方法参数须知：一般我们只选择用description

​         prog=None     - 程序名

​         description=None,    - help时显示的开始文字

​          epilog=None,     - help时显示的结尾文字

​         parents=[],        -若与其他参数的一些内容一样，可以继承

​         formatter_class=argparse.HelpFormatter,     - 自定义帮助信息的格式

​         prefix_chars='-',    - 命令的前缀，默认是‘-’

​         fromfile_prefix_chars=None,     - 命令行参数从文件中读取

​         argument_default=None,    - 设置一个全局的选项缺省值，一般每个选项单独设置

​         conflict_handler='error',     - 定义两个add_argument中添加的选项名字发生冲突时怎么处理，默认处理是抛出异常

​         add_help=True    - 是否增加-h/--help选项，默认是True)

 5、add_argument()方法参数须知：

​          name or flags...    - 必选，指定参数的形式，一般写两个，一个短参数，一个长参数

```javascript
import argparse 
parser = argparse.ArgumentParser() 
parser.add_argument('echo') # add_argument()指定程序可以接受的命令行选项 
args = parser.parse_args() # parse_args()从指定的选项中返回一些数据 
print(args) 
print(args.echo)
```

结果：

>  G:\flower\python\arg_parse>python demo1.py foo Namespace(echo='foo') foo 

action 表示值赋予键的方式，这里用到的是bool类型，action意思是当读取的参数中出现指定参数的时候的行为 help 可以写帮助信息 

```javascript
parser = argparse.ArgumentParser(description = 'this is a description')
parser.add_argument('--ver', '-v', action = 'store_true', help = 'hahaha')
# 将变量以标签-值的字典形式存入args字典
args = parser.parse_args()
if args.ver:
    print("Ture")
else:
    print("False")

```

结果：

```javascript
G:\flower\python\arg_parse>python demo1.py -v


Ture

G:\flower\python\arg_parse>python demo1.py -j

usage: demo1.py [-h] [--ver]

demo1.py: error: unrecognized arguments: -j
```

   required    - 必需参数，通常-f这样的选项是可选的，但是如果required=True那么就是必须的了

 type   - 指定参数类型

```javascript
# required标签就是说--ver参数是必需的，并且类型为int，输入其它类型会报错 
parser.add_argument('--ver', '-v', required = True, type = int)
```

>  结果： G:\flower\python\arg_parse>python demo1.py -v 1 Ture G:\flower\python\arg_parse>python demo1.py -v ss usage: demo1.py [-h] --ver VER demo1.py: error: argument --ver/-v: invalid int value: 'ss' 

  choices    - 设置参数的范围，如果choice中的类型不是字符串，要指定type

表示该参数能接受的值只能来自某几个值候选值中，除此之外会报错，用choice参数即可

```javascript
parser.add_argument('file', choices = ['test1', 'test2']) 
args = parser.parse_args() 
print('read in %s'%(args.file))
```

结果：

>  G:\flower\python\arg_parse>python demo1.py test1 read in test1 

 nargs    - 指定这个参数后面的value有多少个，默认为1

```javascript
# 表示脚本可以读入两个整数赋予num键（此时的值为2个整数的数组）
parser.add_argument('filename', nargs = 2, type = int)
args = parser.parse_args()
print('read in %s'%(args.filename))

```

结果：

>  G:\flower\python\arg_parse>python demo1.py 1 2 3 usage: demo1.py [-h] filename filename demo1.py: error: unrecognized arguments: 3 

分析：nargs还可以'*'用来表示如果有该位置参数输入的话，之后所有的输入都将作为该位置参数的值；‘+’表示读取至少1个该位置参数。'?'表示该位置参数要么没有，要么就只要一个。（PS：跟正则表达式的符号用途一致。）如：

```javascript
parser.add_argument('filename', nargs = '+', type = int)
args = parser.parse_args()
print('read in %s'%(args.filename))

```

dest   - 设置这个选项的value解析出来后放到哪个属性中

```javascript
parser.add_argument('-file', choices = ['test1', 'test2'], dest = 'world')
args = parser.parse_args()
print('read in %s'%(args.world))

```

结果：

>  G:\flower\python\arg_parse>python demo1.py -file test1 read in test1 