"""
Date: 2022.05.19 13:46:23
LastEditors: Rustle Karl
LastEditTime: 2022.05.19 14:22:19
"""
import sys, traceback


def run_user_code(envdir):
    source = input(">>> ")

    try:
        exec(source, envdir)
    except Exception:
        print("Exception in user code:")
        print("-" * 60)
        traceback.print_exc(file=sys.stdout)
        print("-" * 60)


envdir = {}
while True:
    run_user_code(envdir)
