# coding:utf-8
from handlers import Passport,VerifyCode

handlers = [
        (r'/',Passport.IndexHandler),
        (r'/api/imagecode',VerifyCode.ImageCodeHandler),
]
