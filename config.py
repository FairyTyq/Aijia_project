# coding:utf-8

import os

# Application 配置参数
settings = {
    "static_path":os.path.join(os.path.dirname(__file__),"static"),
    "template_path":os.path.join(os.path.dirname(__file__),"template"),
    "cookie_secret":"fdagfagnjnavjnvfiaf",
    "xsrf_cookies":False,    
    "debug":True,
}

# myql
mysql_options = dict(
    host = "127.0.0.1",
    database = "ihome",
    user = "root",
    password = "123qwe"
        
)

# redis
redis_options = dict(
    host = "127.0.0.1",
    port = 6379
)

# 日志
log_file = os.path.join(os.path.dirname(__file__),"logs/log")
log_level = "debug"

# session数据有效期  单位：秒
session_expires = 86400

