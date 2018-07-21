# coding=utf-8

from flask import Blueprint,current_app,make_response
from flask_wtf.csrf import generate_csrf


html = Blueprint("html",__name__)

# 自定义转换器
@html.route("/<re(r'.*'):file_name>")
def get_html_file(file_name):
    if not file_name:
        file_name = 'index.html'
    if file_name !="favicon.ico":
        file_name = 'html/' + file_name

    # 使用wtf帮助我们生成csrf_token字符串
    csrf_token = generate_csrf()

    resp = make_response(current_app.send_static_file(file_name))

    # 为用户设置cookie csrf_token
    resp.set_cookie("csrf_token",csrf_token)

    return resp
