# -*- coding: utf-8 -*-
# @Time    : 2021/7/18 15:26
# @Author  : Haijun

import json
import re
import redis
from lib.base_fun import logger, request_get
from apps.haiying_wish.wish.login_wish import LoginWish
from dynaconf import settings


class Wish(object):
    def __init__(self):
        self.redis_conn = redis.StrictRedis(host=settings.REDIS.HOST, port=settings.REDIS.PORT, db=settings.REDIS.DB,
                                            password=settings.REDIS.PASSWD)
        self.data = {
            'code': False,
            'item': dict()
        }

    def cookie(self):
        _cookie = self.redis_conn.get(settings.WISH.WISH_COOKIE)
        if _cookie:
            _cookie = _cookie.decode('utf-8')
            logger.info(f'cookies====={_cookie}')
        else:
            logger.error(f'没有cookie 重新弄登录')
            _xsrf, _cookie = LoginWish().run_login()
        return _cookie

    def _headers(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            # 'cookie': self.cookie(),
            # 'cookie': 'bsid=7955a54619eb4c019623303ab385fbb0;_fbp=fb.1.1626772165936.386786848;visitor_id=d016a45881094c2da3096f508b53e489;_dcmn_p=8-BeY2lkPU44MXRSMkQzeVNiZlZYX3BBUG8;logged_out_tracker=dfff5b50060a19cd009db3c2c0b01edc8dbd966d567d84aa61ea7af48b56c86a;_gid=GA1.2.1881824203.1626772165;_ga=GA1.2.1102781720.1626772165;tatari-session-cookie=026b910d-95f2-3c2a-ff6c-326d77a7fa26;__ssid=cef7777054d95990c255189ef3cb65d;G_ENABLED_IDPS=google;_dcmn_p=8-BeY2lkPU44MXRSMkQzeVNiZlZYX3BBUG8;_dcmn_p=8-BeY2lkPU44MXRSMkQzeVNiZlZYX3BBUG8;__stripe_mid=a32d6bf0-fea7-4800-8102-8a557829eed2ba4b37;_tq_id.TV-09458190-1.2013=58f5b4beadb84513.1626851623.0.1626853058..;tatari-cookie-test=20997627;__stripe_sid=8b42b183-0b1a-4a0a-980f-e547383bae3acb0684;IR_12396=1626855794223%7C0%7C1626855794223%7C%7C;logged_out_locale=en;_xsrf=2|dbbd291f|d3aa08cdf5bab90255ff7fdb96cc0968|1626855789;_timezone=8;_is_desktop=true;sweeper_uuid=1507a50a7b7941baa11a064d9d64ecf6;_uetsid=2de106b0e93a11ebb9f3e92c0fe2b9c0;_uetvid=2de169c0e93a11eb8afa770f5b78c196;IR_gbd=wish.com;notice_preferences=2:;notice_gdpr_prefs=0,1,2:'
            'cookie': f'visitor_id=19a53d15a09b4096ad4d4f0469ce13a7; tatari-session-cookie=e5934199-0a0d-39d6-9727-d192537bc499; __ssid=556b8d5b45f1d1c2b700f30258fb2a6; __stripe_mid=88ee989b-8933-40e9-8cd5-66a1f908317b8f7ed2; _pin_unauth=dWlkPU1EUTFOVE16T1dVdE5UZ3dZaTAwWmprNExXSmlOamN0TmpGbE1qRTJOV0l6TjJZMw; G_ENABLED_IDPS=google; _fbp=fb.1.1626252903523.1770009377; authentication_id=d6101e62950b3588a45b497b0e43279a; _dcmn_p=x6VeY2lkPXVXSFBNMkR6MU1QeF95RjJBQk0; _dcmn_p=x6VeY2lkPXVXSFBNMkR6MU1QeF95RjJBQk0; rskxRunCookie=0; rCookie=f0aeiu1l57m1c5q9wiutw3kr8yw9ke; _ga=GA1.2.1279326244.1626252829; _ga_S8FFZTJ4RL=GS1.1.1626628281.2.0.1626628281.0; IR_gbd=wish.com; logged_out_locale=en; bsid=0fc612111a2a4891b53e3f19620df299; _xsrf=2|ab7bfe0a|e175c74804290e77c822f4ad37ab6cb0|1626769283; _timezone=8; _is_desktop=true; vendor_user_tracker=8e9b10c617dde4928c346c611b67e8df9f4c076349e77468d6b2e960efd718df; sweeper_session="2|1:0|10:1626769301|15:sweeper_session|84:ODU1N2ZiZTQtZDEwNC00YzE2LWFlZmEtMTU3NjI3MzRiOTA0MjAyMS0wNy0yMCAwODoyMTozNC4xMjE3NTI=|4877bec9a8283aa10f5f6f67ba7c3a4f9c51f2add2096d5414156aa89e71f34f"; sessionRefreshed_60f3d26d94fdf1d17eb88a63=true; isDailyLoginBonusModalLoaded=true; _dcmn_p=x6VeY2lkPXVXSFBNMkR6MU1QeF95RjJBQk0; sweeper_uuid=6d8d6243c66e491c989e7f78b142cbce; IR_12396=1626771761072%7C0%7C1626771761072%7C%7C; IR_PI=807ae331-3513-11eb-99e3-42010a246309%7C1626858161072; lastRskxRun=1626771761457; __stripe_sid=9210ec79-99c1-4d78-a5ba-2a99e0807bc4b72b79; number_of_product_per_row=4; _tq_id.TV-09458190-1.2013=cd6eba59aa4035e0.1626769303.0.1626773018..; _uetsid=0750ed20e79611eb97ea616a5c45d489; _uetvid=02c9c510e48111ebbd9e89268d36dcf9'
        }
        return headers

    def response_text(self, product_id):
        url = f'https://www.wish.com/product/{product_id}?share=web'
        status, response = request_get(url=url, headers=self._headers())
        _data_str = re.search(r'window.__PRELOADED_STATE__ = (.*?)</script>', response.text, re.S)
        if _data_str:
            data = _data_str.group(1)
            data_dict = json.loads(data)
            return data_dict
        return None

    def crawl_wish(self, product_id):
        data = self.response_text(product_id)
        if data:
            login_data = data['data']
            # user_info = login_data['user']['userInfo'].get('id')
            # if not user_info:
            #     # 未登录，需重新登录
            #     logger.error(f'需要重新登录')
            #     # _xsrf, _cookie = LoginWish().run_login()
            #     #
            #     # self.crawl_wish(product_id)
            #     return
            product = login_data['product'][product_id]['staticFields']
            # print(json.dumps(product))
            item = dict()
            item['productId'] = product_id
            item['name'] = self.name(product)
            item['document'] = self.document(product)
            item['score'] = self.score(product)
            item['storeName'] = self.store_name(product)
            item['shopId'], item['storeUrl'] = self.store_url(product)
            item['mainImage'] = self.main_image(product)
            item['goodsImages'] = self.goods_images(product)
            item['category'] = self.category(product)
            # item['skuList'] = self.variations(product)
            return item

    @staticmethod
    def name(data):
        '''商品名'''
        return data['name']

    @staticmethod
    def document(data):
        '''详情文本'''
        return data['description']

    @staticmethod
    def score(data):
        '''评分'''
        return data['productRating']['rating']

    @staticmethod
    def store_name(data):
        return data['merchantInfo']['title']

    @staticmethod
    def store_url(data):
        merchant_id = data['commerceProductInfo']['merchant_id']
        shop_url = f'https://www.wish.com/merchant/{merchant_id}'
        return merchant_id, shop_url

    @staticmethod
    def main_image(data):
        return data['productPagePicture']

    @staticmethod
    def goods_images(data):
        images = data['extraPhotoUrls']
        image_list = [image for image in images.values() if images]
        return image_list

    @staticmethod
    def category(data):
        c = data['categoryListV2']
        _category = [
            {
                'categoryString': i['category'],
                'categoryId': i['id'],
                'displayShortCategory': i['display_short_category'
                ]
            } for i in c]
        return _category

    @staticmethod
    def variations(data):
        _variations = data['commerceProductInfo']['variations']
        sku_list = []
        for v in _variations:
            sku_dict = {}

            color = v.get('color', None)
            property = []
            if color:
                property.append({
                    'name': 'color',
                    'value': color
                })
            size = v.get('size', None)
            if size:
                property.append({
                    'name': 'size',
                    'value': size
                })
            sku_dict['properties'] = property
            sku_dict['price'] = v.get('price')
            sku_dict['skuId'] = v.get('variation_id', None)
            sku_dict['originMarketPrice'] = v.get('retail_price', None)
            sku_dict['stock'] = v.get('inventory', 0)
            sku_list.append(sku_dict)

    @staticmethod
    def properties(data):
        _property = data['dimensionToValues']

    @staticmethod
    def keywords(data):
        d = data['keywords']
        if d:
            return d[0]
        return None
