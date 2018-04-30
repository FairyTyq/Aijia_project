# -*- coding:utf-8 -*-

import logging

from BaseHandler import BaseHandler
from utils.image_storage import storage
from utils.common import require_logined
from models import UserProfile
from utils.response_code import RET
from config import image_url_prefix 


class ProfileHandler(BaseHandler):
    ''' '''
    @require_logined
    def get(self):
        # 根据session中的手机号在mysql中读取用户数据
        try:
            usr = self.session_sql.query(UserProfile).filter(UserProfile.up_mobile==self.session.data['mobile']).first()
        except Exception as e:
            logging(e)
            return self.write({'errno':RET.DBERR,'errmsg':'db error'})

        name = usr.up_name
        mobile = usr.up_mobile
        img_name = usr.up_avatar
        
        avatar = image_url_prefix+img_name
        self.write(dict(errno=RET.OK,errmsg='OK',data={'name':name,'avatar':avatar,'mobile':mobile}))

            

class AvatarHandler(BaseHandler):
    '''上传头像 '''
    @require_logined
    def post(self):
        # 读取图片文件数据
        try:
            image_data= self.request.files['avatar'][0]['body']
        except Exception as e:
            # 参数出错
            logging.error(e)
            return self.write(dict(errno=RET.PARAMERR,essmsg='参数错误'))
        # 将图片存储到七牛
        try:
            image_name = storage(image_data)
        except Exception as e:
            logging.error(e)
            image_name = None
        # storage函数会返回七牛存储器中自动生成的文件名,若为空则存储出错
        if not image_name:
            return self.write({'errno':RET.THIRDERR,'errmsg':'qiniu error'})
        try:
            # 将头像文件名存入mysql数据库
            usr = self.session_sql.query(UserProfile).filter(UserProfile.up_mobile==self.session.data['mobile']).first()
            usr.up_avatar = image_name
            self.session_sql.commit()
        except Exception as e:
            logging.error(e)
            return self.write({'errno':RET.DBERR,'errmsg':'upload failed'}) 
        # 加上外链域名组合成完整url
        img_url = image_url_prefix+image_name
        # 返回数据给ajax
        return self.write({'errno':RET.OK,'errmsg':'OK','url':img_url})


class NicknameHandler(BaseHandler):
    '''修改昵称'''
    @require_logined
    def post(self):
        # 从解析过的json数据中获取用户提交的新昵称
        nick_name = self.json_args.get('name')
        print(nick_name)
        # 根据session中的手机号获取用户信息，并更新昵称
        try:
            usr = self.session_sql.query(UserProfile).filter(UserProfile.up_mobile==self.session.data['mobile']).first()
            usr.up_name = nick_name
            self.session_sql.commit()
        except Exception as e:
            logging.error(e)
            return self.write({'errno':RET.DBERR,'errmsg':'upload failed'})
        # 更新成功，返回OK
        return self.write({'errno':RET.OK,'errmsg':'OK'})


class LogoutHandler(BaseHandler):
    '''登出'''
    @require_logined
    def get(self):
        try:
            self.session.clear()
        except Exception as e:
            logging.error(e)
        return self.write({'errno':RET.OK,'errmsg':'OK'})


class AuthHandler(BaseHandler):
    '''实名认证'''
    @require_logined
    def get(self):
        try:
            usr = self.session_sql.query(UserProfile).filter(UserProfile.up_mobile==self.session.data.get('mobile')).first() 
        except Exception as e:
            logging.error(e)
            return self.write({'errno':RET.DBERR,'errmsg':'dberr'})
        real_name = usr.up_real_name
        id_card = usr.up_id_card
        print '读取的身份信息————%s,%s'%(real_name,id_card)
        return self.write({'errno':RET.OK,'errmsg':'OK','data':{'real_name':real_name,'id_card':id_card}})
    
    @require_logined
    def post(self):
        real_name = self.json_args.get('real_name')
        id_card = self.json_args.get('id_card')
        
        try:
            usr = self.session_sql.query(UserProfile).filter(UserProfile.up_mobile==self.session.data.get('mobile')).first()
        except Exception as e:
            logging.error(e)
            return self.write({'errno':RET.DBERR,'errmsg':'dberr'})

        try:
            usr.up_real_name = real_name
            usr.up_id_card = id_card
            self.session_sql.commit()
        except Exception as e:
            logging.error(e)
            return self.write({'errno':RET.DBERR,'errmsg':'upload error'})
        return self.write({'errno':RET.OK,'errmsg':'OK'})





