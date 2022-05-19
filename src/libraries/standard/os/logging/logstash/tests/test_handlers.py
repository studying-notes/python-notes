"""
Date: 2022.05.18 14:39
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.18 14:39
"""
import logging

import logstash.handlers


def test_logstash_tcp_handler():
    log = logging.getLogger("logstash-py-test")
    log.setLevel(logging.DEBUG)
    log.addHandler(logstash.handlers.LogstashTCPHandler("192.168.0.18", 15000))

    for _ in range(100000):
        log.debug("It's a DEBUG message")
        log.info("It's a INFO message'")
        log.warning("It's a WARN message'")
        log.error("It's a ERROR message'")
        log.critical("It's a CRITICAL message'")
        log.exception("It's a EXCEPTION message'")
