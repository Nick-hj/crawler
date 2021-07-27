# -*- coding: utf-8 -*-
# @Time    : 2021/6/29 15:24
# @Author  : Haijun
import http.client
import requests
import random
import re
import time
import redis
from parsel import Selector
from lib.base_fun import logger, proxy
from dynaconf import settings
from apps.aliexpress.ae_login import LoginAli
http.client._is_legal_header_name = re.compile(rb'[^\s][^:\r\n]*').fullmatch
class ShopProducts(object):
    def __init__(self):
        self.redis_conn = redis.StrictRedis(host=settings.REDIS.HOST, port=settings.REDIS.PORT, db=settings.REDIS.DB,
                                            password=settings.REDIS.PASSWD)
        self.session = requests.Session()
    def headers(self,path):
        # try:
        with open('./apps/aliexpress/cookie.txt','r') as f:
            _cookies = f.readlines()
            cookie = _cookies[0]
        print(cookie)
        headers = {
            # ':authority': 'www.aliexpress.com',
            # ':path': path,
            # 'accept-encoding': 'gzip,deflate,br',
            # ':method': 'GET',
            # 'cache-control': 'max-age=0',
            # ':scheme': 'https',
            # 'referer': 'https://www.aliexpress.com',
            # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            # 'sec-fetch-mode': 'navigate',
            # 'sec-fetch-site': 'same-origin',
            # 'sec-fetch-user': '?1',
            # 'upgrade-insecure-requests': '1',
            # 'user-agent': self.user_agent_r
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'cookie': cookie
        }
        return headers
    def start_url(self, url, page):
        """
        第一页
        https://www.aliexpress.com/store/2178176
        """
        shop = re.search(r'/store/(\d+)', url)
        w_shop = re.search(r'(\d+)\.html', url)
        if shop:
            shop_id = shop.group(1)
        elif w_shop:
            shop_id = w_shop.group(1)
        else:
            raise TypeError('请输入正确的店铺url')
        # 拼接全店铺商品第一页
        shop_url = f'https://www.aliexpress.com/store/{shop_id}/search/{page}.html'
        return shop_url

    def goods_list(self, url, s_p=True):
        '''
        商品列表
        '''
        # try:
        if s_p:
            # 起始页需要判断
            url = self.start_url(url, 1)
        path = re.search(r'https://www.aliexpress.com/(.*)', url).group(1)
        response = self.session.get(url, headers=self.headers(path))
        html = Selector(response.text)
        urls = self.goods_url(html)
        logger.info(f'列表url===={list(urls)}')
        if list(urls):
            for url in urls:
                # ProductsSpider(url).goods_info()
                self.redis_conn.rpush('aliexpress_url', url)
                # 下一页
            next_page = html.xpath('//a[@class="ui-pagination-next"]/@href').get()
            time.sleep(random.randint(4, 7))
            if next_page:
                page_url = 'https:' + next_page
                logger.info(f'进入下一页================={page_url}')
                self.goods_list(page_url, False)
        else:
            logger.info('获取列表失败，重新登录')
            LoginAli().run_login()
            self.goods_list(url)
        # except Exception as e:
        #     logger.info(e)

    def goods_url(self, html):
        '''
        提取每页商品url
        '''
        lis = html.xpath(
            '//ul[@class="items-list util-clearfix"]/li/div[@class="img"]/div[@class="pic"]/a/@href').extract()
        if lis:
            for li in lis:
                url = 'https:' + li
                yield url
        else:
            return []
