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
                price_list = []
                properties_size = {
                    'id': 'size',
                    'name': 'Size',
                    'orginalName': 'Size',
                    'value': list()
                }
                properties_color = {
                    'id': 'color',
                    'name': 'Color',
                    'orginalName': 'Color',
                    'value': list()
                }
                for sku in data:
                    sku_dict = dict()
                    size = sku.get('size')
                    if size:
                        sku_dict['size'] = size
                        properties_size['value'].append(size)
                    color = sku.get('color')
                    if color:
                        sku_dict['color'] = color
                        properties_color['value'].append(color)
                    price = sku.get('price')
                    sku_dict['goodsId'] = sku.get('pid')
                    sku_dict['skuId'] = sku.get('sid')
                    sku_dict['costPrice'] = price
                    sku_dict['price'] = price
                    sku_dict['marketPrice'] = price
                    sku_dict['orginalMarketPrice'] = price
                    sku_dict['stock'] = 0
                    sku_dict['skuPropIds'] = f"size:color"
                    sku_dict['skuAttr'] = f"size:{size.replace(' ', '').lower()};color:{color.replace(' ', '').lower()}"
                    sku_list.append(sku_dict)
                    price_list.append(float(price))
                print(price_list)
                if properties_size['value']:
                    val_list = list()
                    vals = list(set(properties_size['value']))
                    for val in vals:
                        val_dict = {
                            'id': val.replace(' ', '').lower(),
                            "imgId": None,
                            "imgUrl": None,
                            "mainUrl": None,
                            "value": val,
                            "orginalValue": val
                        }
                        val_list.append(val_dict)
                    properties_size['value'] = val_list
                    properties.append(properties_size)
                if properties_color['value']:
                    val_list = list()
                    vals = list(set(properties_color['value']))
                    for val in vals:
                        val_dict = {
                            'id': val.replace(' ', '').lower(),
                            "imgId": None,
                            "imgUrl": None,
                            "mainUrl": None,
                            "value": val,
                            "orginalValue": val
                        }
                        val_list.append(val_dict)
                    properties_color['value'] = val_list
                    properties.append(properties_color)
                data = {
                    'properties': properties,
                    'skuList': sku_list
                }
                return data, price_list
