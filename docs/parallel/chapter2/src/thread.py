'''
Date: 2021.06.01 09:27:39
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2021.06.01 09:31:38
'''
import threading
from typing import List


def function(i):
    print("function called by thread %i\n" % i)
    return


threads: List[threading.Thread] = []

for i in range(5):
    t = threading.Thread(target=function, args=(i, ))
    threads.append(t)
    t.start()
    # t.join()

for t in threads:
    t.join()
