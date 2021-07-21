# -*- coding: utf-8 -*-
# @Time    : 2021/7/21 21:57
# @Author  : Haijun
import asyncio
import json
import threading
import time

import redis
from bin import crawler
from dynaconf import settings
from lib.base_fun import logger
from apps.aliexpress.reviews import Reviews

redis_conn = redis.StrictRedis(host=settings.REDIS.HOST, port=settings.REDIS.PORT, db=settings.REDIS.DB,
                               password=settings.REDIS.PASSWD)

def run_reviews():

    ae_reviews_id = redis_conn.lpop('ae_reviews_id')
    if ae_reviews_id:
        d = json.loads(ae_reviews_id)
        product_id = d.get('product_id')
        owner_member_id = d.get('owner_member_id')
        r = Reviews(product_id, owner_member_id)
        reviews = r.crawl_reviews()
        if reviews:
            data = {
                'productId': product_id,
                'ownerMemberId': owner_member_id,
                'orderReviews': reviews
            }
            redis_conn.lpush('aliexpress_reviews', json.dumps(data))
            logger.info(f'采集评论成功==={ae_reviews_id}')

if __name__ == '__main__':
    while True:
        t_list = []
        for i in range(30):
            t1 = threading.Thread(target=run_reviews, args=())
            t1.start()
            t_list.append(t1)
        for t in t_list:
            t.join()