"""
Date: 2022.05.11 11:18
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.11 11:18
"""
from scapy.layers.inet import ICMP, IP
from scapy.sendrecv import srloop


# With srloop(), we can send 100 ICMP packets to 8.8.8.8 and 8.8.4.4.
ans, unans = srloop(
    IP(dst=["8.8.8.8", "8.8.4.4"]) / ICMP(),
    inter=0.1,
    timeout=0.1,
    count=100,
    verbose=False,
)

# %matplotlib inline
ans.multiplot(lambda x, y: (y[IP].src, (y.time, y[IP].id)), plot_xy=True)
