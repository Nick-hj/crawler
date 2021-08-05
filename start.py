# -*- coding: utf-8 -*-
# @Time    : 2020/8/24 14:37
# @Author  : Haijun
import asyncio
import json
import re

import redis
from dynaconf import settings
from lib.base_fun import logger, run_thread
from apps.aliexpress.goods_detail import ProductsSpider

redis_conn = redis.StrictRedis(host=settings.REDIS.HOST, port=settings.REDIS.PORT, db=settings.REDIS.DB,
                               password=settings.REDIS.PASSWD)


def run_goods_info():
    url = redis_conn.lpop('aliexpress_url')
    if url:
        try:
            _url = url.decode('utf-8')
            if 'https:' not in _url and '//www' in _url:
                _url = f'https:{_url}'
            if '/item/' in _url:
                p = ProductsSpider(_url)
                p.goods_info()
            elif '/store/' in _url:
                full_url = re.search(r'/store/\d+/search/\d+.html',_url)
                if full_url:
                    shop_url = full_url
                else:
                    shop = re.search(r'/store/(\d+)', _url)
                    w_shop = re.search(r'(\d+)\.html', _url)
                    if shop:
                        shop_id = shop.group(1)
                    elif w_shop:
                        shop_id = w_shop.group(1)
                    else:
                        raise TypeError('请输入正确的店铺url')
                    # 拼接全店铺商品第一页
                    shop_url = f'https://www.aliexpress.com/store/{shop_id}/search/1.html'
                print(f'shop_url====={shop_url}')
                redis_conn.lpush('aliexpress_shop', shop_url)
        except Exception as e:
            # redis_conn.lpush('aliexpress_url', url)
            logger.error(f'采集aliexpress商品失败=={url}==={e}')


#
if __name__ == '__main__':
    run_thread('aliexpress_url', 2, run_goods_info, 15)

    # crawler('https://www.aliexpress.com/item/1005001798022744.html')
