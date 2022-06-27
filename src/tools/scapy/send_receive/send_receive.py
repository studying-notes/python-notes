"""
Date: 2022.05.11 10:28
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.11 10:28
"""
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import ICMP, IP, UDP
from scapy.layers.l2 import Ether
from scapy.sendrecv import sniff, sr1, srp

#  use the DNS protocol to get www.example.com IPv4 address
from scapy.utils import rdpcap, wrpcap

p = sr1(IP(dst="8.8.8.8") / UDP() / DNS(qd=DNSQR()))
p[DNS].an
# <DNSRR  rrname='www.example.com.' type=A rclass=IN ttl=5280 rdlen=None rdata=93.184.216.34 |>

# Another alternative is the sr() function. Like srp1(), the sr1() function can be used for layer 2 packets.
r, u = srp(
    Ether()
    / IP(dst="8.8.8.8", ttl=(5, 10))
    / UDP()
    / DNS(rd=1, qd=DNSQR(qname="www.example.com"))
)
r  #  is a list of results (i.e. tuples of the packet sent and its answer)
u  # is a list of unanswered packets

# Access the first tuple
print(r[0][0].summary())  # the packet sent
print(r[0][1].summary())  # the answer received

# Access the ICMP layer. Scapy received a time-exceeded error message
r[0][1][ICMP]

# With Scapy, list of packets, such as r or u, can be easily written to, or read from PCAP files.
wrpcap("scapy.pcap", r)

pcap_p = rdpcap("scapy.pcap")
pcap_p[0]

# Sniffing the network is as straightforward as sending and receiving packets.
s = sniff(count=2)
# <Sniffed: TCP:0 UDP:2 ICMP:0 Other:0>
sniff(count=2, prn=lambda p: p.summary())

# The raw() constructor can be used to “build” the packet’s bytes as they would be sent on the wire.
pkt = IP() / UDP() / DNS(qd=DNSQR())
print(repr(raw(pkt)))
print(pkt.summary())

# "hexdump" the packet's bytes
hexdump(pkt)

# dump the packet, layer by layer, with the values for each field
pkt.show()

# render a pretty and handy dissection of the packet
pkt.canvas_dump()
