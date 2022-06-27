"""
Date: 2022.05.11 13:00
Description: Implementing a new protocol
LastEditors: Rustle Karl
LastEditTime: 2022.05.11 13:00
"""
from scapy.compat import raw
from scapy.fields import FieldLenField, PacketLenField
from scapy.layers.dns import DNS, DNSQR
from scapy.packet import Packet
from scapy.supersocket import StreamSocket

"""
Scapy can be easily extended to support new protocols.

The following example defines DNS over TCP. The `DNSTCP` class 
inherits from `Packet` and defines two field: the length, and the real 
DNS message. The `length_of` and `length_from` arguments link the 
`len` and `dns` fields together. Scapy will be able to automatically 
compute the `len` value.
"""


class DNSTCP(Packet):
    name = "DNS over TCP"

    fields_desc = [
        FieldLenField("len", None, fmt="!H", length_of="dns"),
        PacketLenField("dns", 0, DNS, length_from=lambda p: p.len),
    ]

    # This method tells Scapy that the next packet must be decoded with DNSTCP
    def guess_payload_class(self, payload):
        return DNSTCP


# This new packet definition can be directly used to build a DNS message over TCP.

# Build then decode a DNS message over TCP
DNSTCP(raw(DNSTCP(dns=DNS())))

# Modifying the previous StreamSocket example to use TCP allows to use the new DNSCTP layer easily.
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create an TCP socket
s.connect(("8.8.8.8", 53))  # connect to 8.8.8.8 on 53/TCP

# Create the StreamSocket and gives the class used to decode the answer
ss = StreamSocket(s)
ss.basecls = DNSTCP

# Send the DNS query
ss.sr1(DNSTCP(dns=DNS(rd=1, qd=DNSQR(qname="www.example.com"))))
