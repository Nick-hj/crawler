# -*- coding: utf-8 -*-
# @Time    : 2021/7/31 16:08
# @Author  : Haijun

import asyncio
import datetime
import json
import random
import time
from lib.base_fun import logger
from aredis import StrictRedis
from aiomysql.sa import create_engine


class ReviewsToMyswl(object):

    def __init__(self):
        self.redis_conn = StrictRedis(host='localhost', port=6379, db=4)

    async def redis_goods(self, loop):
        data = await self.redis_conn.lpop('aliexpress_reviews')
        if data:
            await self.mysql_goods(loop, data)

    async def create_pool(self, loop):
        # 该函数用于创建连接池
        pool = await create_engine(
            # host='127.0.0.1',
            # db='aliexpress',
            # user='root',
            # password='root',
            host='172.31.0.155',
            db='voghion-comment',
            user='prod',
            password='Stars@2019',
            maxsize=10,  # 连接池最多同时处理10个请求
            minsize=1,  # 连接池最少1个请求
            loop=loop
        )
        return pool

    async def mysql_goods(self, loop, data):
        engine = await self.create_pool(loop)
        async with engine.acquire() as conn:
            data_dict = json.loads(data)
            product_id = data_dict['productId']
            product_name = data_dict['productName']
            trade_count = data_dict['tradeCount']
            goods_url = f'https://www.aliexpress.com/item/{product_id}.html'
            # cache_goods_id = await self.redis_conn.get(str(product_id))
            # if not cache_goods_id:
            select_g_sql = "select s.goods_id from `product-ua`.`goods_ext_detail` s where s.goods_url=%s"
            select_result = await conn.execute(select_g_sql, goods_url)
            if select_result.rowcount == 1:
                _goods_id = await select_result.fetchone()
                goods_id = _goods_id[0]
                logger.info(f'入库id====={goods_id},交易量: {trade_count}，商品id: {product_id}')
                select_r_sql = "select * from user_goods_comment u where u.goods_id=%s"
                select_r_result = await conn.execute(select_r_sql, goods_id)
                if select_r_result.rowcount == 0:
                    review = data_dict.get('orderReviews')
                    if review:
                        for t in review:
                            user_name = t.get('userName', None)
                            score = t.get('star', 0)
                            comment = t.get('contentsText', None)
                            img_url = ';'.join(t.get('imageList', None))
                            review_time = t.get('rTime', None)
                            props = self._prop(t.get('orderInfo', []))
                            tx = await conn.begin()
                            review_sql = """INSERT INTO `user_goods_comment`(`user_id`, `goods_id`, `goods_name`, `sku_id`, `sku_name`, `comment`, `score`, `img_url`, `order_id`, `status`, `sort`, `create_time`, `update_time`, `nick_name`, `head_img`,`order_info`) VALUES (NULL, %s, %s, 0, '', %s, %s, %s, '', 20, 0, %s, %s, %s, NULL,%s)"""
                            review_val = [goods_id, product_name, comment, score, img_url, review_time, review_time,
                                          user_name,
                                          props]
                            update_goods_sql = 'UPDATE `product-ua`.goods  set sales=%s where id =%s'
                            update_goods_val = [trade_count, goods_id]
                            await conn.execute(review_sql, review_val)
                            await conn.execute(update_goods_sql, update_goods_val)
                            await tx.commit()
                            # await self.redis_conn.set(str(product_id), product_id)
                            # await self.redis_conn.expire(str(product_id), 600)
                else:
                    await self.redis_conn.rpush('aliexpress_url', goods_url)
        engine.terminate()
        engine.close()
        await engine.wait_closed()

    @staticmethod
    def _c_time(r_time):
        if not r_time:
            year = '2021'
            month = random.choice(['06', '07'])
            if month == '06':
                day = random.randint(1, 30)
            else:
                day = random.randint(1, 31)
            if day < 10:
                day = f'0{str(day)}'
            h = random.randint(0, 23)
            if h < 10:
                h = f'0{str(h)}'
            m = random.randint(0, 59)
            if m < 10:
                m = f'0{str(m)}'
            s = random.randint(0, 59)
            if s < 10:
                s = f'0{str(s)}'
            f_time = f'{year}-{str(month)}-{str(day)} {str(h)}:{str(m)}:{str(s)}'
            r_time = datetime.datetime.strptime(f_time, '%Y-%m-%d %H:%M:%S')
        return r_time

    def _prop(self, data):
        if data:
            p = []
            for d in data:
                name = d.get('propName', '').replace(':', '')
                value = d.get('propValue', '')
                if name != 'Logistics':
                    p_v = f'{name}:{value}'
                    p.append(p_v)
            return ';'.join(p)

    def main(self):
        loop = asyncio.get_event_loop()
        # loop.run_until_complete(self.redis_goods(loop))
        tasks = [asyncio.ensure_future(self.redis_goods(loop)) for i in range(10)]
        loop.run_until_complete(asyncio.wait(tasks))
        return True


if __name__ == '__main__':
    while True:
        ReviewsToMyswl().main()
        time.sleep(1)
