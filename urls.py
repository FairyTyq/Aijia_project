# coding:utf-8

import os

from handlers import Passport,VerifyCode,Profile,House
# 提取静态文件的Handler
from handlers.BaseHandler import StaticFileHandler

handlers = [
	(r'/api/house/my',House.MyHouseHandler),
	(r'/api/house/image',House.HouseImgHandler),
	(r'/api/house/info',House.HouseInfoHandler),
	(r'/api/house/area',House.AreaInfoHandler),
        (r'/api/check_login',Passport.CheckLoginHandler),
        (r'/api/logout',Profile.LogoutHandler),
        (r'/api/profile/auth',Profile.AuthHandler),
        (r'/api/profile/name',Profile.NicknameHandler),
        (r'/api/profile/avatar',Profile.AvatarHandler),
        (r'/api/profile',Profile.ProfileHandler),
        (r'/api/login',Passport.LoginHandler),
        (r'/api/register',Passport.RegisterHandler),
        (r'/api/imagecode',VerifyCode.ImageCodeHandler),
        (r'/api/smscode',VerifyCode.SMSCodeHandler),
        (r'/(.*)',StaticFileHandler,dict(path=os.path.join(os.path.dirname(__file__),'html'),default_filename='index.html'))
]
