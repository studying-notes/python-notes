'''
Date: 2021.06.01 16:55
Description : Omit
LastEditors: Rustle Karl
LastEditTime: 2021.06.01 16:55
'''
from celery import Celery

app = Celery('add_task', broker='amqp://admin:admin@localhost:5672/')


@app.task
def add(x, y):
    return x + y
