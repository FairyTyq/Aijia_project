# coding:utf-8

import logging
import re

from .BaseHandler import BaseHandler
from models import UserProfile,engine
from sqlalchemy.orm import sessionmaker
from utils.response_code import RET

class IndexHandler(BaseHandler):
    def get(self):
        logging.debug("debug msg")
        logging.info("info msg")
        logging.warning("warning msg")
        logging.error("error msg")
        print "print msg"
        self.write("hello,world!")

class RegisterHandler(BaseHandler):
    def post(self):
        # 获取参数
        mobile = self.json_args.get("mobile") 
        phoneCode = self.json_args.get("phonecode")
        passwd = self.json_args.get("password")
        passwd2 = self.json_args.get("password2")
        # 判断参数是否完整
        if not all((mobile,phoneCode,passwd,passwd2)):
            return self.write(dict(errno=RET.PARAMERR,errmsg="参数不完整"))
        if not re.match(r'1\d{10}',mobile):
            return self.write(dict(errno=RET.PARAMERR,errmsg="手机号不正确"))
        # 从redis中获取手机验证码
        try:
            real_phoneCode = self.redis.get("sms_code_%s"%mobile)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR,errmsg="查询出错"))
        if not real_phoneCode:
            return self.write(dict(errno=RET.NODATA,errmsg="验证码已过期"))
        if real_phoneCode.lower() != phoneCode.lower():
            return self.write(dict(errno=RET.DATAERR,errmsg="验证码错误"))
        # 判断两次密码一致否
        if passwd != passwd2:
            return self.write(dict(errno=RET.DATAERR,errmsg="密码不一致"))
        # 验证成功，则将手机号与密码存入mysql数据库

        Session_sql = sessionmaker(bind=engine)
        session_sql = Session_sql()
        
        usr_tmp = UserProfile(up_name = "u_%s"%mobile,up_mobile = mobile,up_passwd = passwd)
        session_sql.add(usr_tmp)
        print "----------test-------------------------"
        session_sql.commit()
        session_sql.close()


class LoginHandler(BaseHandler):
    def post(self):
        print self.json_args
        mobile = self.json_args.get("mobile")
        passwd = self.json_args.get("passwd")
        session_id = self.json_args.get("session_id")
        
        Session_sql = sessionmaker(bind=engine)
        session_sql = Session_sql()
        real_passwd = session_sql.query(UserProfile.up_passwd).filter(UserProfile.up_mobile==mobile).first()[0]
        print real_passwd
        session_sql.close()
        print "登录状态:%s"%(passwd == real_passwd)
        print self.get_current_user()
        if not self.get_current_user():
            self.session.save()
        print self.json_args







