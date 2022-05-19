"""
Date: 2022.05.18 14:13
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.18 14:13
"""
from logging.handlers import DatagramHandler, SocketHandler
from . import formatter


class LogstashTCPHandler(SocketHandler):
    def __init__(self, host, port=15000, msg_type="python", tags=None, fqdn=False):
        super(LogstashTCPHandler, self).__init__(host, port)
        self.formatter = formatter.LogstashFormatterVersion1(msg_type, tags, fqdn)

    def makePickle(self, record):
        return self.formatter.format(record).encode("utf-8") + b"\n"


class LogstashUDPHandler(LogstashTCPHandler, DatagramHandler):
    pass
