# -*- coding:utf-8 -*-

import logging

from .BaseHandler import BaseHadler
from ..utils.image_storage import storage
from ..utils.common import require_logined
from ..models import UserProfile,engine
from sqlalchemy import sessionmaker
from utils.response_code import import RET

@require_logined
class AvatarHandler(BaseHandler):
    '''上传头像 '''
    def post(self):
        try:
            image_data= self.request.files['avatar'][0]['body']
        except Exception as e:
            # 参数出错
            logging.error(e)
            return self.write('')
        try:
            # 存入数据库
            Session_sql = sessionmaker(bind=engine)
            session_sql = Session_sql()


        except Exception as e:

        return image_url

