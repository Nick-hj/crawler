# -*- coding: utf-8 -*-
# @Time    : 2021/7/18 16:09
# @Author  : Haijun

from apps.haiying_wish.wish.wish import Wish
from apps.haiying_wish.haiying.haiying_wish_sku import HaiyingWishSku
from apps.haiying_wish.haiying.goods_id import HaiyingList
from apps.haiying_wish.wish.login_wish import LoginWish
from apps.haiying_wish.full_goods_info import get_full_info
LoginWish().run_login()
# Wish().crawl_wish('5f5205da290c090b7a268f38')
# HaiyingList().parser_data()
# HaiyingWishSku().parser_data('5f5205da290c090b7a268f38')
# get_full_info()