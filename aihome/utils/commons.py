# coding=utf-8
from functools import wraps

from flask import g
from flask import session, jsonify
from werkzeug.routing import BaseConverter

from aihome.utils.response_code import RET


class RegexConverter(BaseConverter):

    def __init__(self,url_map,regex):
        super(RegexConverter, self).__init__(url_map)
        self.regex=regex


def login_required(view_func):
    """检查用户的登录状态"""
    @wraps(view_func)
    def warpper(*args,**kwargs):
        user_id = session.get("user_id")
        if user_id is not None:
            # 表示用户已登录
            # 使用g对象保存user_id,在视图函数中可以直接使用
            g.user_id = user_id
            return view_func(*args,**kwargs)
        else:
            resp = {
                "errno":RET.SERVERERR,
                "errmsg":"用户未登录"
            }
            return jsonify(resp)
    return warpper