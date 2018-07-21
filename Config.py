# coding=utf-8
import redis


class Config(object):
    '''工程配置信息'''
    SECRET_KEY = '%&$%^#LKJLKHD&%&*&)()UF6434131**&Y*SHKDJY*131'
    # 数据库配置信息
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/Ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    # flask_session用到的配置信息
    SESSION_TYPE = "redis"  # 指定保存到redis中
    SESSION_USE_SIGNER=True  # 让cookie中的session_id被加密签名处理
    # 使用的redis实例
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 86400  # session的有效期,单位秒


class DevelopmentConfig(Config):
    """开发模式使用的配置信息"""
    DEBUG = True
    # 支付宝
    ALIPAY_APPID = "2016081600258081"
    ALIPAY_URL = "https://openapi.alipaydev.com/gateway.do"

class ProductionConfig(Config):
    """生产模式 线上模式的配置信息"""
    pass

config_dict={
    "develop":DevelopmentConfig,
    "product":ProductionConfig,

}