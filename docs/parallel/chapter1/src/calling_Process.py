'''
Date: 2021.05.31 17:16:37
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2021.05.31 17:24:19
'''
import os

# this is the code to execute
program = "python"
print("Process calling")

arguments = ["called_Process.py"]

# we call the called_Process.py script
# 将执行一个新程序，以替换当前进程
os.execvp(program, (program,) + tuple(arguments))

# 该代码不可达
print("Good Bye!!")
