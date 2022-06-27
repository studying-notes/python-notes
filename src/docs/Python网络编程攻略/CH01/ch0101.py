"""
Date: 2022.04.07 21:28:14
LastEditors: Rustle Karl
LastEditTime: 2022.04.08 11:04:13
"""
from ipaddress import ip_address
import socket
from binascii import hexlify

from sympy import im

host_name = socket.gethostname()
host = socket.gethostbyname(host_name)

socket.gethostbyname("baidu.com")

ip_address = "220.181.38.251"
packed_ip_address = socket.inet_aton(ip_address)
hexlify(packed_ip_address)
socket.inet_ntoa(packed_ip_address)
socket.getservbyport(80, "tcp")

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

addr = ("", 8080)  # all interfaces, port 8080
if socket.has_dualstack_ipv6():
    print("has_dualstack_ipv6")
    # 平台支持创建 IPv4 和 IPv6 连接都可以处理的 TCP 套接字
    s = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
else:
    s = socket.create_server(addr)

client, client_address = s.accept()
client.send(b"OK")

# 关闭一个套接字文件描述符
s.close()

"""
将 host/port 参数转换为 5 元组的序列，其中包含创建（连接到某服务的）套接字所需的所有参数。host 是域名，是字符串格式的 IPv4/v6 地址或 None。port 是字符串格式的服务名称，如 'http' 、端口号（数字）或 None。传入 None 作为 host 和 port 的值，相当于将 NULL 传递给底层 C API。

可以指定 family、type 和 proto 参数，以缩小返回的地址列表。向这些参数分别传入 0 表示保留全部结果范围。flags 参数可以是 AI_* 常量中的一个或多个，它会影响结果的计算和返回。例如，AI_NUMERICHOST 会禁用域名解析，此时如果 host 是域名，则会抛出错误。
"""
socket.getaddrinfo("baidu.com", 80, proto=socket.IPPROTO_TCP)

s.settimeout(100)

try:
    s.accept()
except socket.gaierror as e:
    print(e)
except socket.error as e:
    print(e)

SEND_BUF_SIZE = 4096
RECV_BUF_SIZE = 4096
buf_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUF_SIZE)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SIZE)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(1)
s.settimeout(0.5)
s.bind(("127.0.0.1", 0))
socket_address = s.getsockname()
while (1):
    s.listen(1)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

import ntplib
from time import ctime
ntp_client = ntplib.NTPClient()
response = ntp_client.request("pool.ntp.org")
ctime(response.tx_time)