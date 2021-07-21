# -*- coding: utf-8 -*-
# @Time    : 2021/7/21 17:42
# @Author  : Haijun
import json

from apps.haiying_wish.wish.wish import Wish
from apps.haiying_wish.haiying.haiying_wish_sku import HaiyingWishSku
from apps.haiying_wish.haiying.goods_id import HaiyingList


def get_full_info():
    p_ids = HaiyingList().parser_data()
    for p_id in p_ids:
        data = {
            'code': False,
            'item': None
        }

        sku_info = HaiyingWishSku().parser_data(p_id)
        property = sku_info['properties']
        sku_list = sku_info['skuList']
        goods_info = Wish().crawl_wish(p_id)
        if goods_info and sku_info:
            goods_info['properties'] = property
            goods_info['skuList'] = sku_list
            data['code'] = False
            data['data'] = goods_info
            print(json.dumps(data, ensure_ascii=False))
