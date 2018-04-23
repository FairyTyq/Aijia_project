# coding:utf-8

def auth(fun):
    def wrapper(self,*args,**kwargs):
        if self.get_current_user():
            print "已登录"
            return fun(self,*args,**kwargs)
        else:
            print "未登录"
    return wrapper


