---
date: 2022-04-07T21:23:45+08:00
author: "Rustle Karl"

title: "第1章_套接字、IPV4和简单的客户端服务器编程"
url:  "posts/python/docs/Python网络编程攻略/第1章_套接字、IPV4和简单的客户端服务器编程"  # 永久链接
tags: [ "python"]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

## 标准库文档

https://docs.python.org/zh-cn/3.10/library/socket.html

这个 Python 接口是用 Python 的面向对象风格对 Unix 系统调用和套接字库接口的直译：函数 socket() 返回一个 套接字对象，其方法是对各种套接字系统调用的实现。形参类型一般与 C 接口相比更高级：例如在 Python 文件 read() 和 write() 操作中，接收操作的缓冲区分配是自动的，发送操作的缓冲区长度是隐式的。

## 打印设备名和IPv4地址

```python
import socket

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
```

## 获取远程设备的IP地址

```python
socket.gethostbyname("baidu.com")
```

## 将IPv4地址转换成不同的格式

```python
ip_address = "220.181.38.251"
packed_ip_address = socket.inet_aton(ip_address)
socket.inet_ntoa(packed_ip_address)
```

## 通过指定的端口和协议找到服务名

如果想找到网络服务，最好知道该服务运行在 TCP 或 UDP 协议的哪个端口上。

如果知道网络服务使用的端口，可以调用 socket 库中的 getservbyport() 函数来获取服务的名字。

```python
socket.getservbyport(80, "tcp")
```

## 主机字节序和网络字节序之间相互转换

```python
hex(socket.ntohs(0x1234))
```

```
'0x3412'
```

```python
hex(socket.htons(0x1234))
```

```
'0x3412'
```

```python
hex(socket.ntohl(0x12345678))
```

```python
'0x78563412'
```

```python
hex(socket.htonl(0x12345678))
```

```python
'0x78563412'
```

编写低层网络应用时，或许需要处理通过电缆在两台设备之间传送的低层数据。在这种操作中，需要把主机操作系统发出的数据转换成网络格式，或者做逆向转换，因为这两种数据的表示方式不一样。

```python
data = 1234
# 32 bit
# 网络到主机
data2=socket.ntohl(data)
# 主机到网络
socket.htonl(data2)==data

# 16 bit
# 网络到主机
socket.ntohs(data)
# 主机到网络
socket.htons(data)
```

socket 库中的类函数 ntohl() 把网络字节序转换成了长整形主机字节序。函数名中的 n 表示网络； h 表示主机； l 表示长整形； s 表示短整形，即 16 位。

## 设定并获取默认的套接字超时时间

```python
s.gettimeout()
s.settimeout(100)
```

这个方法在处理阻塞式套接字操作时使用。如果把超时时间设为 None，则禁用了套接字操作的超时检测。

## 优雅地处理套接字错误

在网络应用中，经常会遇到这种情况：一方尝试连接，但另一方由于网络媒介失效或者其他原因无法响应。Python 的 socket 库提供了一个方法，能通过 socket.error 异常优雅地处理套接字错误。

```python
try:
    s.accept()
except socket.gaierror as e:
    print(e)
except socket.error as e:
    print(e)
```

除第二个块处理 socket.gaierror 异常之外，其他块都处理 socket.error 异常。socket.gaierror 是地址相关的错误。除此之外还有两种异常：socket.herror，C API 中抛出的异常；如果在套接字中使用 settimeout() 方法，套接字超时后会抛出 socket.timeout 异常。

## 修改套接字发送和接收的缓冲区大小

很多情况下，默认的套接字缓冲区大小可能不够用。此时，可以将默认的套接字缓冲区大小改成一个更合适的值。

我们要使用套接字对象的 setsockopt() 方法修改默认的套接字缓冲区大小。

首先，定义两个常量：SEND_BUF_SIZE和RECV_BUF_SIZE。然后在一个函数中调用套接字实例的 setsockopt() 方法。修改之前，最好先检查缓冲区大小是多少。注意，发送和接收的缓冲区大小要分开设定。

```python
SEND_BUF_SIZE = 4096
RECV_BUF_SIZE = 4096
buf_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUF_SIZE)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SIZE)
```

在套接字对象上可调用方法 getsockopt() 和 setsockopt() 分别获取和修改套接字对象的属性.setsockopt() 方法接收三个参数：level、optname 和 value。其中，optname 是选项名，value 是该选项的值。第一个参数所用的符号常量（SO_ *等）可在 socket 模块中查看。

[可用选项](https://img-blog.csdnimg.cn/20200714101508103.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0pNVzE0MDc=,size_16,color_FFFFFF,t_70)

## 把套接字改成阻塞或非阻塞模式

默认情况下，TCP 套接字处于阻塞模式中。也就是说，除非完成了某项操作，否则不会把控制权交还给程序。例如，调用 connect() API 后，连接操作会阻止程序继续往下执行，直到连接成功为止。很多情况下，你并不想让程序一直等待服务器响应或者有异常终止操作。例如，如果编写了一个网页浏览器客户端连接服务器，你应该考虑提供取消功能，以便在操作过程中取消连接。这时就要把套接字设置为非阻塞模式。

在 Python 中，套接字可以被设置为阻塞模式或者非阻塞模式。在非阻塞模式中，调用 API 后，例如 send() 或 recv() 方法，如果遇到问题就会抛出异常。但在阻塞模式中，遇到错误并不会阻止操作。我们可以创建一个普通的 TCP 套接字，分别在阻塞模式和非阻塞模式中执行操作实验。
为了能在阻塞模式中处理套接字，首先要创建一个套接字对象。然后, 调用 setblocking(1) 把套接字设为阻塞模式，或者调用 setblocking(0) 把套接字设为非阻塞模式。最后，把套接字绑定到指定的端口上，监听进入的连接。

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(1)
s.settimeout(0.5)
s.bind(("127.0.0.1", 0))
socket_address = s.getsockname()
while (1):
    s.listen(1)
```

## 重用套接字地址

> 多个进程监听同一个端口

### 操作系统如何区分一个 socket

[socket=(A进程的IP地址:端口号),(B进程的IP地址:端口号),协议](https://img-blog.csdnimg.cn/20200713174930728.png)

也就是说，只要五元素不完全一致，操作系统就能区分 socket。

在 A 机上进行客户端网络编程，假如它所使用的本地端口号是 1234，如果没有开启端口复用的话，它用本地端口 1234 去连接 B 机再用本地端口连接 C 机时就不可以，若开启端口复用的话在用本地端口 1234 访问 B 机的情况下还可以用本地端口 1234 访问 C 机。

若是服务器程序中监听的端口，即使开启了复用，也不可以用该端口望外发起连接了，但仍可以接受连接。

端口复用允许在一个应用程序可以把 n 个套接字绑在一个端口上而不出错。

不管连接是被有意还是无意关闭，有时你想始终在同一个端口上运行套接字服务器。某些情况下，如果客户端程序需要一直连接指定的服务器端口，这么做就很有用，因为无需改变服务器端口。

如果在某个端口上运行一个 Python 套接字服务器，连接一次之后便终止运行，就不能再使用这个端口了。如果再次连接，程序会抛出如下错误：

```
address already in use
```

这个问题的解决方法是启用套接字重用选项 SO_REUSEADDR。

创建套接字对象之后，我们可以查询地址重用的状态，比如说旧状态。然后，调用 setsockopt() 方法，修改地址重用状态的值。再按照常规的步骤，把套接字绑定到一个地址上，监听进入的客户端连接。

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

你可以在一个终端窗口运行这个脚本，然后在另一个终端窗口中尝试连接这个服务器。关闭服务器程序后，还可以使用同一个端口再次连接。然而，如果你把设定 SO_REUSEADDR 的那行代码注释掉，服务器将不会再次运行脚本。

### SO_REUSEADDR 功能

- 允许启动一个监听服务器并捆绑其众所周知端口，即使以前建立的将此端口用做他们的本地端口的连接仍存在。这通常是重启监听服务器时出现，若不设置此选项，则 bind 时将出错。
- 允许在同一端口上启动同一服务器的多个实例，只要每个实例捆绑一个不同的本地 IP 地址即可。对于 TCP，我们根本**不可能启动捆绑相同 IP 地址和相同端口号的多个服务器**。
- 允许单个进程**捆绑同一端口到多个套接口上**，只要每个捆绑指定不同的本地 IP 地址即可。这一般不用于 TCP 服务器。
- 允许完全重复的捆绑：当一个 IP 地址和端口绑定到某个套接口上时，还允许此 IP 地址和端口捆绑到另一个套接口上。一般来说，这个特性仅在支持多播的系统上才有，而且只对 UDP 套接口而言（TCP 不支持多播）。

### SO_REUSEADDR 语义

- 此选项允许完全重复捆绑，但仅在想捆绑相同 IP 地址和端口的套接口都指定了此套接口选项才行。
- 如果被捆绑的 IP 地址是一个多播地址，则 SO_REUSEADDR 和 SO_REUSEPORT 等效。

### SO_REUSEADDR 到底什么意思

这个套接字选项通知内核，如果端口忙，但 TCP 状态位于 TIME_WAIT ，可以重用端口。如果端口忙，而 TCP 状态位于其他状态，重用端口时依旧得到一个错误信息，指明"地址已经使用中"。如果你的服务程序停止后想立即重启，而新套接字依旧使用同一端口，此时 SO_REUSEADDR 选项非常有用。必须意识到，此时任何非期望数据到达，都可能导致服务程序反应混乱，不过这只是一种可能，事实上很不可能。

端口复用允许在一个应用程序可以把 n 个套接字绑在一个端口上而不出错。同时，这 n 个套接字**发送信息都正常**，没有问题。但是，这些套接字并**不是所有都能读取信息，只有最后一个套接字会正常接收数据**。

端口复用最常用的用途应该是防止服务器重启时之前绑定的端口还未释放或者程序突然退出而系统没有释放端口。这种情况下如果设定了端口复用，则新启动的服务器进程可以直接绑定端口。如果没有设定端口复用，绑定会失败。

## 从网络时间服务器上获取并打印当前时间

很多程序要求设备的时间精准，例如 Unix 系统中的 make 命令。设备上的时间可能不够准确，需要和网络中的时间服务器同步。

你可以编写一个 Python 客户端，让设备上的时间和某个网络时间服务器同步。要完成这一操作，需要使用 ntplib，通过“网络时间协议”（Network Time Protocol，简称 NTP）处理客户端和服务器之间的通信。

```python
pip install ntplib
```

```python
import ntplib
from time import ctime
ntp_client = ntplib.NTPClient()
response = ntp_client.request("pool.ntp.org")
ctime(response.tx_time)
```

## 编写一个SNTP客户端

与前一个攻略不同，有时并不需要从 NTP 服务器上获取精确的时间。遇到这种情况，就可以使用 NTP 的简化版本，叫作“简单网络时间协议”。

```python
import socket
import struct
import time

TIME1997 = 2208988800
NTP_SERVER = "pool.ntp.org"

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = b"\x1b" + 47 * b"\0"
client.sendto(data, (NTP_SERVER, 123))
data, address = client.recvfrom(1024)
print("response received from server:", address)

ts = struct.unpack("!12L", data)
t = ts[10]
t -= TIME1997
print(time.ctime(t))
```

## 编写一个简单的回显客户端/服务器应用

```python
import socket

host = 'localhost'
payload = 2048
backlog = 5

def echo_server(port=8089):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(backlog)
    while True:
        client, client_address = s.accept()
        data = client.recv(payload)
        if data:
            client.send(data)
            client.close()
    
def echo_client(port=8089):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall("OK")
    data = s.recv(16)
    if data:
        s.sendall(data)
    s.close()
```
