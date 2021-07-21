# -*- coding: utf-8 -*-
# @Time    : 2020/8/24 14:37
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


# async def run_goods_info():
#
#     url = redis_conn.lpop('aliexpress_url')
#     if url:
#         logger.info(f'获取redis url=========={url}')
#         try:
#             _url = url.decode('utf-8')
#             if 'https:' not in _url and '//www' in _url:
#                 _url = f'https:{_url}'
#             crawler(_url)
#         except Exception as e:
#             logger.error(f'采集aliexpress商品失败=={url}==={e}')


# async def run_reviews():
#
#     ae_reviews_id = redis_conn.lpop('ae_reviews_id')
#     if ae_reviews_id:
#         d = json.loads(ae_reviews_id)
#         product_id = d.get('product_id')
#         owner_member_id = d.get('owner_member_id')
#         r = Reviews(product_id, owner_member_id)
#         reviews = r.crawl_reviews()
#         if reviews:
#             data = {
#                 'productId': product_id,
#                 'ownerMemberId': owner_member_id,
#                 'orderReviews': reviews
#             }
#             redis_conn.lpush('aliexpress_reviews', json.dumps(data))
#             logger.info(f'采集评论成功==={data}')


# def run_aliexpress():
#     coroutine1 = run_goods_info()
#     coroutine2 = run_reviews()
#     tasks = [
#         asyncio.ensure_future(coroutine1),
#         asyncio.ensure_future(coroutine2),
#     ]
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(asyncio.wait(tasks))
# if __name__ == '__main__':
#     while True:
#         loop = asyncio.get_event_loop()
#         tasks = [asyncio.ensure_future(run_goods_info()) for i in range(10)]
#         loop.run_until_complete(asyncio.wait(tasks))


def run_goods_info():
    url = redis_conn.lpop('aliexpress_url')
    if url:
        # logger.info(f'获取redis url=========={url}')
        try:
            _url = url.decode('utf-8')
            if 'https:' not in _url and '//www' in _url:
                _url = f'https:{_url}'
            crawler(_url)
        except Exception as e:
            logger.error(f'采集aliexpress商品失败=={url}==={e}')
#
#
# def run_reviews():
#     ae_reviews_id = redis_conn.lpop('ae_reviews_id')
#     if ae_reviews_id:
#         d = json.loads(ae_reviews_id)
#         product_id = d.get('product_id')
#         owner_member_id = d.get('owner_member_id')
#         r = Reviews(product_id, owner_member_id)
#         reviews = r.crawl_reviews()
#         if reviews:
#             data = {
#                 'productId': product_id,
#                 'ownerMemberId': owner_member_id,
#                 'orderReviews': reviews
#             }
#             redis_conn.lpush('aliexpress_reviews', json.dumps(data))
#             logger.info(f'采集评论成功==={ae_reviews_id}')
#
#
if __name__ == '__main__':
    while True:
        t_list = []
        for i in range(30):
            t1 = threading.Thread(target=run_goods_info, args=())
            # t2 = threading.Thread(target=run_goods_info, args=())
            t1.start()
            # t2.start()
            t_list.append(t1)
            # t_list.append(t2)
        for t in t_list:
            t.join()
        # crawler('https://www.aliexpress.com/item/1005001798022744.html')
