# -*- coding: utf-8 -*-
# @Time    : 2021/7/15 16:04
# @Author  : Haijun
import datetime
import random
import re
import threading
import redis
import json

from multiprocessing.dummy import Pool
from parsel import Selector
from lib.base_fun import logger, proxy, request_post
from dynaconf import settings


class Reviews(object):
    def __init__(self, product_id, owner_member_id):
        self.url = 'https://feedback.aliexpress.com/display/productEvaluation.htm'
        self.product_id = product_id
        self.owner_member_id = owner_member_id
        self.order_reviews = []
        self.num = random.randint(30, 200)
        self.total_page = 0
        self.cur_page = 1
        self.pool = Pool(5)

    def request_reviews(self, page):
        '''

        '''
        data = {
            'ownerMemberId': self.owner_member_id,  # 251128372 240039249
            'memberType': 'seller',
            'productId': self.product_id,  # 1005003002680274 1005001798022744
            'companyId': '',
            'evaStarFilterValue': 'all Stars',
            'evaSortValue': 'sortlarest@feedback',  # sortdefault@feedback  sortlarest@feedback
            'page': page,
            'currentPage': 1,
            'startValidDate': '',
            'i18n': 'true',
            'withPictures': 'false',
            'withAdditionalFeedback': 'false',
            'onlyFromMyCountry': 'false',
            'version': '',
            'isOpened': 'true',
            'translate': 'Y',
            'jumpToTop': 'false',
            'v': 2
        }
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        }
        # form请求
        status, response = request_post(url=self.url, data=data, headers=headers,
                                        proxy=proxy(settings.PROXY_USER1, settings.PROXY_PWD1))
        logger.info(f'状态====={status}')
        if status == 200:
            return response

    def crawl_reviews(self, page=1, flat=False):
        logger.info(f'页数：{page}')
        logger.info(f'id：{self.product_id}')
        response = self.request_reviews(page)
        if response:
            html = Selector(response.text)
            div_list = html.xpath('//div[@class="feedback-list-wrap"]/div')
            if not div_list:
                return div_list
            if flat:
                self.pages(html)
            for div in div_list:
                data_dict = {}
                data_dict['userName'] = self._user_name(div)
                data_dict['country'] = self._country(div)
                data_dict['star'] = self._star(div)
                data_dict['orderInfo'] = self._order_info(div)
                data_dict['contentsText'] = self._contents_text(div)
                data_dict['imageList'] = self._image_list(div)
                data_dict['rTime'] = self.review_time(div)
                if data_dict['userName'] and data_dict['contentsText']:
                    self.order_reviews.append(data_dict)
                logger.info(data_dict)
        return self.order_reviews

    def review_results(self):
        r = self.crawl_reviews(1, True)
        if r:
            logger.info(f'self.num===={self.num}')
            num = int(self.num / 10) + 1
            if self.total_page >= num:
                self.pool.map(self.crawl_reviews, range(2, num))
                while True:
                    if len(self.order_reviews) < self.num:
                        num += 1
                        if self.total_page >= num:
                            self.crawl_reviews(num)
                        else:
                            break
                    else:
                        break
            elif self.total_page >= 2 and self.total_page <= num:
                self.pool.map(self.crawl_reviews, range(2, self.total_page))
        return self.order_reviews

    def pages(self, html):
        total_reviews = html.xpath('//div[@class="customer-reviews"]/text()').get()
        if total_reviews:
            number = re.search(r'(\d+)', total_reviews).group(1)
            self.total_page = int(int(number) / 10) + 1

    @staticmethod
    def _user_name(div):
        u = div.xpath('./div[@class="fb-user-info"]/span[@class="user-name"]/a/text()').get()
        if not u:
            u = div.xpath('./div[@class="fb-user-info"]/span[@class="user-name"]/text()').get()
        return u

    @staticmethod
    def _country(div):
        return div.xpath('./div[@class="fb-user-info"]/div[@class="user-country"]/b/text()').get()

    @staticmethod
    def _star(div):
        _width = div.xpath(
            './div[@class="fb-main"]/div[@class="f-rate-info"]/span[@class="star-view"]/span/@style').get()
        try:
            n = int(_width.split(':')[1].replace('%', '')) / 20
        except AttributeError as e:
            n = 0
        return n

    @staticmethod
    def _order_info(div):
        spans = div.xpath('./div[@class="fb-main"]/div[@class="user-order-info"]/span')
        property_list = []
        for span in spans:
            prop_dict = {}
            _prop_name = span.xpath('./strong/text()').get()
            prop_dict['propName'] = _prop_name.replace(':', '') if _prop_name else ''
            _prop_value = span.xpath('./text()').extract()
            _prop_value = [k.strip() for k in
                           [i.replace('\n', '').replace('\t', '').replace('\xa0', ' ') for i in _prop_value] if
                           k.strip()] if _prop_value else None
            prop_dict['propValue'] = _prop_value[0] if _prop_value else None
            property_list.append(prop_dict)
        return property_list

    @staticmethod
    def _contents_text(div):
        return div.xpath(
            './div[@class="fb-main"]/div[@class="f-content"]/dl[@class="buyer-review"]/dt[@class="buyer-feedback"]/span[1]//text()').get()

    @staticmethod
    def _image_list(div):
        return div.xpath(
            './div[@class="fb-main"]/div[@class="f-content"]/dl[@class="buyer-review"]/dd[@class="r-photo-list"]/ul[@class="util-clearfix"]/li/@data-src').extract()

    def review_time(self, div):
        time_format = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        r_time = div.xpath(
            './div[@class="fb-main"]/div[@class="f-content"]/dl[@class="buyer-review"]/dt[@class="buyer-feedback"]/span[2]//text()').get()
        if r_time:
            time_format = datetime.datetime.strptime(r_time, '%d %b %Y %H:%M').strftime(
                "%Y-%m-%d %H:%M:%S")

        return time_format
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


