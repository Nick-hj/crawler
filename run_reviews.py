# -*- coding: utf-8 -*-
# @Time    : 2021/7/21 21:57
# @Author  : Haijun

import json
import random

import redis
from dynaconf import settings
from lib.base_fun import logger
from apps.aliexpress.reviews import Reviews
from lib.base_fun import run_thread

redis_conn = redis.StrictRedis(host=settings.REDIS.HOST, port=settings.REDIS.PORT, db=settings.REDIS.DB,
                               password=settings.REDIS.PASSWD)


def run_reviews():
    ae_reviews_id = redis_conn.lpop('ae_reviews_id')
    if ae_reviews_id:
        d = json.loads(ae_reviews_id)
        product_name = d.get('product_name', None)
        product_id = d.get('product_id', None)
        owner_member_id = d.get('owner_member_id', None)
        r = Reviews(product_id, owner_member_id,product_name)
        reviews = r.review_results()
        if reviews:
            trade_count = random.randint(5, 10)
            data = {
                'productId': product_id,
                'productName': product_name,
                'ownerMemberId': owner_member_id,
                'tradeCount': trade_count * len(reviews),
                'orderReviews': reviews
            }
            redis_conn.lpush('aliexpress_reviews', json.dumps(data))
            logger.info(f'采集评论成功==={ae_reviews_id}')


if __name__ == '__main__':
    run_thread('ae_reviews_id', 100, run_reviews, 10)
