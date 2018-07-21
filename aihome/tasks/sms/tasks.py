# coding=utf-8
from aihome.tasks.main import app
from libs.yuntongxun.sms import CCP


@app.task
def send_template_sms(to,datas,temp_id):
    ccp = CCP()
    ccp.send_template_sms(to,datas,temp_id)