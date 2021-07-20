# -*- coding: utf-8 -*-
# @Time    : 2021/7/15 0:22
# @Author  : Haijun

import requests
import json

from parsel import Selector


def goods_list():
    '''
    wish url:https://www.wish.com/c/5c24229a62d5c42244032782
    :return:
    '''
    url = 'https://haiyingshuju.com/wish_2.0/product/list'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }
    for i in range(30, 31):  # 26页
        print(i)
        data = {"index": i, "pageSize": 200, "orderColumn": "max_num_bought", "sort": "DESC", "pid": "", "pname": "",
                "cids": [], "ratingStart": "", "ratingEnd": "", "totalpriceStart": "", "totalpriceEnd": "",
                "genTimeStart": "", "genTimeEnd": "", "maxNumBoughtStart": "", "maxNumBoughtEnd": "",
                "viewRate1Start": "",
                "viewRate1End": "", "intervalRatingStart": "", "intervalRatingEnd": "", "pb": "", "verified": "",
                "hwc": "",
                "pnameStatus": 1, "pidStatus": 1, "merchantStatus": 1, "dailySalesAccuracyStart": "",
                "dailySalesAccuracyEnd": "", "totalSalesArrivalDateStart": "", "totalSalesArrivalDateEnd": "",
                "numRatingStart": "", "numRatingEnd": "", "selfShop": "", "oPriceStart": "", "oPriceEnd": "",
                "token": ""}
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        yield response.text


def parser_data():
    datas = goods_list()
    for data in datas:
        data_dict = json.loads(data)
        code = data_dict.get('code', None)
        if code == 1:
            data_list = data_dict.get('data', None)
            pids = [d.get('pid', None) for d in data_list]
            print(pids)


if __name__ == '__main__':
    parser_data()
