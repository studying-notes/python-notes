"""
Date: 2022.05.19 14:30:18
LastEditors: Rustle Karl
LastEditTime: 2022.05.19 14:30:23
"""
import traceback


def another_function():
    lumberstack()


def lumberstack():
    traceback.print_stack()
    print(repr(traceback.extract_stack()))
    print(repr(traceback.format_stack()))


another_function()
