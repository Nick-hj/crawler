# -*- coding: utf-8 -*-
# @Time    : 2020/8/24 14:39
# @Author  : Haijun
import os
import requests
from contextlib import closing

from loguru import logger as base_logger
from dynaconf import settings


def init_logger():
    '''
    日志
    '''
    base_logger.add(os.path.join('/data/logs', 'spider_info_{time:YYYY-MM-DD}.log'),
                    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file.path} | {module} | {function} | {line} | {message}",
                    level="INFO", rotation="00:00", retention='6 days', enqueue=True, encoding='utf-8')
    base_logger.add(os.path.join('/data/logs', 'spider_error_{time:YYYY-MM-DD}.log'),
                    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file.path} | {module} | {function} | {line} | {message}",
                    level="ERROR", rotation="00:00", retention='6 days', enqueue=True, encoding='utf-8')
    return base_logger


logger = init_logger()


# 代理
def proxy():
    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = settings.PROXY_USER
    proxyPass = settings.PROXY_PWD
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta
    }
    return proxies


def request_get(url, headers=None, proxy=None):
    '''
    get 请求
    '''
    # headers = kwargs.get('headers', None)
    # proxy = kwargs.get('proxy', None)
    try:
        with closing(requests.get(url=url, headers=headers, proxies=proxy)) as response:
            return response.text
    except requests.exceptions.ProxyError as e:
        with closing(requests.get(url=url, headers=headers)) as response:
            return response.text
    except Exception as e:
        logger.error(f'请求失败====={e}')
        return 404, ''


def headers(path):
    '''
    请求头
    '''
    headers = {
        ':authority': 'www.aliexpress.com',
        ':path': path,
        'accept-encoding': 'gzip,deflate,br',
        ':method': 'GET',
        'cache-control': 'max-age=0',
        ':scheme': 'https',
        'referer': 'https://www.aliexpress.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        # 'user-agent': self.user_agent_r
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'cookie': settings.AE_COOKIE
    }
    return headers
