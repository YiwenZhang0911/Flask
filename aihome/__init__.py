# coding=utf-8
import logging
from flask import Flask
from flask_session import Session
from Config import config_dict
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from logging.handlers import RotatingFileHandler
from utils.commons import RegexConverter


# 构建数据库对象

db = SQLAlchemy()

# 构建redis连接对象
redis_store=None

# 为flask补充csrf防护机制
csrf = CSRFProtect()

# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)
# 创建日志记录器  指明文件路径,文件大小,保存日志文件的个数上限
file_log_handler = RotatingFileHandler("logs/log",maxBytes=1024*1024*100,backupCount=10)
# 创建日志记录的格式  日志等级  输入日志信息的文件名  行数  日志信息
formatter = logging.Formatter('%(levelname)s%(filename)s:%(lineno)d%(message)s')
# 为刚创建的日志记录器设置日志记录的格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象(flask app使用的)添加日志记录器
logging.getLogger().addHandler(file_log_handler)


# 工厂模式
def create_app(conf_name):
    """创建flask应用对象"""

    # 创建应用对象
    app = Flask(__name__)

    # 设置flask的配置信息
    conf = config_dict[conf_name]
    app.config.from_object(conf)

    # 初始化数据库db
    db.init_app(app)

    # 初始化redis
    global redis_store
    redis_store = redis.StrictRedis(host=conf.REDIS_HOST, port=conf.REDIS_PORT)
    # 初始化
    # csrf.init_app(app)

    # 将flask里的session数据保存到redis中
    Session(app)

    # 向app中添加自定义路由转换器
    app.url_map.converters["re"] = RegexConverter

    # 注册蓝图
    import api_1_0
    app.register_blueprint(api_1_0.api,url_prefix="/api/v1_0")

    # 提供html静态文件的蓝图
    import web_html
    app.register_blueprint(web_html.html)

    return app

