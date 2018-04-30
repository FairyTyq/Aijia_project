# coding:utf-8

import os

from handlers import Passport,VerifyCode,Profile
# 提取静态文件的Handler
from handlers.BaseHandler import StaticFileHandler

handlers = [
        (r'/api/profile',Profile.ProfileHandler),
        (r'/api/profile/avatar',Profile.AvatarHandler),
        (r'/api/login',Passport.LoginHandler),
        (r'/api/register',Passport.RegisterHandler),
        (r'/api/imagecode',VerifyCode.ImageCodeHandler),
        (r'/api/smscode',VerifyCode.SMSCodeHandler),
        (r'/(.*)',StaticFileHandler,dict(path=os.path.join(os.path.dirname(__file__),'html'),default_filename='index.html'))
]
