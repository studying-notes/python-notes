---
date: 2020-12-16T12:46:16+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Python 蓝牙模块"  # 文章标题
url:  "posts/py/libraries/tripartite/pybluez"  # 设置网页永久链接
tags: [ "python", "蓝牙" ]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类
# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

```shell
apt-get install -y libbluetooth-dev libboost-python-dev libboost-all-dev
```

```shell
pip install pybluez
```

## 编译问题

必须安装 VC++ 14.0 以上

## 获取本机蓝牙地址

```py
import bluetooth

print(bluetooth.read_local_bdaddr())
```

## 查询设备服务

```py
import bluetooth

nearby_devices = bluetooth.discover_devices(lookup_names=True)

for addr, name in nearby_devices:
    print("%s - %s" % (addr, name))

    services = bluetooth.find_service(address=addr)

    for svc in services:
        print("Service Name: %s" % svc["name"])
        print("\tHost: %s" % svc["host"])
        print("\tDescription: %s" % svc["description"])
        print("\tProvided By: %s" % svc["provider"])
        print("\tProtocol: %s" % svc["protocol"])
        print("\tChannel/PSM: %s" % svc["port"])
        print("\tService Classes: %s " % svc["service-classes"])
        print("\tProfiles: %s " % svc["profiles"])
        print("\tService Id: %s " % svc["service-id"])

    print('-------------------------------------------')
```

## 通过名称寻找通信对象

```py
import bluetooth

target_name = "PDD-150BT-53EE"
target_address = None

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
    find_name = bluetooth.lookup_name(bdaddr)
    if target_name == find_name:
        target_address = bdaddr
        break
    print(find_name)

if target_address is not None:
    print("found target bluetooth device with address ", target_address)
else:
    print("could not find target bluetooth device nearby")
```

## 通过 RFCOMM 方式进行通信

```py

```

```py

```


```py

```


```py

```


```py

```


```py

```


```py

```


```py

```


