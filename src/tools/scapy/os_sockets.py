"""
Date: 2022.05.11 11:15
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.11 11:15
"""

import socket

from scapy.layers.dns import DNS, DNSQR
from scapy.supersocket import StreamSocket

# Alternatively, Scapy can use OS sockets to send and receive packets.
# Unlike other Scapy sockets, StreamSockets do not require root privileges.

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create an UDP socket
s.connect(("8.8.8.8", 53))  # connect to 8.8.8.8 on 53/UDP

# Create the StreamSocket and gives the class used to decode the answer
ss = StreamSocket(s)
ss.basecls = DNS

# Send the DNS query
ss.sr1(DNS(rd=1, qd=DNSQR(qname="www.example.com")))
