# -*- coding: utf-8 -*-
# @Time    : 2020/8/24 14:34
# @Author  : Haijun

import json
import random
import re
import http.client
import redis

from lib.base_fun import logger, proxy, request_get, headers
from dynaconf import settings

http.client._is_legal_header_name = re.compile(rb'[^\s][^:\r\n]*').fullmatch


class ProductsSpider(object):

    def __init__(self, url):
        self.url = url
        self.redis_conn = redis.StrictRedis(host=settings.REDIS.HOST, port=settings.REDIS.PORT, db=settings.REDIS.DB,
                                            password=settings.REDIS.PASSWD)
        self.goods_data = {
            'code': False,
            'item': {}
        }

    def goods_info(self):
        ali_id = re.findall(r'(\d+)\.html', self.url)
        if ali_id:
            ali_id = ali_id[0]
            ali_link = 'https://www.aliexpress.com/item/' + str(ali_id) + '.html'
            path = '/item/' + str(ali_id) + '.html'
            try:
                status, response = request_get(ali_link, headers=headers(path),
                                               proxy=proxy(settings.PROXY_USER1, settings.PROXY_PWD1))
                if status == 200:
                    response_text = response.text
                    _data = re.findall(r'data:(.*),.*csrfToken:', response_text, re.S)[0]
                    data = json.loads(_data)
                    if data:
                        item = {}
                        item['category'] = self.category(data)
                        item['commentNumber'] = self.review(data)
                        item['createTime'] = None
                        item['deleteSkuIds'] = []
                        item['description'] = ''
                        item['detailUrl'] = self.detail_url(data)
                        if item['detailUrl']:
                            item['detailsImgs'], item['document'] = self.parse_desc(item['detailUrl'])
                        else:
                            item['detailsImgs'] = None
                            item['document'] = None
                        item['goodsCreateTime'] = ''
                        item['goodsExtDetailId'] = 0
                        item['goodsImages'] = self.images(data)
                        item['goodsVideos'] = self.video(data)
                        item['id'] = 0
                        item['ip'] = ''
                        item['isFix'] = ''
                        item['isShow'] = ''
                        item['itemNumber'] = ''
                        item['key'] = ''
                        item['mainImage'] = item['goodsImages'][0]
                        item['maxMarketPrice'] = self.max_market_price(data)
                        item['maxPrice'] = self.max_price(data)
                        item['minMarketPrice'] = self.min_market_price(data)
                        item['minPrice'] = self.min_price(data)
                        item['name'] = self.product_title(data)
                        item['orginalName'] = self.product_title(data)
                        item['newAddSkuIds'] = [0]
                        item['originalDescription'] = ''
                        item['originalSizeTables'] = [{"rowName": [None], "value": "string"}]
                        item['originalStoreName'] = ''
                        item['orignalMaxMarketPrice'] = 0
                        item['orignalMaxPrice'] = 0
                        item['orignalMinPrice'] = 0
                        item['packageSize'] = {"height": "string", "length": "string", "width": "string"}
                        item['productId'] = ali_id
                        item['productNoFound'] = False
                        item['productUrl'] = ali_link
                        item['properties'] = self.prop_name_value(data)
                        item['saleStock'] = 0
                        item['score'] = self.star(data)  # 评分
                        item['shopId'] = ''
                        item['shopQualification'] = ''
                        item['showMarketPrice'] = 0
                        item['showPrice'] = 0
                        item['sizeImage'] = 0
                        item['sizeTables'] = [{"rowName": [None], "value": "string"}]
                        item['skuList'], item['skuIds'] = self.sku_price_list(data, ali_id)
                        item['skuPrice'] = 0
                        item['specs'] = self.specification(data)
                        item['storeName'] = self.store_name(data)
                        item['storeUrl'] = self.store_url(data)
                        item['type'] = 0
                        item['updatePrice'] = True
                        item['updateSkuPrice'] = True
                        item['url'] = None
                        item['weight'] = None
                        item['years'] = self.opened_year(data)
                        item['shippingFrom'] = self.shipping_from(data)
                        item['keywords'] = self.keywords(data)
                        item['ownerMemberId'] = self.seller_admin_seq(data)
                        item['tradeCount'] = self.trade_count(data)
                        item['isActivity'] = self.is_activity(data)
                        # item['orderReviews'] = Reviews().crawl_reviews(ali_id, self.seller_admin_seq(data))
                        self.goods_data['code'] = True
                        self.goods_data['item'] = item
                        # 评论
                        ae_reviews_id = {
                            "product_name": item['name'],
                            'product_id': ali_id,
                            'owner_member_id': self.seller_admin_seq(data),
                            'tag': True
                        }
                        self.redis_conn.lpush('ae_reviews_id', json.dumps(ae_reviews_id))
                        goods_data_dict = json.dumps(self.goods_data, ensure_ascii=False)
                        self.redis_conn.lpush(settings.SAVE_GOODS_TO_REDIS_KEY, goods_data_dict)
                        logger.info(f'爬取成功： {self.url}')
                    else:
                        self.redis_conn.rpush('aliexpress_url', self.url)
                        logger.error(f'失败url:   {self.url}')
                elif status == 404:
                    logger.error(f'商品已经下架:   {self.url}')
                else:
                    self.redis_conn.rpush('aliexpress_url', self.url)
                    logger.error(f'失败url:   {self.url}')
            except Exception as e:
                logger.error(f'失败url:   {self.url} ==== {e}')
                self.redis_conn.rpush('aliexpress_url', self.url)
        return self.goods_data

    def is_activity(self, data):
        try:
            _is_show_banner = data['middleBannerModule']['showUniformBanner']
        except Exception as e:
            _is_show_banner = False
        return _is_show_banner

    @logger.catch()
    def parse_desc(self, desc_url):
        '''
        详情
        '''
        # path = re.search(r'\.com(.*)', desc_url).group(1)
        status, response = request_get(desc_url)
        # 详情图片
        response_text = response.text
        text2 = re.sub('<table.*?table>', '', response_text, re.S)
        text3 = re.sub(r'<a.*?</a>', '', text2, re.S)
        img_desc = re.findall(r'src="(.*?)"', text3)
        if img_desc:
            tmp_img_desc = [i for i in img_desc if 'png' not in i]
            _img_desc = []
            for img in tmp_img_desc:
                if '.jpg' in img or '.jpeg' in img or '.webp' in img or '.bmp' in img:
                    if '?' in img:
                        img = img.split('?')[0]
                    if img.startswith('//'):
                        img = 'https:' + img
                    elif not img.startswith('https:') and not img.startswith('//'):
                        img = 'https://' + img
                    _img_desc.append(img)
            return _img_desc, response_text
        return [], response_text

    @staticmethod
    def seller_admin_seq(data):
        return data['storeModule']['sellerAdminSeq']

    @staticmethod
    def keywords(data):
        return data['pageModule']['keywords']

    @staticmethod
    def detail_url(data):
        '''
        详情url
        '''
        try:
            return data['descriptionModule']['descriptionUrl']
        except KeyError as e:
            return None

    @staticmethod
    def category(data):
        '''
        分类
        :param data:
        :return:
        '''
        crawl_category = data['crossLinkModule']['breadCrumbPathList']
        cate_list = []
        if len(crawl_category) > 1:
            categories = crawl_category[2:]
            for cate in categories:
                _category = {
                    'categoryString': cate['name'],
                    'categoryId': cate['cateId']
                }
                cate_list.append(_category)
        else:
            cate_list = [{
                'categoryString': 'Other',
                'categoryId': None
            }]

        return cate_list

    @staticmethod
    def images(data):
        '''
        产品图片
        :param data:
        :return:
        '''
        image = data['imageModule']['imagePathList']
        if image:
            image_list = []
            for img in image:
                if img.startswith('//'):
                    img = 'https:' + img
                elif not img.startswith('https:') and not img.startswith('//'):
                    img = 'https://' + img
                pattern = re.compile(r'.*(\.jpg|\.jpeg|\.png)')
                img_format = pattern.match(img)
                if img_format:
                    _image = img + "_Q90" + img_format.group(1) + "_.webp"
                    image_list.append(_image)

            image = image_list
        return image

    @staticmethod
    def video(data):
        '''
        视频
        :param data:
        :return:
        '''
        try:
            video_url_list = []
            video_id = data['imageModule']['videoId']
            video_uid = data['imageModule']['videoUid']
            video_url = 'https://cloud.video.taobao.com/play/u/' + str(
                video_uid) + '/p/1/e/6/t/10301/' + str(video_id) + '.mp4'
            video_url_list.append(video_url)
        except Exception as e:
            video_url_list = []

        return video_url_list

    @staticmethod
    def max_price(data):
        '''
        最高价格
        :param data:
        :return:
        '''
        try:
            hig_price = data['priceModule']['maxActivityAmount']['value']
        except Exception as e:
            hig_price = data['priceModule']['maxAmount']['value']
        return hig_price

    def max_market_price(self, data):
        hig_price = data['priceModule']['maxAmount']['value']
        return hig_price

    @staticmethod
    def min_price(data):
        '''
        最低价格
        :param data:
        :return:
        '''
        try:
            low_price = data['priceModule']['minActivityAmount']['value']
        except Exception as e:
            low_price = data['priceModule']['minAmount']['value']
        return low_price

    @staticmethod
    def min_market_price(data):
        low_price = data['priceModule']['minAmount']['value']
        return low_price

    @staticmethod
    def prop_name_value(data):
        properties = []
        try:
            property_list = data['skuModule']['productSKUPropertyList']  # 属性集
            for prop in property_list:
                property_name = {
                    'id': prop.get('skuPropertyId', None),  # 属性名id
                    'name': prop.get('skuPropertyName', None),  # 属性名
                    'orginalName': prop.get('skuPropertyName', None),  # 属性名
                    # 'order': prop.get('order', None)  # 排序
                }
                sku_property_values = prop.get('skuPropertyValues', None)
                properties_value = []
                if sku_property_values:
                    for _value in sku_property_values:
                        values = {
                            'id': _value.get('propertyValueIdLong', None),
                            'imgId': None,
                            'imgUrl': _value.get('skuPropertyImagePath', None),
                            'mainUrl': _value.get('skuPropertyImagePath', None),
                            'value': _value.get('propertyValueName', None),
                            'orginalValue': _value.get('propertyValueDisplayName', None),
                        }
                        properties_value.append(values)
                property_name['values'] = properties_value
                properties.append(property_name)
        except Exception as e:
            property_name = {
                "id": 0,
                "name": "Color",
                'orginalName': 'Color',
                "values": [
                    {
                        'id': 0,
                        'imgId': None,
                        'imgUrl': None,
                        'mainUrl': None,
                        'value': 'As Picture',
                        'orginalValue': 'As Picture',
                    }
                ]
            }
            properties.append(property_name)
        return properties

    def sku_price_list(self, data, product_id):
        sku_list = data['skuModule']['skuPriceList']
        sku_prop_value = []
        sku_ids = []
        if sku_list:
            for sku_price in sku_list:
                sku = {}
                # 属性值id集合
                sku['channel'] = 0
                # 是否新用户
                is_new_user = data['priceModule'].get('activityMessage', None)
                if is_new_user:
                    try:
                        cost_price = sku_price['skuVal']['skuAmount']['value']
                    except KeyError as e:
                        cost_price = sku_price['skuVal']['skuMultiCurrencyCalPrice']
                else:
                    try:
                        cost_price = sku_price['skuVal']['skuActivityAmount']['value']
                    except KeyError as e:
                        cost_price = sku_price['skuVal']['skuAmount']['value']
                sku['costPrice'] = cost_price
                sku['createTime'] = None
                sku['goodsId'] = product_id
                sku['id'] = None
                try:
                    sku['marketPrice'] = sku_price['skuVal']['skuAmount']['value']
                except Exception as e:
                    sku['marketPrice'] = sku_price['skuVal']['skuCalPrice']
                try:
                    sku['orginalMarketPrice'] = sku_price['skuMultiCurrencyDisplayPrice']
                except Exception as e:
                    sku['orginalMarketPrice'] = sku['marketPrice']
                sku['name'] = None
                sku['num'] = None
                sku['orginalPrice'] = None
                sku['originalSkuId'] = None
                sku['price'] = sku['costPrice']
                sku['pvalueDesc'] = None
                sku['pvalueStr'] = None
                sku['ratio'] = None
                sku['skuId'] = sku_price.get('skuId', '0')
                sku['stock'] = sku_price['skuVal']['availQuantity']  # 库存
                sku['skuPropIds'] = sku_price.get('skuPropIds', '') or '0'
                sku['skuAttr'] = sku_price.get('skuAttr', '0:0') or '0:0'
                sku_prop_value.append(sku)
                sku_ids.append(sku['skuId'])
        return sku_prop_value, sku_ids

    @staticmethod
    def shipping_from(data):
        '''
        发货地
        :param data:
        :return:
        '''
        country = data['storeModule']['countryCompleteName']
        try:
            property_list = data['skuModule']['productSKUPropertyList']  # 属性集
            shipping_from = []
            for prop in property_list:
                if prop['skuPropertyName'] == 'Ships From':
                    # 发货地

                    country_list = prop['skuPropertyValues']

                    for k in range(len(country_list)):
                        country_dict = {}
                        country_dict['name'] = country_list[k][
                            'propertyValueName']
                        country_dict['code'] = country_list[k][
                            'skuPropertySendGoodsCountryCode']
                        country_dict['currency'] = ''
                        country_dict['description'] = ''
                        country_dict['sort'] = k + 1
                        shipping_from.append(country_dict)
            if shipping_from == []:
                country_dict = {}
                country_dict['name'] = country
                country_dict['code'] = ''
                country_dict['currency'] = ''
                country_dict['description'] = ''
                country_dict['sort'] = 1
                shipping_from.append(country_dict)
            else:
                shipping_from = shipping_from
        except Exception as e:
            shipping_from = []
            country_dict = {}
            country_dict['name'] = country
            country_dict['code'] = ''
            country_dict['currency'] = ''
            country_dict['description'] = ''
            country_dict['sort'] = 1
            shipping_from.append(country_dict)
        return shipping_from

    @staticmethod
    def specification(data):
        '''
        参数部分
        :param data:
        :return:
        '''
        try:
            specs = data['specsModule']['props']
            specs_list = []
            append = specs_list.append
            for spec in specs:
                specs_dict = {}
                specs_dict['key'] = spec['attrName']
                specs_dict['originalKey'] = spec['attrName']
                specs_dict['value'] = spec['attrValue']
                specs_dict['originalValue'] = spec['attrValue']
                append(specs_dict)
        except Exception as e:
            specs_list = []
        return specs_list

    @staticmethod
    def opened_year(data):
        '''
        开店年限
        :param data:
        :return:
        '''
        try:
            year = data['storeModule']['openedYear']
        except Exception as e:
            year = 0
        return year

    @staticmethod
    def positive_rate(data):
        '''
        好的回馈率
        :param data: regionCountryName
        :return:
        '''
        try:
            rate = data['storeModule']['positiveRate']
        except Exception as e:
            rate = ''
        return rate

    @staticmethod
    def product_id(data):
        '''
        产品id
        :param data:
        :return:
        '''
        id = data['storeModule']['productId']
        return id

    @staticmethod
    def store_name(data):
        '''
        店铺名称
        :param data:
        :return:
        '''
        try:
            name = data['storeModule']['storeName']
        except Exception as e:
            name = ''
        return name

    @staticmethod
    def store_url(data):
        '''
        店铺url
        :param data:
        :return:
        '''
        try:
            url = 'https:' + data['storeModule']['storeURL']
        except Exception as e:
            url = ''
        return url

    @staticmethod
    def store_id(data):
        '''
        店铺id
        :param data:
        :return:
        '''
        try:
            id = data['storeModule']['storeNum']
        except Exception as e:
            id = ''
        return id

    @staticmethod
    def product_title(data):
        '''
        产品名称
        :param data:
        :return:
        '''
        title = data['titleModule']['subject']
        return title

    @staticmethod
    def trade_count(data):
        '''
        交易数量,
        :param data:
        :return:
        '''
        sales = data['titleModule']['formatTradeCount']
        return sales

    @staticmethod
    def product_url(data):
        '''
        产品url
        :param data:
        :return:
        '''
        url = data['storeModule']['detailPageUrl']
        if url:
            url = url.split('?')[0]
        return url

    @staticmethod
    def review(data):
        '''
        浏览量
        :param data:
        :return:
        '''
        num = data['titleModule']['feedbackRating']['totalValidNum']
        return num

    @staticmethod
    def wished_count(data):
        '''
        收藏量
        :param data:
        :return:
        '''
        wished_count = data['actionModule']['itemWishedCount']
        return wished_count

    @staticmethod
    def star(data):
        '''
        星级
        :param data:
        :return:
        '''

        avarage_star = data['titleModule']['feedbackRating']['averageStar']
        return avarage_star

    @staticmethod
    def sku_id_and_attr(data):
        skus = data['skuModule']['skuPriceList']

        sku_list = []
        for sku in skus:
            sku_dict = {}
            sku_dict['skuAttr'] = sku['skuAttr']
            sku_dict['skuId'] = sku['skuId']
            sku_list.append(sku_dict)
        return sku_list
