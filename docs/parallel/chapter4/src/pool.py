'''
Date: 2021.06.01 15:50
Description : Omit
LastEditors: Rustle Karl
LastEditTime: 2021.06.01 15:50
'''
import concurrent.futures
import time

number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def evaluate_item(x):
    # 计算总和，这里只是为了消耗时间
    result_item = count(x)

    # 打印输入和输出结果
    return result_item


def count(number):
    i = 0
    for i in range(0, 10000000):
        i = i + 1
    return i * number


if __name__ == "__main__":
    # 顺序执行
    start_time = time.time()
    for item in number_list:
        print(evaluate_item(item))
    print("Sequential execution in " + str(time.time() - start_time), "seconds")

    # 线程池执行
    start_time_1 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(evaluate_item, item) for item in number_list]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())
    print("Thread pool execution in " + str(time.time() - start_time_1), "seconds")

    # 进程池
    start_time_2 = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(evaluate_item, item) for item in number_list]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())
    print("Process pool execution in " + str(time.time() - start_time_2), "seconds")
