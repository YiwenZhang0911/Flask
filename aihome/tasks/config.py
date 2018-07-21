# coding=utf-8

BROKER_URL = "redis://127.0.0.1:6379/5"

# 返回文件数据库 与broker不同
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/6"