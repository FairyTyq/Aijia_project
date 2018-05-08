# coding:utf-8

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import config
import torndb
import redis

from tornado.options import define,options
from urls import handlers

define("port",type=int,default=8000,help="run server on the given port")

# 注入数据库
class Application(tornado.web.Application):
    """ """
    def __init__(self,*args,**kwargs):
        super(Application,self).__init__(*args,**kwargs)
        # 连接mysql数据库
#        self.db = torndb.Connection(
#            host = config.mysql_options['host'],
#            database = config.mysql_options['database'],
#            user = config.mysql_options['user'],
#            password = config.mysql_options['password']       
#        )
        self.db = torndb.Connection(**config.mysql_options)
        
        # 连接redis数据库
#        self.redis = redis.StrictRedis(
#            host = config.redis_options['host'],
#            port = config.redis_options['port']
#        )
        self.redis = redis.StrictRedis(**config.redis_options)

def main():
    options.log_file_prefix = config.log_file
    options.logging = config.log_level
    tornado.options.parse_command_line()
    app = Application(
        handlers,**config.settings
        )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port,'192.168.213.128')

    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()

