# -*-coding=utf-8 -*-

import logging
import json

from .BaseHandler import BaseHandler
from utils.common import require_logined
from utils.response_code import RET
from models import AreaInfo,HouseInfo,HouseFacility,House_image,UserProfile
from constants import AREA_INFO_REDIS_EXPIRES_SECONDS,MYHOUSES_INFO_REDIS_EXPIRES_SECONDS
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
        self.redis.delete('My_houses')
        return self.write({'errno':RET.OK,'errmsg':'OK','house_id':house_info.hi_house_id})

    @require_logined
    def get(self):
        '''房屋信息detail页面'''
        house_id = self.get_argument('house_id')
        print 'HOUSE ID:%s'%house_id
        # 查询房屋信息 
        try:
            house = self.session_sql.query(HouseInfo).filter(HouseInfo.hi_house_id==house_id).first()
        except Exception as e:
            logging.error(e)
            return self.write({'errno':RET.DBERR,'errmsg':'failed get data from darabase'})
        # 查询房东信息
        try:
            owner = self.session_sql.query(UserProfile).filter(UserProfile.up_user_id==house.hi_user_id).first()
        except Exception as e:
            logging.error(e)
        
        # 查询房屋设施
        try:
            facility = self.session_sql.query(HouseFacility).filter(HouseFacility.hf_house_id==house_id).all()
        except Exception as e:
            logging.error(e)
        facilities = []
        if facility:
            for f in facility:
                facilities.append(f.hf_facility_id)
        # 查询房屋图片
        try:
            house_imgs = self.session_sql.query(House_image).filter(House_image.hi_house_id==house_id).all()
        except Exception as e:
            logging.error(e)
        imgs_list = []
        if house_imgs:
            for house_img in house_imgs:
                imgs_list.append(image_url_prefix+house_img.hi_url)
            print "**--HOUSE IMGS--**:%s"%imgs_list
        
        data ={
                "hid":house_id,
                "images":imgs_list,
                "price":house.hi_price*100,
                "user_id":house.hi_user_id,
                "user_avatar":image_url_prefix+owner.up_avatar,
                "title":house.hi_title,
                "user_name":owner.up_name,
                "address":house.hi_address,
                "room_count":house.hi_room_count,
                "acreage":house.hi_acreage,
                "unit":house.hi_house_unit,
                "capacity":house.hi_capacity,
                "beds":house.hi_beds,
                "deposit":house.hi_deposit,
                "min_days":house.hi_min_days,
                "max_days":house.hi_max_days,
                "facilities":facilities,
                "comments":[]
            }
        self.write({"errno":RET.OK,"errmsg":"OK","data":data,"user_id":self.session.data.get('id')})




class HouseImgHandler(BaseHandler):
    '''房屋图片 '''
    @require_logined
    def post(self):
        img_data = self.request.files['house_image'][0]['body']
        house_id = self.get_argument('house_id')
        print'HOUSE_ID%s'%house_id
        # 上传文件到七牛
        try:
            img_name = storage(img_data)
        except Exception as e:
            logging.error(e)
            img_name = None
        if not img_name:
            return self.write({'errno':RET.THIRDERR,'errmsg':'qiniu error'})
        
        try:
            img_tmp = House_image(hi_house_id=house_id,hi_url=img_name)
            self.session_sql.add(img_tmp)
            self.session_sql.commit()
        except Exception as e:
            logging.error(e)
            return self.write({'errno':RET.DBERR,'errmsg':'upload failed'})
        # 设置最新上传的图片为房源首页图片
        try:
            house_tmp = self.session_sql.query(HouseInfo).filter(HouseInfo.hi_house_id==house_id).first()
        except Exception as e:
            logging.error(e)
        house_tmp.hi_index_image_url = img_name
        self.session_sql.commit()
        url = image_url_prefix+img_name
        return self.write({'errno':RET.OK,'errmsg':'OK','url':url})
            

        
class MyHouseHandler(BaseHandler):
    '''用户房源'''
    @require_logined
    def get(self):
        # 尝试从redis中获取用户房屋信息
        try:
           houses_info_redis = self.redis.get("My_houses")
        except Exception as e:
            logging.error(e)
            houses_info_redis = ''
        if houses_info_redis:
            print "GET INFO FROM REDIS \n REDIS HOUSE INFO : %s"%houses_info_redis
            return self.write('{"errono":%s,"errmsg":"OK","houses":%s}'%(RET.OK,houses_info_redis))

        # 未从redis中读取到数据，根据用户id获取该用户名下所有的房子信息
        try:
            my_houses = self.session_sql.query(HouseInfo).filter(HouseInfo.hi_user_id==self.session.data['id']).all()
            print 'Users houses :%s'%my_houses
        except Exception as e:
            logging.error(e)
            return self.write({'errno':RET.DBERR,'errmsg':'database err'})
        # 遍历从mysql中查询到的结果，每个房源信息存储成一个字典，该用户的所有房源信息存储成一个列表返回个前端
        h_list = []
        if my_houses:
            for h in my_houses:
                # 获取房屋所在区域名称
                try:
                    a_name = self.session_sql.query(AreaInfo).filter(AreaInfo.ai_area_id == h.hi_area_id).first().ai_name
                except Exception as e:
                    logging.error(e)
                # 组合图片url
                image_name =h.hi_index_image_url,
                if image_name == (None,):
                    image_name = ''
                else:
                    image_name = image_name[0]
                print 'Image Name1:%s,Type1:%s'%(image_name,type(image_name))
                #print 'Image Name2:%s,Type2:%s'%(image_name[0],type(image_name))
                # 房源信息存入字典
                h_tmp = {
                        "house_id":h.hi_house_id,        
                        "img_url":image_url_prefix+image_name,
                        "area_name":a_name,
                        "ctime":h.hi_utime.strftime("%Y-%m-%d"),
                        "price":h.hi_price*100,
                        "title":h.hi_title
                    }
                # 将字典存入列表
                h_list.append(h_tmp)
            self.redis.setex("My_houses",MYHOUSES_INFO_REDIS_EXPIRES_SECONDS,json.dumps(h_list))
        return self.write({'errno':RET.OK,'errmsg':'OK','houses':h_list})












