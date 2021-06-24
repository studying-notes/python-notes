"""
Date: 2020-11-30 09:00:29
LastEditors: Rustle Karl
LastEditTime: 2020-11-30 10:54:46
"""
import logging
import os
from logging import Logger
from logging.handlers import RotatingFileHandler


def get_logger(name, log_file: str) -> Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)

    if not log_file.endswith('.log'):
        log_file += '.log'

    log_file = os.path.join(logs_dir, log_file)

    # 日志文件
    file_handler = RotatingFileHandler(
        log_file,
        mode='a',
        encoding='utf-8',
        maxBytes=1024*1024*50,
        backupCount=30
    )
    file_handler.setLevel(logging.INFO)

    # 控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 输出格式
    formatter = logging.Formatter(
        "%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )

    # 为文件输出设定格式
    file_handler.setFormatter(formatter)

    # 控制台输出设定格式
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    logger = get_logger(__name__, "default")
    logger.setLevel(logging.DEBUG)

    logger.debug('logger debug message')
    logger.info('logger info message')
    logger.warning('logger warning message')
    logger.error('logger error message')
    logger.critical('logger critical message')
