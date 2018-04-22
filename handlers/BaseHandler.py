# coding:utf-8

import json

from tornado.web import RequestHandler

class BaseHandler(RequestHandler):
    """handler 基类"""
    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis
    
    def prepare(self):
        self.xsrf_token
        if self.request.headers.get("Content-Type","").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None

    def write_error(self,status_code,**kwargs):
        pass

    def set_default_headers(self):
        self.set_header("Content-Type","application/json;charset=UTF-8")

    def initialize(self):
        pass

    def on_finish(self):
        pass



