"""
Date: 2022.05.10 16:41
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.10 16:41
"""
from pprint import pprint

from scapy.layers.inet import ICMP, IP, TCP
from scapy.layers.l2 import Ether

from scapy.packet import ls

# 建议在 Linux 系统下测试，Windows 内核限制了很多底层协议

# The '/' operator is used to bind layers together.
Ether() / IP() / TCP()
# <Ether  type=IPv4 |<IP  frag=0 proto=tcp |<TCP  |>>>

# Protocol fields can be listed using the ls() function:
ls(IP, verbose=True)
"""
version    : BitField  (4 bits)                  = ('4')
ihl        : BitField  (4 bits)                  = ('None')
tos        : XByteField                          = ('0')
len        : ShortField                          = ('None')
id         : ShortField                          = ('1')
flags      : FlagsField                          = ('<Flag 0 ()>')
               MF, DF, evil
frag       : BitField  (13 bits)                 = ('0')
ttl        : ByteField                           = ('64')
proto      : ByteEnumField                       = ('0')
               ip: 0
               icmp: 1
               ggp: 3
               tcp: 6
               egp: 8
               pup: 12
               udp: 17
               hmp: 20
               xns_idp: 22
               rdp: 27
               ipv6: 41
               ipv6_route: 43
               ipv6_frag: 44
               esp: 50
               ah: 51
               ipv6_icmp: 58
               ipv6_nonxt: 59
               ipv6_opts: 60
               rvd: 66
chksum     : XShortField                         = ('None')
src        : SourceIPField                       = ('None')
dst        : DestIPField                         = ('None')
options    : PacketListField                     = ('[]')
"""

p = Ether() / IP(dst="www.secdev.org") / TCP()
p.summary()
# 'Ether / IP / TCP 192.168.0.117:ftp_data > Net("www.secdev.org/32"):http S'


# Using internal mechanisms (such as DNS resolution, routing table and
# ARP resolution), Scapy has automatically set fields necessary to send
# the packet. These fields can of course be accessed and displayed.
print(p.dst)  # first layer that has an src field, here Ether
print(p[IP].src)  # explicitly access the src field of the IP layer

# sprintf() is a useful method to display fields
print(p.sprintf("%Ether.src% > %Ether.dst%\n%IP.src% > %IP.dst%"))

# Scapy uses default values that work most of the time.
# For example, TCP() is a SYN segment to port 80.
print(p.sprintf("%TCP.flags% %TCP.dport%"))

# Moreover, Scapy has implicit packets. For example, they are useful to
# make the TTL field value vary from 1 to 5 to mimic traceroute.
ps = [p for p in IP(ttl=(1, 5)) / ICMP()]
pprint(ps)
