# -*-coding=utf-8 -*-

import logging
import json

from .BaseHandler import BaseHandler
from utils.common import require_logined
from utils.response_code import RET
from models import AreaInfo,HouseInfo,HouseFacility,House_image
from constants import AREA_INFO_REDIS_EXPIRES_SECONDS
from utils.image_storage import storage
from config import image_url_prefix

class AreaInfoHandler(BaseHandler):
    '''区域信息'''
    def get(self):
        # 先尝试从redis中获取区域信息
        try:
            redis_area_info = self.redis.get('BeiJing_areas')
        except Exception as e:
            logging.error(e)
            redis_area_info = ''
        if redis_area_info:
            logging.info('get data from redis')
            return self.write('{"errno":%s,"errmsg":"OK","data":%s}'%(RET.OK,redis_area_info))
        # redis中没找到区域信息，去mysql数据库中提取
        try:
            area_infos = self.session_sql.query(AreaInfo).all()
        except Exception as e:
            logging.error(e)
            return self.write({'errno':RET.DBERR,'errmsg':'database get error'})
        area_list = []
        for info in area_infos:
            area_list.append({"area_id":info.ai_area_id,"name":info.ai_name})
        
        # 将从mysql中提取到的信息存到redis中，一遍下一次借口被调用时可以从redis中直接获取到
        try:
            self.redis.setex('BeiJing_areas',AREA_INFO_REDIS_EXPIRES_SECONDS,json.dumps(area_list))
        except Exception as e:
            logging.error(e)
        return self.write({'errno':RET.OK,'errmsg':'OK','data':area_list})    


class HouseInfoHandler(BaseHandler):
    '''房屋信息发布 '''
    @require_logined
    def post(self):
        info = self.json_args
        house_info = HouseInfo(
                hi_user_id = self.session.data.get('id'),
                hi_title = info.get('title'),
                hi_price = info.get('price'),
                hi_area_id = info.get('area_id'),
                hi_address = info.get('address'),
                hi_room_count = info.get('room_count'),
                hi_acreage = info.get('acreage'),
                hi_house_unit = info.get('unit'),
                hi_capacity = info.get('capacity'),
                hi_beds = info.get('beds'),
                hi_deposit = info.get('deposit'),
                hi_min_days = info.get('min_days'),
                hi_max_days = info.get('max_days')
                )
        self.session_sql.add(house_info)
        self.session_sql.commit()
        for f in info.get('facility'):
            faci_tmp = HouseFacility(
                hf_house_id = house_info.hi_house_id,
                hf_facility_id = f
                )
            self.session_sql.add(faci_tmp)
        try:
            self.session_sql.commit()
        except Exception as e:
            logging.error(e)
            return self.write({'errno':RET.DBERR,'errmsg':'db storage error'})
        return self.write({'errno':RET.OK,'errmsg':'OK'})
            

class HouseImgHandler(BaseHandler):
    @require_logined
    def post(self):
        try:
            img_data = self.request.files['house_image'][0]['body']
            #house_id = self.json_args.get('house_id')
            house_id = self.request.files['house_id']
            print'HOUSE_ID%s'%house_id
        except Exception as e:
            logging.error(e)
            return self.write({'errno':RET.PARAMERR,'errmsg':'参数错误'})
        # 上传文件到七牛
#        try:
#            img_name = storage(img_data)
#        except Exception as e:
#            logging.error(e)
#            img_name = None
#        if not img_name:
#            return self.write({'errno':RET.THIRDERR,'errmsg':'qiniu error'})
        
        #try:
        #   img_tmp = House_image(hi_house_id=,hi_url=img_name) 

        














