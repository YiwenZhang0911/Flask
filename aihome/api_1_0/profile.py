# coding=utf-8
from flask import current_app,g, jsonify,request,session
from aihome import constants, db
from aihome.models import User
from aihome.api_1_0 import api
from aihome.utils.commons import login_required
from aihome.utils.image_storage import storage
from aihome.utils.response_code import RET


@api.route("/users/avatar", methods=["POST"])
@login_required
def set_user_avatar():
    """设置用户头像"""
    # 获取参数, 头像图片、用户
    user_id = g.user_id
    image_file = request.files.get("avatar")

    # 校验参数
    if image_file is None:
        # 表示用户没有上传头像
        return jsonify(errno=RET.PARAMERR, errmsg="未上传头像")

    # 保存用户头像数据
    image_data = image_file.read()
    try:
        file_name = storage(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="上传头像异常")

    # 将文件名信息保存到数据库中
    try:
        User.query.filter_by(id=user_id).update({"avatar_url": file_name})
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存头像信息失败")

    avatar_url = constants.QINIU_URL_DOMAIN + file_name

    # 返回值
    return jsonify(errno=RET.OK, errmsg="保存头像成功", data={"avatar_url": avatar_url})




# 请求url,请求方式,更新个人信息PUT
@api.route("/user/name",methods=["PUT"])
@login_required
def change_user_name():
    """修改用户名"""
    # 使用login_required装饰器,可以使用g对象获取用户id
    user_id = g.user_id
    # 获取用户想要设置的用户名,从前端获取用户输入的数据
    req_data = request.get_json()

    # 校验参数
    if not req_data:
        return jsonify(errno=RET.PARAMERR,errmsg="参数不完整")

    name = req_data.get("name")  # 用户想要设置的名字
    if not name:
        return jsonify(errno=RET.PARAMERR,errmsg="名字不能为空")

    # 保存用户昵称name,并同时判断name是否重复(利用数据库的unique)
    try:
        User.query.filter_by(id=user_id).update({"name":name})
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()  # 事务回滚
        return jsonify(errno=RET.DBERR,errmsg="设置用户错误")

    # 修改session数据中的name字段
    session["user_name"]=name

    return jsonify(errno=RET.OK,errmsg="ok",data={"name": name})


@api.route("/user", methods=["GET"])
@login_required
def get_user_profile():
    """获取个人信息"""
    user_id = g.user_id
    # 查询数据库获取个人信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")

    if user is None:
        return jsonify(errno=RET.NODATA, errmsg="无效操作")

    return jsonify(errno=RET.OK, errmsg="OK", data=user.to_dict())




# @api.route("/user/auth",methods=["GET"])
# @login_required
# def get_user_auth():
#     """获取用户的实名认证信息"""
#     user_id = g.user_id
#
#     # 获取参数
#     try:
#         user = User.query.get(user_id)
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR,errmsg="获取用户失败")
#     # 校验参数
#     if user is None:
#         return jsonify(errno=RET.NODATA,errmsg="无效操作")
#     #返回值
#     return jsonify(errno=RET.OK,errmsg="ok",data=user.auth_to_dict())

@api.route("/user/auth", methods=["GET"])
@login_required
def get_user_auth():
    """获取用户的实名认证信息"""
    user_id = g.user_id

    # 在数据库中查询信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户实名信息失败")

    if user is None:
        return jsonify(errno=RET.NODATA, errmsg="无效操作")

    return jsonify(errno=RET.OK, errmsg="OK", data=user.auth_to_dict())



# @api.route("/user/auth",methods=["POST"])
# @login_required
# def set_user_auth():
#     """保存实名认证信息"""
#     user_id = g.user_id
#     # 获取参数
#     req_data = request.get_json()
#     if not req_data:
#         return jsonify(errno=RET.PARAMERR,errmsg="参数错误")
#     real_name = req_data.get("real_name")
#     id_card = req_data.get("id_card")
#
#     # 校验参数
#     if not all([real_name,id_card]):
#         return jsonify(errno=RET.PARAMERR,errmsg="参数错误")
#     # 业务逻辑
#     # 保存用户的姓名与身份证好
#     try:
#         User.query.filter_by(id=user_id,real_name=None,id_card=None).update({"real_name":real_name,"id_card":id_card})
#         db.session.commit()
#     except Exception as e:
#         current_app.logger.error(e)
#         db.session.rollback()  # 事务回滚
#         return jsonify(errno=RET.DBERR,errmsg="保存用户实名认证失败")
#     # 返回值
#     return jsonify(errno=RET.OK,errmsg="ok")

@api.route("/user/auth", methods=["POST"])
@login_required
def set_user_auth():
    """保存实名认证信息"""
    user_id = g.user_id

    # 获取参数
    req_data = request.get_json()
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    real_name = req_data.get("real_name")  # 真实姓名
    id_card = req_data.get("id_card")  # 身份证号

    # 参数校验
    if not all([real_name, id_card]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 保存用户的姓名与身份证号
    try:
        User.query.filter_by(id=user_id, real_name=None, id_card=None)\
            .update({"real_name": real_name, "id_card": id_card})
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存用户实名信息失败")

    return jsonify(errno=RET.OK, errmsg="OK")