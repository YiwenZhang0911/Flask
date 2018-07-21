# coding=utf-8
import random

from flask import current_app, jsonify, make_response
from flask import request

from aihome import redis_store, constants
from aihome.api_1_0 import api
from aihome.libs.yuntongxun.sms import CCP
from aihome.utils.captcha.captcha import captcha
from aihome.utils.response_code import RET
from aihome.tasks import task_sms


@api.route("/image_codes/<image_code_id>")
def get_image_code(image_code_id):
    # 获取参数
    # 校验参数
    # 业务处理
    # 生成验证码图片
    # 名字,验证码真实值,图片二进制内容
    name, text, image_data = captcha.generate_captcha()
    try:
        # 将真实值,image_code_id,存入数据库
        # redis_store.set("image_code_%s" % image_code_id,text)
        # 设置redis的数据有效期
        # redis_store.expires("image_code_%s" % image_code_id,constants.IMAGE_CODE_REDIS_EXPIRES)
        redis_store.setex("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        # 日志中记录异常
        current_app.logger.error(e)
        resp = {
            "errno": RET.DBERR,
            "errmsg": "保存验证码失败"
        }
        return jsonify(resp)

    # 返回验证码图片
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp


@api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
def send_sms_code(mobile):
    '''发送短信验证码'''
    # 获取参数
    image_code_id = request.args.get("image_code_id")  # 编号
    image_code = request.args.get("image_code")  # 用户填写的图形验证码


    # 校验参数
    if not all([image_code_id, image_code]):
        resp = {
            "errno": RET.PARAMERR,
            "errmsg": "参数不完整"
        }
        return jsonify(resp)

    # 业务处理
    # 取出图形验证码的真实值
    try:
        real_image_code = redis_store.get("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        resp = {
            "errno": RET.DBERR,
            "errmsg": "获取图形验证码失败"
        }
        return jsonify(resp)

    # 判断验证码是否过期
    if real_image_code is None:
        resp = {
            "errno": RET.NODATA,
            "errmsg": "图形验证码过期"
        }
        return jsonify(resp)
    # 删除redis中的图形验证码,防止用户对此尝试同一个图形验证码
    try:
        redis_store.delete("image_code_%d" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
    # 比对用户填写的验证码和真实的验证码
    if real_image_code.lower() != image_code.lower():
        resp = {
            "errno": RET.DATAERR,
            "errmsg": "图形验证码有误"
        }
        return jsonify(resp)
    # 创建短信验证码
    sms_code = "%06d" % random.randint(0, 999999)
    # 保存短信验证码
    try:
        redis_store.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
    except Exception as e:
        current_app.logger.error(e)
        resp = {
            "errno": RET.DBERR,
            "errmsg": "保存短信验证码异常"
        }
        return jsonify(resp)


    # 发送短信验证码
    # try:
    #     ccp = CCP()
    #     result = ccp.send_template_sms(mobile, [sms_code, str(constants.SMS_CODE_REDIS_EXPIRES / 60)], 1)
    # except Exception as e:
    #     current_app.logger.error(e)
    #     resp = {
    #         "errno": RET.THIRDERR,
    #         "errmsg": "发送短信异常"
    #     }
    #     return jsonify(resp)
    # if result == 0:
    #     resp = {
    #         "errno": RET.OK,
    #         "errmsg": "发送成功"
    #     }
    #     return jsonify(resp)
    # else:
    #     resp = {
    #         "errno": RET.THIRDERR,
    #         "errmsg": "发送短信失败"
    #     }
    #
    #     return jsonify(resp)
    #     # 返回值

    # 使用celery发送短信验证码
    task_sms.send_template_sms.delay(mobile,[sms_code, str(constants.SMS_CODE_REDIS_EXPIRES/60)], 1)

    return jsonify(errno=RET.OK,errmsg="ok")

