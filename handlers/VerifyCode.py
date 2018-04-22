# coding:utf-8

import logging
import constants
import random
import constants
import re

from utils.captcha.captcha import captcha
from .BaseHandler import BaseHandler
from libs.yuntongxun.CCP import ccp
from utils.response_code import RET

class ImageCodeHandler(BaseHandler):
    """ """
    def get(self):
        code_id = self.get_argument("codeid")
        pre_code_id = self.get_argument("pcodeid")
        if pre_code_id:
            try:
                self.redis.delete("image_code_%s"%pre_code_id)
            except Exception as e:
                logging.error(e)
        # name 图片验证码名称
        # text 图片验证码文本
        # image 图片验证码二进制数据
        name,text,image = captcha.generate_captcha()
        try:
            self.redis.setex("image_code_%s"%code_id,constants.IMAGE_CODE_EXPIRES_SECONDS,text)
        except Exception as e:
            logging.error(e)
            self.write("")
        self.set_header("Content-Type","image/jpg")
        self.write(image)

class SMSCodeHandler(BaseHandler):
    """ """
    def post(self):
#        usr_data = self.get_body_argument("")
#        phone = usr_data["mobile"]
#        ic_id = usr_data["image_code_id"]
#        ic_text = usr_data["image_code_text"] 
#        if self.redis.get("ic_id") == ic_text:
#            ccp = _CCP.instance()
#            ccp.sendTemplateSMS(phone,[,5],1)
        # 获取参数
        mobile = self.json_args.get("mobile")
        image_code_id = self.json_args.get("image_code_id")
        image_code_text = self.json_args.get("image_code_text")
        # 判断参数是否完整
        if not all((mobile,image_code_id,image_code_text)):
            return self.write(dict(errno=RET.PARAMERR,errmsg="参数不完整"))
        if not re.match(r'1\d{10}',mobile):
            return self.write(dict(errno=RET.PARAMERR),errmsg="手机号不正确")
        # 判断图片验证码
        try:
            real_image_code_text = self.redis.get("image_code_%s"%image_code_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR),errmsg="查询出错")
        if not real_image_code_text:
            return self.write(dict(errno=RET.NODATA,errmsg="验证码已过期！"))
        if real_image_code_text.lower() != image_code_text.lower():
            return self.write(dict(errno=RET.DATAERR,errmsg="验证码错误！"))
        # 若验证成功，生成随机验证码
        sms_code = "%04d"%random.randint(0,9999)
        try:
            self.redis.setex("sms_code_%s"%mobile,constants.SMS_CODE_EXPIRES_SECONDS,sms_code)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR,errmsg="生成短信验证码错误"))
        # 发送短信
        try:
            ccp.sendTemplateSMS(mobile,[sms_code,constants.SMS_CODE_EXPIRES_SECONDS],1)
        except Exception as e:
            logging.error(e)
        self.write(dict(errno=RET.OK,errmsg="OK"))


