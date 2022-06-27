---
date: 2022-04-08T13:26:32+08:00
author: "Rustle Karl"

title: "第2章_使用多路复用套接字IO提升性能"
url:  "posts/python/docs/Python网络编程攻略/第2章_使用多路复用套接字I0提升性能"  # 永久链接
tags: [ "python"]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

考虑多个客户端连接服务器的情况，而且可以异步通信。服务器不需要在阻塞模式中处理客户端发出的请求，而是单独处理每个请求。如果某个客户端接收或处理数据时花了很长时间，服务器无需等待处理完成，可以使用另外的线程或进程和其他客户端通信。

select 模块建立在底层操作系统内核的 select 系统调用基础之上，提供了平台专用的 I/O 监控功能。。我们的套接字服务器要和多个客户端交互，所以 select 可以帮助我们监控非阻塞式套接字。有些第三方 Python 库也能帮助我们同时处理多个客户端，比如 Diesel 并发库。

## 在套接字服务器程序中使用 ForkingMixIn

你已经决定要编写一个异步 Python 套接字服务器程序。服务器处理客户端发出的请求时不能阻塞，因此要找到一种机制来单独处理每个客户端。

SocketServer 模块提供了两个实用类：ForkingMixIn 和 ThreadingMixIn。

SocketServer 模块提供了可以直接使用的 TCP、UDP 及其他协议服务器。我们可以创建 ForkingServer 类，继承 TCPServer 和 ForkingMixIn 类。前一个父类让 ForkingServer 类实现了之前手动完成的所有服务器操作，例如创建套接字、绑定地址和监听进入的连接。我们的服务器还要继承 ForkingMixIn 类，异步处理客户端。

ForkingServer 类还要创建一个请求处理程序，说明如何处理客户端请求。在这个攻略中，我们的服务器会回显客户端发送的文本字符串。请求处理类 ForkingServerRequestHandler 继承自 SocketServer 库提供的 BaseRequestHandler 类。

回显服务器的客户端 ForkingClient 可以使用面向对象的方式编写。在 Python 中，类的构造方法叫作 `__init__()`。按照惯例，要把 self 作为参数传入` __init__()`方法，以便指定具体实例的属性。ForkingClient 连接的回显服务器要在` __init__()`方法中初始化，然后在 `run()` 方法中向服务器发送消息。

```python
"""
Date: 2022.04.08 13:33:41
LastEditors: Rustle Karl
LastEditTime: 2022.04.08 13:39:52
"""
import os
import socket
import socketserver
import threading

SERVER_HOST='localhost'
SERVER_PORT=0# 让内核动态选取
BUF_SIZE=1024
ECHO_MSG=b"I'm echo server"

class ForkingClient(object):

    def __init__(self, ip,port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((ip, port))

    def run(self):
        current_process_id = os.getpid()
        print(f"PID {current_process_id} sending echo message to the server: {ECHO_MSG}")
        self._socket.send(ECHO_MSG)
        response = self._socket.recv(BUF_SIZE)
        print(f"PID {current_process_id} received: {response}")

    def shutdown(self):
        self._socket.close()

class ForkingServerRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        response=self.request.recv(BUF_SIZE)
        current_process_id = os.getpid()
        print(f"PID {current_process_id} received: {response}")
        self.request.send(response)


class ForkingServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

def main():
    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    print(f"Server loop running PID: {os.getpid()}")
    
    c1 = ForkingClient(ip, port)
    c1.run()
    
    c2 = ForkingClient(ip, port)
    c2.run()
    
    c1.shutdown()
    c2.shutdown()
    
    server.socket.close()
```        

主线程中创建了一个 ForkingServer 实例，作为守护进程在后台运行。然后再创建两个客户端和服务器交互。

在你的设备中可能会使用不同的服务器端口号，因为端口号由操作系统内核动态选择。

## 在套接字服务器程序中使用 ThreadingMixIn

或许基于某些原因你不想编写基于进程的应用程序，而更愿意编写多线程应用程序。可能的原因有：在线程之间共享应用的状态，避免进程间通信的复杂操作，等等。遇到这种需求，如果想使用 SocketServer 库编写异步网络服务器，就得使用 ThreadingMixIn 类。

和前一节中基于 ForkingMixIn 的套接字服务器一样，使用 ThreadingMixIn 编写的套接字服务器要遵循相同的回显服务器编程模式，不过仍有几点不同。首先，ThreadedTCPServer 继承自 TCPServer 和 TheadingMixIn。客户端连接这个多线程版服务器时，会创建一个新线程。

## 使用 select.select 编写一个聊天室服务器

```python
"""
Date: 2022.04.08 13:33:41
LastEditors: Rustle Karl
LastEditTime: 2022.04.08 13:39:52
"""
import os
import socket
import socketserver
import threading

SERVER_HOST='localhost'
SERVER_PORT=0# 让内核动态选取
BUF_SIZE=1024
ECHO_MSG=b"I'm echo server"

def client(ip, port, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    try:
        s.sendall(message)
        response = s.recv(BUF_SIZE)
        print(f'client received: {response}')
    finally:
        s.close()

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        response = self.request.recv(BUF_SIZE)
        current_process = threading.current_thread()
        print(f"{current_process}: {response}")
        self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def main():
    server = ThreadedTCPServer((SERVER_HOST,SERVER_PORT), ThreadedTCPRequestHandler)
    ip,port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    client(ip,port, 'client1')
    client(ip,port, 'client2')
    client(ip,port, 'client3')

    server.shutdown()
```

在客户端和服务器的通信中用到了sendall() 方法，以保证发送的数据无任何丢失。

## 使用select.select编写一个聊天室服务器

在大型网络服务器应用程序中可能有几百或几千个客户端同时连接服务器，此时为每个客户端创建单独的线程或进程可能不切实际。由于内存可用量受限，且主机的 CPU 能力有限，我们需要一种更好的技术来处理大量的客户端。幸好，Python 提供的 select 模块能解决这一问题。

我们将编写一个高效的聊天室服务器，处理几百或更多数量的客户端连接。我们要使用 select 模块提供的 select() 方法，让聊天室服务器和客户端所做的操作始终不会阻塞消息的发送和接收。
这个攻略使用一个脚本就能启动客户端和服务器，执行脚本时要指定—— name 参数。只有在命令行中传入了—— name = server，脚本才启动聊天室服务器。如果为—— name 参数指定了其他值，例如 client1 或 client2，则脚本会启动聊天室客户端。聊天室服务器绑定的端口在命令行参数—— port 中指定。对大型应用程序而言，最好在不同的模块中编写服务器和客户端。

```python

```

初始化聊天室服务器时创建了一些属性：客户端数量、客户端映射和输出的套接字。和之前创建服务器套接字一样，初始化时也设定了重用地址的选项，这么做可以使用同一个端口重启服务器。聊天室服务器类的构造方法还有一个可选参数backlog，用于设定服务器监听的连接队列的最大数量。

这个聊天室服务器有个值得介绍的地方，它可以使用signal模块捕获用户的中断操作。中断操作一般通过键盘输入。ChatServer类为中断信号（SIGINT）注册了一个信号处理方法sighandler。信号处理方法捕获从键盘输入的中断信号后，关闭所有输出套接字，其中一些套接字可能还有数据等待发送。

聊天室服务器的主要执行方法是run（），在while循环中执行操作。run（）方法注册了一个select接口，输入参数是聊天室服务器套接字stdin，输出参数由服务器的输出套接字列表指定。调用select.select（）方法后得到三个列表：可读套接字、可写套接字和异常套接字。聊天室服务器只关心可读套接字，其中保存了准备被读取的数据。如果可读套接字是服务器本身，表示有一个新客户端连到服务器上了，服务器会读取客户端的名字，将其广播给其他客户端。如果输入参数中有内容，聊天室服务器会退出。类似地，这个聊天室服务器也能处理其他客户端套接字的输入，转播客户端直接传送的数据，还能共享客户端进入和离开聊天室的信息。

初始化聊天室客户端时指定了name参数，连接到聊天室服务器之后，这个名字会发送给服务器。初始化时还设置了一个自定义的提示符［name@host］>。客户端的执行方法run（）在连接到服务器的过程中一直运行着。和聊天室服务器类似，聊天室客户端也使用select（）方法注册。只要可读套接字做好了准备，客户端就开始接收数据。如果sock的值为0，而且有可用的数据，客户端就可以发送数据。发送的数据还会显示在stdout或者本例中的命令行终端里。

## 使用 select.epoll 多路复用 Web 服务器

Python 的 select 模块中有很多针对特定平台的网络事件管理函数。在 Linux 设备中可以使用 epoll。这个函数利用操作系统内核轮询网络事件，让脚本知道有事件发生了。

这个脚本的核心在 Web 服务器的初始化过程中，我们要调用方法 select.epoll()，注册服务器的文件描述符，以达到事件通知的目的。

```python
import socket

import select

SERVER_HOST = "localhost"
EOL1 = b"\n\n"
EOL2 = b"\n\r\n"

SERVER_RESPONSE = (
    b"HTTP/1.1 200 OK\r\n"
    b"Date:Mon,1 Apr 2013 01:01:01 GMT\r\n"
    b"Content-Type:text/plain\r\n"
    b"Content-Length:25\r\n\r\n"
    b"Hello from Epoll Server!"
)


class EpollServer(object):
    def __init__(self, host=SERVER_HOST, port=0):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(1)
        self.sock.setblocking(False)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        print("Started Epoll Server")
        self.epoll = select.epoll()
        self.epoll.register(self.sock.fileno(), select.EPOLLIN)

    def run(self):
        try:
            connections = {}
            requests = {}
            responses = {}

            while True:
                events = self.epoll.poll(1)
                for fileno, event in events:
                    if fileno == self.sock.fileno():
                        connection, address = self.sock.accept()
                        connection.setblocking(False)
                        self.epoll.register(connection.fileno(), select.EPOLLIN)
                        connections[connection.fileno()] = connection
                        requests[connection.fileno()] = b""
                        responses[connection.fileno()] = SERVER_RESPONSE
                    elif event & select.EPOLLIN:
                        requests[fileno] += connections[fileno].recv(1024)
                        if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                            self.epoll.modify(fileno, select.EPOLLOUT)
                            print("-" * 40 + "\n" + requests[fileno].decode()[:-2])
                    elif event & select.EPOLLOUT:
                        byteswritten = connections[fileno].send(responses[fileno])
                        responses[fileno] = responses[fileno][byteswritten:]
                        if len(responses[fileno]) == 0:
                            self.epoll.modify(fileno, 0)
                            connections[fileno].shutdown(socket.SHUT_RDWR)
                    elif event & select.EPOLLHUP:
                        self.epoll.unregister(fileno)
                        connections[fileno].close()
                        del connections[fileno]
        finally:
            self.epoll.unregister(self.sock.fileno())
            self.epoll.close()
            self.sock.close()


server = EpollServer(host=SERVER_HOST, port=0)
server.run()
```
