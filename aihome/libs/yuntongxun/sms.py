#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
import ConfigParser

#主帐号
accountSid= '8aaf07086488623101649165c91307e2'

#主帐号Token
accountToken= '1b5186a95fbd4c9a89b9f1adc1a4b3d8'

#应用Id
appId='8aaf07086488623101649165c97507e9'

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com'

#请求端口 
serverPort='8883'

#REST版本号
softVersion='2013-12-26'

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id

class CCP(object):
    def __new__(cls):
        if not hasattr(cls,"instance"):
            # 判断CCP中 有没有类属性instance
            # 如果没有,则创建这个类的对象,并保存到instance中
            obj = super(CCP, cls).__new__(cls)

            # 初始化REST SDK
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls.instance = obj

        # 如果有,则直接返回
        return cls.instance

# send_template_sms(手机号码,内容数据,模板Id)
    def send_template_sms(self,to, datas, temp_id):
        try:
            # 调用云通讯的工具rest发送短信
            # sendTemplateSMS(手机号码,内容数据["",分钟],模板id)
            result = self.rest.sendTemplateSMS(to, datas, temp_id)
        except Exception as e:
            raise e
        # 返回值
        # {'templateSMS': {'smsMessageSid': '62676c547a194d18b4103b07a69e56e0', 'dateCreated': '20171106182730'},
        # 'statusCode': '000000'}

        status_code = result.get("statusCode")

        if status_code == "000000":
            return 0  # 发送成功
        else:
            return -1  # 发送失败


if __name__ == '__main__':
    ccp = CCP()
    ccp.send_template_sms("18120444388", ["1234", 5], 1)