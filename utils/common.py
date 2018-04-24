# coding=utf-8

# functools下的wraps装饰器可以保证 自己定义的装饰器不改变被装饰函数的__name__属性
import functools

from utils.response_code import RET

def require_logined(fun):
    @functools.wraps(fun)
    def wrapper(request_handler_obj,*args,**kwargs):
        # 根据get_current_user方法进行判断，如果返回的不是一个空字典，证明用户已经登陆过，该用户的session数据已经保存
        if not request_handler_obj.get_current_user():
            fun(request_handler_obj,*args,**kwargs)
        # 返回的是空字典，代表用户未登录过，没有保存用户的session数据
        else:
            request_handler_obj.write(dict(errno=RET.SESSIONERR,errmsg="用户未登录"))
    return wrapper

