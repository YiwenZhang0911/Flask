# coding=utf-8

from celery import Celery

app = Celery("aihome")

# app.config_from_object(config)
app.config_from_object("aihome.tasks.config")

# 让celery自己找到任务
app.autodiscover_tasks(["aihome.tasks.sms"])