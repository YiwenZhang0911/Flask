# coding=utf-8

# 绑定蓝图路由
from . import api
from aihome import db, models

@api.route("/index")
def index():
    return 'index page'
