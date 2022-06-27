"""
Date: 2022.04.08 21:05:01
LastEditors: Rustle Karl
LastEditTime: 2022.04.08 21:38:14
"""
import subprocess
import shlex

command_line = "ping -c 1 www.google.com"
args = shlex.split(command_line)
try:
    subprocess.check_call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Google web server is up!")
except subprocess.CalledProcessError:
    print("Failed to get ping.")


from shlex import join

print(join(["echo", "-n", "Multiple words"]))

# 以下用法是不安全的：
filename = "somefile; rm -rf ~"
command = "ls -l {}".format(filename)
print(command)  # executed by a shell: boom!

# 用 quote() 可以堵住这种安全漏洞：

from shlex import quote
command = 'ls -l {}'.format(quote(filename))
print(command)

remote_command = 'ssh home {}'.format(quote(command))
print(remote_command)
