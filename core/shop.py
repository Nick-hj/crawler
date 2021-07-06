# -*- coding: utf-8 -*-
# @Time    : 2021/6/29 15:24
# @Author  : Haijun
import json
import random
import re
import time

from parsel import Selector
from lib.base_fun import logger, proxy, request_get, headers
from core.goods_detail import ProductsSpider
from dynaconf import settings

class ShopProducts(object):

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
        try:
            if s_p:
                # 起始页需要判断
                url = self.start_url(url, 1)
            path = re.search(r'https://www.aliexpress.com/(.*)', url).group(1)
            response_text = request_get(url, headers=headers(path), proxy=proxy())
            if response_text:
                html = Selector(response_text)
                urls = self.goods_url(html)
                if urls:
                    for url in urls:
                        ProductsSpider(url).goods_info()
                        time.sleep(random.randint(1, settings.SLEEP_TIME))
                        # 下一页
                    next_page = html.xpath('//a[@class="ui-pagination-next"]/@href').get()
                    time.sleep(random.randint(1, settings.SLEEP_TIME))
                    if next_page:
                        page_url = 'https:' + next_page
                        logger.info(f'进入下一页================={page_url}')
                        self.goods_list(page_url, False)
        except Exception as e:
            logger.info(e)

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
