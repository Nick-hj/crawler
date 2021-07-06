# -*- coding: utf-8 -*-
# @Time    : 2020/8/24 14:37
# @Author  : Haijun

import redis

from bin import crawler
from dynaconf import settings
from lib.base_fun import logger


def main():
    while True:
        redis_conn = redis.StrictRedis(host=settings.REDIS.HOST, port=settings.REDIS.PORT, db=settings.REDIS.DB,
                                       password=settings.REDIS.PASSWD)
        url = redis_conn.lpop('aliexpress_url')
        if url:
            try:
                crawler(url.encode('utf-8'))
            except Exception as e:
                logger.error(f'采集aliexpress商品失败=={url}==={e}')


if __name__ == '__main__':
    main()
