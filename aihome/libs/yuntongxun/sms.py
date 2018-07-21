#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
import ConfigParser

#���ʺ�
accountSid= '8aaf07086488623101649165c91307e2'

#���ʺ�Token
accountToken= '1b5186a95fbd4c9a89b9f1adc1a4b3d8'

#Ӧ��Id
appId='8aaf07086488623101649165c97507e9'

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com'

#����˿� 
serverPort='8883'

#REST�汾��
softVersion='2013-12-26'

  # ����ģ�����
  # @param to �ֻ�����
  # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
  # @param $tempId ģ��Id

class CCP(object):
    def __new__(cls):
        if not hasattr(cls,"instance"):
            # �ж�CCP�� ��û��������instance
            # ���û��,�򴴽������Ķ���,�����浽instance��
            obj = super(CCP, cls).__new__(cls)

            # ��ʼ��REST SDK
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls.instance = obj

        # �����,��ֱ�ӷ���
        return cls.instance

# send_template_sms(�ֻ�����,��������,ģ��Id)
    def send_template_sms(self,to, datas, temp_id):
        try:
            # ������ͨѶ�Ĺ���rest���Ͷ���
            # sendTemplateSMS(�ֻ�����,��������["",����],ģ��id)
            result = self.rest.sendTemplateSMS(to, datas, temp_id)
        except Exception as e:
            raise e
        # ����ֵ
        # {'templateSMS': {'smsMessageSid': '62676c547a194d18b4103b07a69e56e0', 'dateCreated': '20171106182730'},
        # 'statusCode': '000000'}

        status_code = result.get("statusCode")

        if status_code == "000000":
            return 0  # ���ͳɹ�
        else:
            return -1  # ����ʧ��


if __name__ == '__main__':
    ccp = CCP()
    ccp.send_template_sms("18120444388", ["1234", 5], 1)