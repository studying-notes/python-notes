"""
Date: 2022.05.10 16:25
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.10 16:25
"""
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import send

# Sending a TCP segment with maximum segment size set to 0 to a specific
# port is an interesting test to perform against embedded TCP stacks.
send(IP(dst="192.168.1.79") / TCP(dport=80, options=[("MSS", 0)]))
