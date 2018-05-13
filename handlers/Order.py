# coding:utf-8

import logging

from datetime import datetime
from BaseHandler import BaseHandler
from utils.response_code import RET
from utils.common import require_logined
from models import OrderInfo,HouseInfo
from sqlalchemy import and_,or_
from config import image_url_prefix

class OrderHandler(BaseHandler):
    """ 订单预定处理类  """
    @require_logined
    def post(self):
        # 1.接收参数
        house_id = self.json_args.get('house_id')
        start_date = self.json_args.get('start_date')
        end_date = self.json_args.get('end_date') 
        # 2.参数校验
        s_date = datetime.strptime(start_date,"%Y-%m-%d")
        e_date = datetime.strptime(end_date,"%Y-%m-%d")
        # 3.查询数据
        # 查询房屋信息
        try:
            house = self.session_sql.query(HouseInfo).filter(HouseInfo.hi_house_id==house_id).first()
        except Exception as e:
            logging.error(e)
            return self.write({"errno":RET.DBERR,"errmsg":"get house info error"})
        # 查询客户提交的时间段内，该房间是否已有订单
        try:
            h_order = self.session_sql.query(OrderInfo).filter(and_(OrderInfo.oi_house_id==house_id,OrderInfo.oi_begin_date<=e_date,OrderInfo.oi_end_date>=s_date)).first()
        except Exception as e:
            logging.error(e)
            return self.write({"errno":RET.DBERR,"errmsg":"database query error!"})
        # 4.数据处理
        if h_order:
            return self.write({"errno":RET.DATAERR,"errmsg":"房间已经被预定"})
        else:
            order_obj = OrderInfo(
                    oi_user_id = self.session.data.get('id'),
                    oi_house_id = house_id,
                    oi_begin_date = s_date,
                    oi_end_date = e_date,
                    oi_days = (e_date-s_date).days+1,
                    oi_house_price = house.hi_price*100,
                    oi_amount = ((e_date-s_date).days+1)*house.hi_price*100,
                    oi_status = 0,
                    oi_comment = ""
                    )
            self.session_sql.add(order_obj)
            try:
                self.session_sql.commit()
            except Exception as e:
                logging.error(e)
                return self.write({"errno":RET.DBERR,"errmsg":"data upload error"})
        # 5.返回结果
            return self.write({"errno":RET.OK,"errmsg":"OK"})



class MyOrderHandler(BaseHandler):
    """ 我的订单 """
    @require_logined
    def get(self):
        # 1.获取参数
        role = self.get_argument('role')
        print "ROLE:%s"%role
        # 2.参数校验
        
        # 3.数据查询
        orders = self.session_sql.query(OrderInfo).filter(OrderInfo.oi_user_id==self.session.data.get('id')).all()
        order_list = []
        for i in orders:
            tmp = {
                "order_id":i.oi_order_id,
                "status":i.oi_status,
                "img_url":image_url_prefix+i.house.hi_index_image_url,
                "title":i.house.hi_title,
                "ctime":i.oi_ctime.strftime('%Y-%m-%d'),
                "start_date":i.oi_begin_date.strftime('%Y-%m-%d'),
                "end_date":i.oi_end_date.strftime('%Y-%m-%d'),
                "amount":i.oi_amount,
                "days":i.oi_days,
                "comment":[]
            }
            order_list.append(tmp)
        # 4.数据处理
        # 5.结果返回
        return self.write({"errno":RET.OK,"errmsg":"OK","orders":order_list})















