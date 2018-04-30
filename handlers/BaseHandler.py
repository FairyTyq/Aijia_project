# coding:utf-8

import json
import tornado.web

from tornado.web import RequestHandler
from utils.session import Session
from sqlalchemy.orm import sessionmaker
from models import engine

class BaseHandler(RequestHandler):
    """handler 基类"""
    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis
    
    def prepare(self):
        # xsrf验证
        self.xsrf_token
        # 数据是json类型则进行处理
        if self.request.headers.get("Content-Type","").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None

        # 连接数据库
        self.Session_sql = sessionmaker(bind=engine)
        self.session_sql = self.Session_sql()


    def write_error(self,status_code,**kwargs):
        pass

    def set_default_headers(self):
        self.set_header("Content-Type","application/json;charset=UTF-8")

    def initialize(self):
        pass

    def on_finish(self):
        #pass
        # 关闭数据库
        self.session_sql.close()

    def get_current_user(self):
        self.session = Session(self)
        return self.session.data

class StaticFileHandler(tornado.web.StaticFileHandler):
    """ """
    def __init__(self,*args,**kwargs):
        super(StaticFileHandler,self).__init__(*args,**kwargs)
        self.xsrf_token

