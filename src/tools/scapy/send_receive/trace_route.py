"""
Date: 2022.05.11 11:27
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.11 11:27
"""
from scapy.layers.inet import traceroute

ans, unans = traceroute("www.secdev.org", maxttl=15)
"""
   217.25.178.5:tcp80 
1  172.24.16.1     11 
2  192.168.4.1     11 
9  202.97.43.70    11 
15 184.105.81.166  11 
"""

# The result can be plotted with .world_trace() (this requires GeoIP module and data, from MaxMind)
ans.world_trace()
