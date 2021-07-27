# -*- coding: utf-8 -*-
# @Time    : 2021/7/2 15:33
# @Author  : Haijun
import re

from conf.settings import load_or_create_settings
from apps.aliexpress.goods_detail import ProductsSpider
from apps.aliexpress.shop import ShopProducts
from apps.aliexpress.ae_login import LoginAli

load_or_create_settings('')

