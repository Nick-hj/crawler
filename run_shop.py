# -*- coding: utf-8 -*-
# @Time    : 2021/7/23 19:25
# @Author  : Haijun

import json
import re
import time
import os
import redis
from dynaconf import settings
from lib.base_fun import logger, run_thread
from apps.aliexpress.ae_web_shop import LoginAli

redis_conn = redis.StrictRedis(host=settings.REDIS.HOST, port=settings.REDIS.PORT, db=settings.REDIS.DB,
                               password=settings.REDIS.PASSWD)


def goods_url_via_shop():
    shop_url = redis_conn.lpop('aliexpress_shop')
    if shop_url:
        shop = LoginAli()
        shop.run_login(shop_url.decode('utf-8'))


if __name__ == '__main__':
    while True:
        length = redis_conn.llen('aliexpress_shop')
        if length != 0:
            goods_url_via_shop()
            time.sleep(30)
            os.system('ps -ef | grep chrome-linux/chrome|grep -v grep | cut -c 9-15 | xargs kill -9')
        else:
            time.sleep(10)
