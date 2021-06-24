'''
Date: 2021.04.30 15:55
Description : Omit
LastEditors: Rustle Karl
LastEditTime: 2021.04.30 15:55
'''
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

dt = datetime(2020, 10, 21, 12, tzinfo=ZoneInfo('America/Los_Angeles'))
print(dt)

dt += timedelta(days=7)
print(dt)
