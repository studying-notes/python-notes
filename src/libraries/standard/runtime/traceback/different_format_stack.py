"""
Date: 2022.05.19 14:30:18
LastEditors: Rustle Karl
LastEditTime: 2022.05.20 10:20:18
"""
import traceback


def another_function():
    lumberstack()


def lumberstack():
    print("-" * 60)
    traceback.print_stack()
    print("-" * 60)
    print(repr(traceback.extract_stack()))
    print("-" * 60)
    print(repr(traceback.format_stack()))
    print("-" * 60)


another_function()
