"""
Date: 2022.05.11 12:58
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.11 12:58
"""
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, TCP, UDP
from scapy.sendrecv import sr

ans = sr(
    IP(dst=["scanme.nmap.org", "nmap.org"]) / TCP(dport=[22, 80, 443, 31337]),
    timeout=3,
    verbose=False,
)[0]

ans.extend(
    sr(
        IP(dst=["scanme.nmap.org", "nmap.org"]) / UDP(dport=53) / DNS(qd=DNSQR()),
        timeout=3,
        verbose=False,
    )[0]
)

ans.make_table(
    lambda x, y: (
        x[IP].dst,
        x.sprintf("%IP.proto%/{TCP:%r,TCP.dport%}{UDP:%r,UDP.dport%}"),
        y.sprintf("{TCP:%TCP.flags%}{ICMP:%ICMP.type%}"),
    )
)
