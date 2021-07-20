# -*- coding: utf-8 -*-
# @Time    : 2021/7/20 23:29
# @Author  : Haijun
import json

import redis

from dynaconf import settings
from lib.base_fun import request_post


class HaiyingWishSku(object):
    def __init__(self):
        self.url = 'https://haiyingshuju.com/wish_2.0/product/detail/sku'

        self.redis_conn = redis.StrictRedis(
            host=settings.REDIS.HOST,
            port=settings.REDIS.PORT,
            db=settings.REDIS.DB,
            password=settings.REDIS.PASSWD
        )
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_response(self, p_id):
        data = {
            "index": 1,
            "pageSize": 50,
            "pid": p_id,
            "orderColumn": "",
            "sort": ""
        }
        status, response = request_post(url=self.url, headers=self.headers, data=json.dumps(data))
        if status == 200:
            return response.text
        else:
            return None

    def parser_data(self, p_id):
        response_text = self.get_response(p_id)
        if response_text:
            result = json.loads(response_text)
            if result['code'] == 1:
                data = result['data']
                sku_list = list()
                properties = list()
                properties_size = {
                    'name': 'size',
                    'value': list()
                }
                properties_color = {
                    'name': 'color',
                    'value': list()
                }
                for sku in data:
                    sku_dict = dict()
                    size = sku.get('size')
                    if size:
                        properties_size['value'].append(size)
                    color = sku.get('color')
                    if color:
                        properties_color['value'].append(color)
                    sku_dict['pId'] = sku.get('pid')
                    sku_dict['skuId'] = sku.get('sid')
                    sku_dict['price'] = sku.get('price')
                    sku_list.append(sku_dict)
                if properties_size['value']:
                    properties_size['value'] = list(set(properties_size['value']))
                    properties.append(properties_size)
                if properties_color['value']:
                    properties_color['value'] = list(set(properties_color['value']))
                    properties.append(properties_color)
                data = {
                    'properties': properties,
                    'skuList': sku_list
                }
                print(data)
