# -*- coding: utf-8 -*-
# @Time    : 2021/8/5 16:28
# @Author  : Haijun

import redis
import pandas as pd

redis_conn = redis.StrictRedis(host='localhost', port=6379, db=4)
pf = pd.read_excel('./url.xlsx')
data = pf['url']
for d in data:
    redis_conn.lpush('aliexpress_url', d)
