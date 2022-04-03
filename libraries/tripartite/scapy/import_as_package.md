---
date: 2022-04-03T15:56:13+08:00
author: "Rustle Karl"

title: "作为第三方库导入 Scapy"
url:  "posts/python/libraries/tripartite/scapy/import_as_package"  # 永久链接
tags: [ "python"]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

你可以使用 Scapy 构建你自己的自动化工具。你也可以扩展 Scapy 而不必编辑它的源文件。

## 在你的工具中使用 Scapy

你可以很容易的在你的工具中使用 Scapy，只需要导入你需要的便可以使用。

第一个例子是传入一个 IP 或者一个主机名作为参数，发送一个 ICMP 响应请求，然后显示返回包完整的构造。

```python
import sys
from scapy.all import sr1,IP,ICMP

p=sr1(IP(dst=sys.argv[1])/ICMP())
if p:
    p.show()
```

找个有一个更加灵活的例子，就是生成一个 ARP 的 ping 包，并用 LaTeX 格式报告它所发现的东西。

```python
import sys
if len(sys.argv) != 2:
    print("Usage: arping2tex <net>\n eg: arping2tex 192.168.1.0/24")
    sys.exit(1)

from scapy.all import srp,Ether,ARP,conf
conf.verb=0
ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=sys.argv[1]),
              timeout=2)

print(r"\begin{tabular}{|l|l|}")
print(r"\hline")
print(r"MAC & IP\\")
print(r"\hline")
for snd,rcv in ans:
    print(rcv.sprintf(r"%Ether.src% & %ARP.psrc%\\"))
print(r"\hline")
print(r"\end{tabular}")
```

这有另外一个工具，它将时刻监控机器上的所有的网卡并打印所有的 ARP 请求。即使是混杂模式下的无线网卡上的 801.11 数据帧。注意，sniffer() 函数的参数 store = 0 是为了避免将所有的数据包存储在内存。

```python
from scapy.all import *

def arp_monitor_callback(pkt):
    if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
        return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")

sniff(prn=arp_monitor_callback, filter="arp", store=0)
```

这里有一个生活中真实的例子，你可以参考WiFitap(http://sid.rstack.org/static/articles/w/i/f/Wifitap_EN_9613.html).

## 扩展Scapy

如果你想添加一些新的协议，新的函数，或者任何东西，你可以直接编辑 Scapy 的源代码。但是这是非常不方便的。即使这些修改将会整合到 Scapy 中去。可以更加方便的编写他们在单独的文件中。

一旦你这么做了，你可以启动 Scapy 并导入自己的文件，但是这还是不是很方便，另外一个能做到这一点的方法是让你文件执行并且调用 Scapy 的 interact() 函数。

```python
# Set log level to benefit from Scapy warnings
import logging
logging.getLogger("scapy").setLevel(1)

from scapy.all import *

class Test(Packet):
    name = "Test packet"
    fields_desc = [ ShortField("test1", 1),
                    ShortField("test2", 2) ]

def make_test(x,y):
    return Ether()/IP()/Test(test1=x,test2=y)

if __name__ == "__main__":
    interact(mydict=globals(), mybanner="Test add-on v3.14")
```

如果你运行上面的代码，便会得到下面的结果：

```
Welcome to Scapy (0.9.17.109beta)
Test add-on v3.14
>>> make_test(42,666)
<Ether type=0x800 |<IP |<Test test1=42 test2=666 |>>>
```
