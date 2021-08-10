# -*- coding: utf-8 -*-
# @Time    : 2021/7/15 0:22
# @Author  : Haijun

import json
import redis

from lib.base_fun import request_post, logger, proxy
from dynaconf import settings


class HaiyingList(object):
    def __init__(self):
        self.url = 'https://haiyingshuju.com/wish_2.0/product/list'
        self.redis_conn = redis.StrictRedis(host=settings.REDIS.HOST, port=settings.REDIS.PORT, db=settings.REDIS.DB,
                                            password=settings.REDIS.PASSWD)
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        }

    def get_response(self):
        '''
        wish url:https://www.wish.com/c/5c24229a62d5c42244032782
        :return:
        '''
        for i in range(1, 2):  # 26页
            data = {
                "index": i,
                "pageSize": 200,
                "orderColumn": "max_num_bought",
                "sort": "DESC",
                # "pid": "",
                # "pname": "",
                # "cids": [],
                # "ratingStart": "",
                # "ratingEnd": "",
                # "totalpriceStart": "",
                # "totalpriceEnd": "",
                # "genTimeStart": "",
                # "genTimeEnd": "",
                # "maxNumBoughtStart": "",
                # "maxNumBoughtEnd": "",
                # "viewRate1Start": "",
                # "viewRate1End": "",
                # "intervalRatingStart": "",
                # "intervalRatingEnd": "",
                # "pb": "",
                # "verified": "",
                # "hwc": "",
                # "pnameStatus": 1,
                # "pidStatus": 1,
                # "merchantStatus": 1,
                # "dailySalesAccuracyStart": "",
                # "dailySalesAccuracyEnd": "",
                # "totalSalesArrivalDateStart": "",
                # "totalSalesArrivalDateEnd": "",
                # "numRatingStart": "",
                # "numRatingEnd": "",
                # "selfShop": "",
                # "oPriceStart": "",
                # "oPriceEnd": "",
                # "token": ""
            }
            # status, response = request_post(url=self.url, headers=self.headers, data=json.dumps(data),
            #                                 proxy=proxy(settings.PROXY_USER2, settings.PROXY_PWD2))
            status, response = request_post(url=self.url, headers=self.headers, data=json.dumps(data))
            if status == 200:
                yield response.text

    def parser_data(self):
        datas = self.get_response()
        for data in datas:
            data_dict = json.loads(data)
            code = data_dict.get('code', None)
            if code == 1:
                data_list = data_dict.get('data', None)
                p_ids = [d.get('pid', None) for d in data_list]
                for p_id in p_ids:
                    yield p_id


if __name__ == '__main__':
    HaiyingList().parser_data()
