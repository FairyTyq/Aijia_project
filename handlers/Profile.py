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
        try:
            name = self.session_sql.query(UserProfile.up_name).filter(UserProfile.up_mobile==self.session.data['mobile']).first()[0] 
        except Exception as e:
            logging(e)
        if name == None:
            name = 'erroname'
        
        try:
            img_name = self.session_sql.query(UserProfile.up_avatar).filter(UserProfile.up_mobile==self.session.data['mobile']).first()[0]
        except Exception as e:
            logging(e)
        if img_name == None:
            img_name = ''
            
        avatar = image_url_prefix+img_name
        return self.write(dict(errno=RET.OK,errmsg='OK',data={'name':name,'avatar':avatar}))

            

class AvatarHandler(BaseHandler):
    '''上传头像 '''
    @require_logined
    def post(self):
        try:
            image_data= self.request.files['avatar'][0]['body']
        except Exception as e:
            # 参数出错
            logging.error(e)
            return self.write(dict(errno=RET.PARAMERR,essmsg='参数错误'))
        try:
            image_name = storage(image_data)
        except Exception as e:
            logging.error(e)
            image_name = None
        if not image_name:
            return self.write({'errno':RET.THIRDERR,'errmsg':'qiniu error'})
        try:
            # 存入数据库
            usr = self.session_sql.query(UserProfile).filter(UserProfile.up_mobile==self.session.data['mobile']).first()
            print 'test print mobile:%s'%usr.up_mobile
            usr.up_avatar = image_name
            self.session_sql.commit()
        except Exception as e:
            logging.error(e)
            return self.write({'errono':RET.DBERR,'errmsg':'upload failed'})
        
        img_url = image_url_prefix+image_name
        return self.write({'errno':RET.OK,'errmsg':'OK','url':img_url})

