# coding:utf-8
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer
from sqlalchemy import DateTime
from sqlalchemy import VARCHAR,BIGINT,CHAR,Boolean
from datetime import datetime

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
engine = create_engine('mysql+mysqldb://root:123qwe@localhost:3306/ihome?charset=utf8')

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = 'ih_user_profile'
    up_user_id = Column(Integer,primary_key=True,autoincrement=True,nullable=False,comment="用户ID")
    up_name = Column(VARCHAR(32),nullable=False,unique=True,comment="昵称")
    up_mobile = Column(CHAR(11),nullable=False,unique=True,comment="手机号")
    up_passwd = Column(VARCHAR(64),nullable=False,comment="密码")
    up_real_name = Column(VARCHAR(32),nullable=True,comment="真实姓名")
    up_id_card = Column(VARCHAR(20),nullable=True,comment="身份证号")
    up_admin = Column(Boolean,nullable=False,default=False,comment="是否为管理员")
    up_utime = Column(DateTime,nullable=False,default=datetime.now(),comment="最后更新时间")
    up_ctime = Column(DateTime,nullable=False,default=datetime.now(),comment="创建时间")



if __name__ == '__main__':
    Base.metadata.create_all(engine)

