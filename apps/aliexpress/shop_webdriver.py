# -*- coding: utf-8 -*-
# @Time    : 2021/7/11 2:19
# @Author  : Haijun

import os
import time
import random
import asyncio
import pyppeteer
import redis

import pyppeteer.errors
from dynaconf import settings

from lib.base_fun import logger


class LoginAli(object):
    """
    登录
    """
    pyppeteer.DEBUG = True
    page = None
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_data_dir')
    redis_conn = redis.StrictRedis(host=settings.REDIS.HOST, port=settings.REDIS.PORT, db=settings.REDIS.DB,
                                   password=settings.REDIS.PASSWD)

    async def _injection_js(self):
        """注入js
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

        await self.page.evaluate(js1)
        # await self.page.evaluate(js2)
        await self.page.evaluate(js3)
        await self.page.evaluate(js4)
        await self.page.evaluate(js5)

    async def _init(self):
        """初始化浏览器
        """
        self.browser = await pyppeteer.launch({'headless': False,  # headless=True 启动无头模式
                                               'userDataDir': self.base_path,
                                               'args': [
                                                   # '--enable-automation=false',
                                                   # '--window-size={1300},{600}'
                                                   # '--disable-extensions',
                                                   # '--hide-scrollbars',
                                                   # '--disable-bundled-ppapi-flash',
                                                   # '--mute-audio',
                                                   '--no-sandbox',
                                                   # '--disable-setuid-sandbox',
                                                   # '--disable-gpu',
                                                   # "--proxy-server=" + proxies(), # --proxy-server 启动代理
                                                   # '--disable-infobars',
                                               ],
                                               # 'dumpio': True,
                                               })

        self.page = await self.browser.newPage()
        # 禁止加载JavaScript，可提高加载速度，视情况确定True/False，
        await self.page.setJavaScriptEnabled(enabled=False)
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

    async def mouse_slider(self):
        """
        滑动滑块
        """
        await asyncio.sleep(1)
        try:
            await self.page.hover('#nc_1_n1z')
            # 鼠标按下按钮
            await self.page.mouse.down()
            # 移动鼠标
            await self.page.mouse.move(2000, 0, {'steps': 30})
            # 松开鼠标
            await self.page.mouse.up()
            await asyncio.sleep(1)
        except Exception as e:
            print(e, '      :错误')
            return None
        else:
            await asyncio.sleep(1)
            # 获取元素内容
            slider_again = await self.page.querySelectorEval('#nc_1__scale_text span', 'node => node.textContent')
            if slider_again != 'Verified':
                return None
            else:
                print('验证通过')
                return True

    async def shop_list(self, shop_url):
        try:
            # await self.page.goto(shop_url)
            await self.check_login(shop_url)
            slider_again = await self.page.xpath('//div[@id="nc_1__scale_text"]')
            if slider_again:
                flag = await self.mouse_slider()
                if not flag:
                    print('滑动滑块失败')
                    # await asyncio.sleep(200)
                    await self.page.goto('https://login.aliexpress.com')
                    await self.check_login(shop_url)
            url_list = await self.page.xpath('//a[@class="pic-rind"]/@href')
            for i, url in enumerate(url_list):
                url = await self.page.evaluate('(url) => url.textContent', url)
                if 'https:' not in url:
                    url = f'https:{url}'
                    self.redis_conn.rpush('aliexpress_url', url)
            try:
                next_page = await self.page.querySelectorEval('a[class=ui-pagination-next]', 'node => node.href')
                await asyncio.sleep(5)
                if next_page:
                    await self.shop_list(next_page)
            except pyppeteer.errors.ElementHandleError as e:
                next_page = await self.page.xpath('//span[@class="ui-pagination-next ui-pagination-disabled"]')
                if next_page:
                    logger.info(f'本店铺采集结束======={shop_url}')
        except Exception as e:
            self.redis_conn.rpush('aliexpress_url', shop_url)
            logger.error(f'打开店铺url失败========{shop_url}')

    async def check_login(self, shop_url):
        # 如果存在登录按钮，需要登录
        # login_button = await self.page.xpath('//button[@class="fm-button"]')
        # 获取当前页url
        cur_url = self.page.url
        # 如果当前链接跳转到登录页，就走登录逻辑
        if 'login.aliexpress.com' in cur_url:
            # 已登录状态，只需点击登录即可
            logined_ele = await self.page.xpath('//div[@class="fm-logined"]')
            if not logined_ele:
                # 输入用户名
                await self.page.type('#fm-login-id', 'haijun0425@126.com', {'delay': random.randint(100, 151) - 50})
                # 输入密码
                await self.page.type('#fm-login-password', 'haijun19840422@', {'delay': random.randint(100, 151)})
                await asyncio.sleep(random.random() + 2)
                # 获取滑块元素
                slider = await self.page.xpath('//div[@id="nocaptcha-password" and @style="display: block;"]')
                if slider:
                    print('进入登录页滑块')
                    # 移动滑块
                    flag = await self.mouse_slider()
                    if not flag:
                        print('滑动滑块失败')
                        # await asyncio.sleep(200)
                        await self.page.goto('https://login.aliexpress.com')
                        await self.check_login(shop_url)
                else:
                    print('没滑块')
                await self.page.goto(shop_url)
            # 点击登录
            await self.page.click('.fm-button')
            print("登录成功")
            await asyncio.sleep(random.random() + 0.5)

    async def main(self, shop_url):
        """
        登陆
        """
        try:
            # 初始化浏览器
            await self._init()
            # 打开店铺
            await self.page.goto(shop_url)
            # 注入js
            await self._injection_js()
            await self.shop_list(shop_url)
            time.sleep(30)
            await self.browser.close()
        except Exception as e:
            self.redis_conn.rpush('aliexpress_url', shop_url)

    def run_login(self):
        shop_url = 'https://crossten.aliexpress.com/store/615649/search/1.html?spm=a2g0o.store_pc_allProduct.8148361.8.245922a1mMjaI3&origin=n&SortType=bestmatch_sort'
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(self.main(shop_url))
        loop.run_until_complete(task)


def login_ali():
    LoginAli().run_login()


if __name__ == '__main__':
    login_ali()
