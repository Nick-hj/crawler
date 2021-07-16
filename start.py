# -*- coding: utf-8 -*-
# @Time    : 2020/8/24 14:37
# @Author  : Haijun

import redis
import threading
from bin import crawler
from dynaconf import settings
from lib.base_fun import logger

redis_conn = redis.StrictRedis(host=settings.REDIS.HOST, port=settings.REDIS.PORT, db=settings.REDIS.DB,
                               password=settings.REDIS.PASSWD)


def main():
    while True:
        url = redis_conn.lpop('aliexpress_url')
        if url:
            logger.info(f'获取redis url=========={url}')
            try:
                _url = url.decode('utf-8')
                if 'https:' not in _url and '//www' in _url:
                    _url = f'https:{_url}'
                crawler(_url)
            except Exception as e:
                logger.error(f'采集aliexpress商品失败=={url}==={e}')


if __name__ == '__main__':
    t1 = threading.Thread(target=main(), args=())
    t2 = threading.Thread(target=main(), args=())
    t1.start()
    t2.start()
    t1.join()
    t2.join()
