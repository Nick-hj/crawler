# -*- coding: utf-8 -*-
# @Time    : 2021/7/19 17:19
# @Author  : Haijun

import os
import re
import time
import random
import asyncio
import pyppeteer
import pyppeteer.errors
import redis

from dynaconf import settings

from lib.base_fun import logger

'''CLICK_WEB_LOGIN_MODAL_EMAIL'''
'''
获取token
https://static.securedtouch.com/sdk/pong.js?body=eyJwaW5nVmVyc2lvbiI6IjEuMS4wcCIsImFwcElkIjoid2lzaCJ9
'''


class LoginWish(object):
    """
    登录
    """
    pyppeteer.DEBUG = True
    page = None
    base_path = os.path.join(settings.HOME_DIR, 'user_data_dir')
    redis_conn = redis.StrictRedis(host=settings.REDIS.HOST, port=settings.REDIS.PORT, db=settings.REDIS.DB,
                                   password=settings.REDIS.PASSWD)

    def __init__(self):
        self.xsrf = ''
        self.cookie = ''

    async def _injection_js(self):
        """
            注入js
        """
        js1 = '''() =>{

                   Object.defineProperties(navigator,{
                     webdriver:{
                       get: () => false
                     }
                   })
                }'''

        js2 = '''() => {
                alert (
                    window.navigator.webdriver
                )
            }'''

        js3 = '''() => {
                window.navigator.chrome = {
            runtime: {},
            // etc.
          };
            }'''

        js4 = '''() =>{
        Object.defineProperty(navigator, 'languages', {
              get: () => ['en-US', 'en']
            });
                }'''

        js5 = '''() =>{
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5,6],
          });
                }'''

        js6 = '''
            ()=>{
                const newProto = navigator.__proto__;
                delete newProto.webdriver;
                navigator.__proto__ = newProto;
            }
        '''

        await self.page.evaluateOnNewDocument(js1)
        # await self.page.evaluate(js2)
        await self.page.evaluateOnNewDocument(js3)
        await self.page.evaluateOnNewDocument(js4)
        await self.page.evaluateOnNewDocument(js5)
        await self.page.evaluateOnNewDocument(js6)

    async def _init(self):
        """初始化浏览器
        """
        self.browser = await pyppeteer.launch({'headless': False,  # headless=True 启动无头模式
                                               'userDataDir': self.base_path,
                                               'args': [
                                                   # '--window-size={1300},{600}'
                                                   # '--disable-extensions',
                                                   # '--hide-scrollbars',
                                                   # '--disable-bundled-ppapi-flash',
                                                   # '--mute-audio',
                                                   '--no-sandbox',
                                                   # '--disable-setuid-sandbox',
                                                   # '--disable-gpu',
                                                   # "--proxy-server=http://127.0.0.1:20800", # --proxy-server 启动代理
                                                   # "--proxy-server=" + proxies(), # --proxy-server 启动代理
                                                   # '--disable-infobars',
                                               ],
                                               # 'dumpio': True,
                                               })

        self.page = await self.browser.newPage()
        # 禁止加载JavaScript，可提高加载速度，视情况确定True/False，
        await self.page.setJavaScriptEnabled(enabled=False)
        # 运行js来修改window.navigator.webdriver属性值，绕过webdriver检测
        await self.page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

        await self.page.setUserAgent(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36')
        # await browser.createIncognitoBrowserContext()
        # 输入代理账号密码
        # await self.page.authenticate(authens())
        # await self.page.setExtraHTTPHeaders({"property":proxies()}) # 在pyppeteer中和puppeteer是一样的，都不能把隧道加在args里，只能加在headers里
        # 设置浏览器大小
        await self.page.setViewport({'width': 1300, 'height': 600})

    async def _get_cookie(self):
        cookies_list = await self.page.cookies()
        cookies = ''
        for cookie in cookies_list:
            str_cookie = '{0}={1};'
            str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
            cookies += str_cookie
        return cookies

    async def main(self, url, username, pwd):
        """
        登陆
        """
        # 初始化浏览器
        await self._init()
        # 打开登陆页面
        logger.info(f'开始打开主页')
        await self.page.goto(url)
        time.sleep(20)
        # 注入js
        await self._injection_js()
        # 输入用户名
        await self.page.type('[data-testid="login-username"]', username, {'delay': random.randint(100, 151) - 50})
        # 输入密码
        await self.page.type('[data-testid="login-password"]', pwd, {'delay': random.randint(100, 151)})
        time.sleep(random.random() * 2)
        # 点击登陆
        time.sleep(7)
        logger.info(f'开始点击登录')
        await self.page.click('[data-testid="login-button"]')
        # 获取cookie
        time.sleep(10)
        await self.page.goto('https://www.wish.com/feed/tag_53dc186421a86318bdc87f1c')
        # with open('data.txt', 'w') as f:
        #     f.write(await self.page.content())
        logger.info(f'开始获取cookie')
        _cookie = await self._get_cookie()
        # 提取cookie种的xsrf
        logger.info(f'登录获取cookie====={_cookie}')
        _xsrf = re.search(r'_xsrf=(.*?);', _cookie, re.I)
        if _xsrf:
            xsrf = _xsrf.group(1)
            self.redis_conn.set(settings.WISH.WISH_XSRF, xsrf)
            self.redis_conn.set(settings.WISH.WISH_COOKIE, _cookie)
            return xsrf, _cookie
        else:
            self.run_login()

    def run_login(self):
        try:
            username = settings.WISH.USERNAME
            password = settings.WISH.PASSWD
            login_url = 'https://www.wish.com'
            loop = asyncio.get_event_loop()
            task = asyncio.ensure_future(self.main(login_url, username, password))
            loop.run_until_complete(task)
        except pyppeteer.errors.TimeoutError as e:
            logger.error(e)
            self.run_login()
        except pyppeteer.errors.BrowserError as e:
            logger.error(e)
            self.run_login()
        # finally:
        # self.browser.close()


def login_wish():
    LoginWish().run_login()


if __name__ == '__main__':
    login_wish()
