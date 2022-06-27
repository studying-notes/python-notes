#############################
#     Logging subsystem     #
#############################

import logging
import traceback
import time
import warnings


# Typing imports
from logging import LogRecord
from typing import Any, Dict, Tuple



class MyException(Exception):
    pass


class MyInvalidPlatformException(MyException):
    pass


class MyNoDstMacException(MyException):
    pass

