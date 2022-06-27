"""
Date: 2022.05.11 13:14
Description: Cheap Man-in-the-middle with NFQUEUE
LastEditors: Rustle Karl
LastEditTime: 2022.05.11 13:14
"""
from scapy.compat import raw
from scapy.layers.inet import ICMP, IP
import nfqueue
import socket

"""
NFQUEUE is an iptables target than can be used to transfer packets to 
userland process. As a nfqueue module is available in Python, you can 
take advantage of this Linux feature to perform Scapy based MiTM.

This example intercepts ICMP Echo request messages sent to 8.8.8.8, 
sent with the ping command, and modify their sequence numbers. 
In order to pass packets to Scapy, the following `iptables` command 
put packets into the NFQUEUE #2807:

iptables -I OUTPUT --destination 8.8.8.8 -p icmp -o eth0 -j NFQUEUE --queue-num 2807
"""


def scapy_cb(i, payload):
    s = payload.get_data()  # get and parse the packet
    p = IP(s)

    # Check if the packet is an ICMP Echo Request to 8.8.8.8
    if p.dst == "8.8.8.8" and ICMP in p:
        # Delete checksums to force Scapy to compute them
        del (p[IP].chksum, p[ICMP].chksum)

        # Set the ICMP sequence number to 0
        p[ICMP].seq = 0

        # Let the modified packet go through
        ret = payload.set_verdict_modified(nfqueue.NF_ACCEPT, raw(p), len(p))

    else:
        # Accept all packets
        payload.set_verdict(nfqueue.NF_ACCEPT)


# Get an NFQUEUE handler
q = nfqueue.queue()
# Set the function that will be call on each received packet
q.set_callback(scapy_cb)
# Open the queue & start parsing packes
q.fast_open(2807, socket.AF_INET)
q.try_run()
