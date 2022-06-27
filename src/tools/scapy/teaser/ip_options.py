"""
Date: 2022.05.10 16:27
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.10 16:27
"""
from scapy.layers.inet import ICMP, IP, IPOption_RR, IPOption_Traceroute
from scapy.sendrecv import sr
from scapy.volatile import RandShort

# Advanced firewalling using IP options is sometimes
# useful to perform network enumeration.

# dst = "192.168.1.79"
dst = "8.8.8.8"
ans = sr(
    [
        IP(dst=dst, ttl=(1, 8), options=IPOption_RR()) / ICMP(seq=RandShort()),
        IP(dst=dst, ttl=(1, 8), options=IPOption_Traceroute()) / ICMP(seq=RandShort()),
        IP(dst=dst, ttl=(1, 8)) / ICMP(seq=RandShort()),
    ],
    verbose=True,
    timeout=3,
)[0]

ans.make_table(
    lambda x, y: (
        ", ".join(z.summary() for z in x[IP].options) or "-",
        x[IP].ttl,
        y.sprintf("%IP.src% %ICMP.type%"),
    )
)
