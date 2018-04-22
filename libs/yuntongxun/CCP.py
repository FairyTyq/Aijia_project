# coding:utf-8

from CCPRestSDK import REST
import ConfigParser

# 主账号，登录云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
_accountSid='8a216da862dcd1050162e733567c05ae';

# 主账号Token，登录云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken='da5cfeff2ea14b82b4ac202ed11bc891';

# 请使用管理控制台首页的APPID或自己创建应用的APPID
_appId='8a216da862dcd1050162e73356d405b4';

# 请求地址，生产环境配置成app.cloopen.com
_serverIP='app.cloopen.com';

# 请求端口，生产环境为8883
_serverPort='8883';

# REST API版本号保持不变
_softVersion='2013-12-26';

class _CCP(object):
    def __init__(self):
        self.rest = REST(_serverIP,_serverPort,_softVersion)
        self.rest.setAccount(_accountSid,_accountToken)
        self.rest.setAppId(_appId)
    
    # 创建一个单例
    @classmethod
    def instance(cls):
        if not hasattr(cls,"_instance"):
            cls._instance = cls()
        return cls._instance

    def sendTemplateSMS(self,to,datas,tempId):
        return self.rest.sendTemplateSMS(to,datas,tempId)

ccp = _CCP.instance()

if __name__=='__main__':
    ccp.sendTemplateSMS('15122302865',['1234',5],1)

