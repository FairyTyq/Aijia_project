# coding:utf-8
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import Column,String,Integer,TIMESTAMP,SMALLINT
from sqlalchemy import DateTime,Date
from sqlalchemy import VARCHAR,BIGINT,TEXT,CHAR,Boolean
from datetime import datetime


if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
engine = create_engine('mysql+mysqldb://root:123qwe@localhost:3306/ihome?charset=utf8')

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = 'ih_user_profile'
    #__table_args__ = {'extend_existing': True} 
    up_user_id = Column(Integer,primary_key=True,autoincrement=True,nullable=False,comment="用户ID")
    up_name = Column(VARCHAR(32),nullable=False,unique=True,comment="昵称")
    up_mobile = Column(CHAR(11),nullable=False,unique=True,comment="手机号")
    up_passwd = Column(VARCHAR(64),nullable=False,comment="密码")
    up_real_name = Column(VARCHAR(32),nullable=True,comment="真实姓名")
    up_id_card = Column(VARCHAR(20),nullable=True,comment="身份证号")
    up_avatar = Column(VARCHAR(128),nullable=True,comment='用户头像')
    up_admin = Column(Boolean,nullable=False,default=False,comment="是否为管理员")
    up_utime = Column(DateTime,nullable=False,default=datetime.now(),comment="最后更新时间")
    up_ctime = Column(DateTime,nullable=False,default=datetime.now(),comment="创建时间")

class AreaInfo(Base):
    '''房源区域表 '''
    __tablename__ = 'ih_area_info'
    #__table_args__ = {'extend_existing': True} 
    ai_area_id = Column(Integer,primary_key=True,autoincrement=True,nullable=False,comment='区域id')
    ai_name = Column(VARCHAR(32),nullable=False,comment='区域名称')
    ai_ctime = Column(DateTime,nullable=False,default=datetime.now(),comment='创建时间')

class HouseInfo(Base):
    '''房屋信息表 '''
    __tablename__ = 'ih_house_info'
    hi_house_id = Column(Integer,primary_key=True,autoincrement=True,nullable=False,comment='房屋id')
    hi_user_id = Column(Integer,ForeignKey('ih_user_profile.up_user_id'),nullable=False,comment='用户id')
    hi_title = Column(VARCHAR(64),nullable=False,comment='房屋名称')
    hi_price = Column(Integer,nullable=False,comment='房屋价格')
    hi_area_id = Column(Integer,ForeignKey('ih_area_info.ai_area_id'),nullable=False,comment='房屋区域ID')
    hi_address = Column(VARCHAR(512),nullable=False,default='',comment='地址')
    hi_room_count = Column(SMALLINT,nullable=False,default=1,comment='房间数')
    hi_acreage = Column(Integer,nullable=False,default=0,comment='房屋面积')
    hi_house_unit = Column(VARCHAR(32),nullable=False,default='',comment='房屋户型')
    hi_capacity = Column(Integer,nullable=False,default=1,comment='容纳人数')
    hi_beds = Column(VARCHAR(64),nullable=False,default='',comment='床的配置')
    hi_deposit = Column(Integer,nullable=False,default=0,comment='押金')
    hi_min_days = Column(Integer,nullable=False,default=1,comment='最短入住时间')
    hi_max_days = Column(Integer,nullable=False,default=0,comment='最长入住时间，0-不限制')
    hi_order_count = Column(Integer,nullable=False,default=0,comment='下单数量')
    hi_verify_status = Column(SMALLINT,nullable=False,default=0,comment='审核状态,0-待审核，1-审核未通过，2-审核通过')
    hi_online_status = Column(SMALLINT,nullable=False,default=1,comment='0-下线，1-上线')
    hi_index_image_url = Column(VARCHAR(256),nullable=True,comment='房屋主图片')
    hi_utime = Column(DateTime,nullable=False,default=datetime.now(),comment='更新时间')

class HouseFacility(Base):
    ''' 房屋设施表 '''
    __tablename__='ih_house_facility'
    hf_id = Column(BIGINT,nullable=False,primary_key=True,autoincrement=True,comment='自增ID')
    hf_house_id = Column(Integer,ForeignKey('ih_house_info.hi_house_id'),nullable=False,comment='房屋ID')
    hf_facility_id = Column(Integer,nullable=False,comment='房屋设施')
    hf_ctime = Column(DateTime,nullable=False,default=datetime.now(),comment='创建时间')
   

class FacilityCatelog(Base):
    '''设施目录表 '''
    __tablename__='ih_facility_catelog'
    fc_id = Column(Integer,nullable=False,autoincrement=True,primary_key=True,comment='自增id')
    fc_name = Column(VARCHAR(32),nullable=False,comment='设施名称')
    fc_ctime = Column(DateTime,nullable=False,default=datetime.now(),comment='创建时间')


class OrderInfo(Base):
    '''订单表 ''' 
    __tablename__='ih_order_info'
    oi_order_id = Column(BIGINT,nullable=False,autoincrement=True,primary_key=True,comment='订单id')
    oi_user_id = Column(Integer,ForeignKey('ih_user_profile.up_user_id'),nullable=False,comment='用户ID')
    oi_house_id = Column(Integer,ForeignKey('ih_house_info.hi_house_id'),nullable=False,comment='房屋id')
    oi_begin_date = Column(Date,nullable=False,comment='入住时间')
    oi_end_date = Column(Date,nullable=False,comment='离开时间')
    oi_days = Column(Integer,nullable=False,comment='入住天数')
    oi_house_price = Column(Integer,nullable=False,comment='房屋单价，单位分')
    oi_amount = Column(Integer,nullable=False,comment='订单金额，单位分')
    oi_status = Column(SMALLINT,nullable=False,default=0,comment='订单状态，0-待接单，1-待支付，2-已支付，3-待评价，4-已完成，5-已取消，6-据接单')
    oi_comment = Column(TEXT,nullable=True,comment='订单评论')
    oi_utime = Column(DateTime,nullable=True,default=datetime.now(),comment='最后更新时间')
    oi_ctime = Column(DateTime,nullable=True,default=datetime.now(),comment='创建时间')


class House_image(Base):
    '''房屋图片表 '''
    __tablename__='ih_house_image'
    hi_image_id = Column(BIGINT,nullable=False,autoincrement=True,primary_key=True,comment='图片id')
    hi_house_id = Column(Integer,ForeignKey('ih_house_info.hi_house_id'),nullable=False,comment='房屋id')
    hi_url = Column(VARCHAR(256),nullable=False,comment='图片url')
    hi_ctime = Column(DateTime,nullable=False,default=datetime.now(),comment='创建时间')


if __name__ == '__main__':
    Base.metadata.create_all(engine)

