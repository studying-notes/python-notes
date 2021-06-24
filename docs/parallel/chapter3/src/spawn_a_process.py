'''
Date: 2021.06.01 14:25
Description : Omit
LastEditors: Rustle Karl
LastEditTime: 2021.06.01 14:25
'''

import multiprocessing


def foo(i):
    print('called function in process: %s' % i)


if __name__ == '__main__':
    process_jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=foo, args=(i,))
        process_jobs.append(p)
        p.start()
        p.join()
