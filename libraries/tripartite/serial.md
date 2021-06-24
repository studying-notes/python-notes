---
date: 2020-12-17T10:10:53+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Python 串口读写"  # 文章标题
# description: "文章描述"
url:  "posts/py/libraries/tripartite/serial"  # 设置网页永久链接
tags: [ "python", "串口" ]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

## 单片机

- TXD 发送数据 Transmit Data 简写形式  
- RXD 接收数据 Receive Data 简写形式
- VCC 电路的供电电压
- VDD 芯片的工作电压

## 4针 USB

- 红色－ 供电：标有－ VCC、Power、5V、5VSB 字样
- 白色－ USB 数据线：（负）－ DATA-、USBD-、PD-、USBDT-
- 绿色－ USB 数据线：（正）－ DATA+、USBD+、PD+、USBDT+
- 黑色－地线：GND、Ground

## 驱动

```url
https://wwa.lanzous.com/i2Xdqjfwsrg
```

## 示例

```py
import serial
from time import sleep


def checksum(model_id, param_h, param_l, data_h, data_l):
    return 0x100-(model_id+0x06+param_h+param_l+data_h+data_l) % 0x100


def combine_cmd(model_id, param_h, param_l, data_h, data_l):
    return ':%02x06%02x%02x%02x%02x%02x\r\n' % (model_id, param_h, param_l, data_h, data_l,
                                                checksum(model_id, param_h, param_l, data_h, data_l))


if __name__ == '__main__':
    s = serial.Serial('COM3', baudrate=115200, timeout=1,
                      bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE,
                      parity=serial.PARITY_NONE)
    if not s.is_open:
        raise serial.PortNotOpenError("open failed")

    print("open success")

    cnt = 1
    while cnt < 0xFF:
        cmd = combine_cmd(cnt, 0x80, 0x00, 0x00, 0xFC).upper()
        print(cmd)
        s.write(cmd.encode(encoding='ASCII'))
        recv = s.read_all()
        if recv != b'':
            print("recv: ", recv)
            break
        cnt += 1
        sleep(0.1)
```
