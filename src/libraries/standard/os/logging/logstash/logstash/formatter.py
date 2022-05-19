"""
Date: 2022.05.18 14:13
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.18 14:13
"""
import json
import logging
import socket
import sys
import time


class LogstashFormatterBase(logging.Formatter):
    converter = time.gmtime  # utc

    default_time_format = '%Y-%m-%dT%H:%M:%S'
    default_msec_format = '%s.%03dZ'

    def __init__(self, msg_type: str, tags: list = None, fqdn: bool = False):
        super().__init__()
        self.msg_type = msg_type
        self.tags = tags if tags is not None else []
        self.hostname = socket.getfqdn() if fqdn else socket.gethostname()

    def get_debug_fields(self, record: logging.LogRecord) -> dict:
        return {
            "line_no": record.lineno,
            "func_name": record.funcName,
            "thread_name": record.threadName,
            "process": record.process,
            "process_name": record.processName,
            "stack_trace": self.formatException(record.exc_info),
        }


class LogstashFormatterVersion1(LogstashFormatterBase):
    def format(self, record):
        message = {
            "@timestamp": self.formatTime(record, self.datefmt),
            "@version": "1",
            "host": {"hostname": self.hostname},
            "level": record.levelname,
            "logger_name": record.name,
            "message": record.getMessage(),
            "path": record.pathname,
            "python_version": sys.version,
            "tags": self.tags,
            "type": self.msg_type,
        }

        if record.exc_info:
            message.update(self.get_debug_fields(record))

        return json.dumps(message, default=str)
