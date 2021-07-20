# -*- coding: utf-8 -*-
# @Time    : 2021/7/15 16:04
# @Author  : Haijun
import re
import threading
import redis
import json

from parsel import Selector
from lib.base_fun import logger, proxy, request_form_post
from dynaconf import settings


class Reviews(object):
    def __init__(self, product_id, owner_member_id):
        self.url = 'https://feedback.aliexpress.com/display/productEvaluation.htm'
        self.product_id = product_id
        self.owner_member_id = owner_member_id
        self.order_reviews = []

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
        response_text = request_form_post(url=self.url, data=data, headers=headers, proxy=proxy())
        return response_text

    def crawl_reviews(self, page=1, flat=True):
        response_text = self.request_reviews(page)
        html = Selector(response_text)
        div_list = html.xpath('//div[@class="feedback-list-wrap"]/div')
        if not div_list:
            return div_list
        n = 1
        if flat:
            n = self.pages(html)
        for div in div_list:
            data_dict = {}
            data_dict['userName'] = self._user_name(div)
            data_dict['country'] = self._country(div)
            data_dict['star'] = self._star(div)
            data_dict['orderInfo'] = self._order_info(div)
            data_dict['contentsText'] = self._contents_text(div)
            data_dict['imageList'] = self._image_list(div)
            if data_dict['userName']:
                self.order_reviews.append(data_dict)
        if n > 1:
            t_list = []
            for _page in range(2, n + 1):
                t = threading.Thread(target=self.crawl_reviews, args=(_page, False))
                t.start()
                t_list.append(t)
            for i in t_list:
                i.join()
            # self.crawl_reviews(product_id, owner_member_id, _page, False)
        return self.order_reviews

    def pages(self, html):
        total_reviews = html.xpath('//div[@class="customer-reviews"]/text()').get()
        if total_reviews:
            number = re.search(r'(\d+)', total_reviews).group(1)
            total_page = int(int(number) / 10) + 1
            if total_page >= 5:
                n = 5
            else:
                n = total_page
            return n

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
            prop_dict['propName'] = _prop_name
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
