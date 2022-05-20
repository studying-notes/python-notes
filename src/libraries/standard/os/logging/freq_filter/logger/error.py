"""
Date: 2022.05.20 09:37:35
LastEditors: Rustle Karl
LastEditTime: 2022.05.20 10:55:54
"""

#############################
#     Logging subsystem     #
#############################

import logging
import re
import traceback
import time
from typing import Dict, Tuple
import warnings
import colorama

# Typing imports
from logging import LogRecord, warning


colorama.init()


class PackageException(Exception):
    pass


class PackageInvalidPlatformException(PackageException):
    pass


class PackageFreqFilter(logging.Filter):
    def __init__(self) -> None:
        # super().__init__()
        logging.Filter.__init__(self)
        self.warning_table: Dict[int, Tuple[float, int]] = {}

    def filter(self, record: LogRecord) -> bool:
        if record.levelno <= logging.INFO:
            return True

        warning_threshold = 8
        if warning_threshold > 0:
            caller = 0
            stack_summary = traceback.extract_stack()

            for _, l, n, _ in stack_summary:
                if n == "warning":
                    break
                caller = l

            # 时间，次数
            tm, nb = self.warning_table.get(caller, (0, 0))
            ltm = time.time()

            if ltm - tm > warning_threshold:
                tm = ltm
                nb = 0
            else:
                if nb < 2:
                    nb += 1
                    if nb == 2:
                        record.msg = "more" + record.msg
                else:
                    return False

            self.warning_table[caller] = (tm, nb)

        return True


class PackageColoredFormatter(logging.Formatter):

    levels_colored = {
        "DEBUG": "reset",
        "INFO": "reset",
        "WARNING": "bold+yellow",
        "ERROR": "bold+red",
        "CRITICAL": "bold+white+bg_red",
    }

    def format(self, record: LogRecord) -> str:
        message = super().format(record)
        # return color.format(message, self.levels_colored[record.levelname])
        return message


# get package's master logger
log_package = logging.getLogger("package")

# override the level if not already set
if log_package.level == logging.NOTSET:
    log_package.setLevel(logging.WARNING)

# add a custom handler controlled by package's config
_handler = logging.StreamHandler()
_handler.setFormatter(PackageColoredFormatter("%(levelname)s: %message)s"))
log_package.addHandler(_handler)

# logs at runtime
log_runtime = logging.getLogger("package.runtime")
log_runtime.addFilter(PackageFreqFilter())

# logs in interactive functions
log_interactive = logging.getLogger("package.interactive")
log_interactive.setLevel(logging.DEBUG)

# logs when loading package
log_loading = logging.getLogger("package.loading")


def warning(msg, *args, **kwargs):
    """Prints a warning during runtime."""
    log_runtime.warning(msg, *args, **kwargs)
 