# -*- coding: utf-8 -*-
# @Time    : 2021/7/26 15:50
# @Author  : Haijun
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


def Proxies():
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"
    # 代理隧道验证信息
    proxyServer = "http://" + proxyHost + ":" + proxyPort

    return proxyServer


def Authens():
    proxyUser = settings.PROXY_USER2
    proxyPass = settings.PROXY_PWD2
    authen = {"username": proxyUser, "password": proxyPass}
    return authen


class LoginAli(object):
    """
    登录
    """
    pyppeteer.DEBUG = True
    page = None
    base_path = os.getcwd()
    user_data_dir = os.path.join(base_path, 'user_data_dir')
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

        # await self.page.evaluate(js1)
        # # await self.page.evaluate(js2)
        # await self.page.evaluate(js3)
        # await self.page.evaluate(js4)
        # await self.page.evaluate(js5)

    async def _init(self):
        """初始化浏览器
        """
        self.browser = await pyppeteer.launch({'headless': True,  # headless=True 启动无头模式
                                               'userDataDir': self.user_data_dir,
                                               'args': [
                                                   # '--window-size={1300},{600}'
                                                   # '--disable-extensions',
                                                   # '--hide-scrollbars',
                                                   # '--disable-bundled-ppapi-flash',
                                                   # '--mute-audio',
                                                   # '--no-sandbox',
                                                   # '--disable-setuid-sandbox',
                                                   # '--disable-gpu',
                                                   # '--disable-infobars'
                                                   '--no-sandbox',
                                                   # "--proxy-server=" + Proxies(),  # --proxy-server 启动代理
                                               ],
                                               # 'dumpio': True,
                                               })

        self.page = await self.browser.newPage()
        await self.page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                              '{ webdriver:{ get: () => undefined } }) }')
        await self.page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                              '{ appVersion:{ get: () => 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 } }) }')

        # 禁止加载JavaScript，可提高加载速度，视情况确定True/False，
        # await self.page.setJavaScriptEnabled(enabled=False)
        # 设置user agent
        await self.page.setUserAgent(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36')
        # await browser.createIncognitoBrowserContext()
        # 隧道类型代理
        # await self.page.authenticate(Authens())
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
        # 模拟浏览器中，滑块在一个iframe中
        frame = self.page.frames
        if frame:
            iframe = frame[1]
            try:
                print('鼠标移到滑块')
                await iframe.hover('#nc_1_n1z')
                # 鼠标按下按钮
                print('按下按钮')
                await self.page.mouse.down()
                # 移动鼠标
                print('移动鼠标')
                await self.page.mouse.move(2000, 0, {'steps': 30})
                # 松开鼠标
                print('松开鼠标')
                await self.page.mouse.up()
                await asyncio.sleep(1)
            except Exception as e:
                print(e, '      :错误')
                return None
            else:
                await asyncio.sleep(1)
                # 获取元素内容，存在说明滑块失败
                slider_again = await iframe.xpath('//span[@class="nc-lang-cnt"]')
                if slider_again:
                    await self.check_login()
                else:
                    print('验证通过')
                    return True

    async def shop_list(self, shop_url, flag=True):
        try:
            await self.page.goto(shop_url)
            url_list = await self.page.xpath('//a[@class="pic-rind"]/@href')
            print(f'url list========={len(url_list)}')
            if url_list:
                for i, url in enumerate(url_list):
                    url = await self.page.evaluate('(url) => url.textContent', url)
                    if 'https:' not in url:
                        url = f'https:{url}'
                        self.redis_conn.rpush('aliexpress_url', url)
                # 滚动到浏览器底部
                await self.page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
                try:
                    next_page = await self.page.querySelectorEval('a[class=ui-pagination-next]', 'node => node.href')
                    if next_page:
                        logger.info(f'下一页==={next_page}')
                        await asyncio.sleep(15)
                        await self.shop_list(next_page)
                except pyppeteer.errors.ElementHandleError as e:
                    next_page = await self.page.xpath('//span[@class="ui-pagination-next ui-pagination-disabled"]')
                    if next_page:
                        logger.info(f'本店铺采集结束======={shop_url}')
            else:
                # 出现了滑块，重新登录
                await self.page.screenshot(path='./apps/aliexpress/test_screenshot5.png')
                print(f'出现了滑块，重新登录')
                await self.check_login()
                await self.shop_list(shop_url, False)
        except Exception as e:
            self.redis_conn.rpush('aliexpress_shop', shop_url)
            logger.error(f'打开店铺url失败========{shop_url}==={e}')

    async def check_email(self):
        '''
        输入邮箱或者手机验证码
        '''
        email_ele = self.page.xpath('//div[@class="fm-dialog-content"]')
        if email_ele:
            frame = self.page.frames
            if frame:
                iframe = frame[1]
                _check_code = iframe.xpath('//div[@class="checkcode-warp"]')
                if _check_code:
                    check_code = input(f'请输入邮箱或手机验证码：')
                    await iframe.type('#J_Checkcode', check_code, {'delay': random.randint(100, 151) - 50})
                    # await self.page.click('#J_GetCode_Email') 重新获取验证码
                    await iframe.click('button[type="submit"]')

    async def input_user_pwd(self):
        '''
        用户名，密码输入
        '''
        print('输入用户名')
        await self.page.type('#fm-login-id', 'haijun0425@126.com', {'delay': random.randint(100, 151) - 50})
        # 输入密码
        await self.page.type('#fm-login-password', 'haijun19840422@', {'delay': random.randint(100, 151)})
        print('输入密码')
        await asyncio.sleep(random.random() + 6)
        # 获取滑块元素
        await self.slider()

    async def check_login(self):
        await self.page.goto('https://login.aliexpress.com')
        # 已登录状态，只需点击登录即可
        logined_ele = await self.page.xpath('//div[@class="fm-logined"]')
        if not logined_ele:
            # 输入用户名
            await self.input_user_pwd()
        # 点击登录
        await asyncio.sleep(10)
        await self.page.screenshot(path='./apps/aliexpress/test_screenshot1.png')
        print("点击登录")
        await self.page.click('.fm-button')
        await asyncio.sleep(10)
        cur_url2 = self.page.url
        if 'login.aliexpress' in cur_url2:
            # 有可能又回到登录页面
            print('重新登录')
            await self.page.screenshot(path='./apps/aliexpress/test_screenshot4.png')
            await self.input_user_pwd()
            await self.page.click('.fm-button')
        await asyncio.sleep(20)
        await self.page.screenshot(path='./apps/aliexpress/test_screenshot2.png')
        # await self.page.goto(shop_url)
        # await self.check_email()
        # cookies = await self._get_cookie()
        await self.page.screenshot(path='./apps/aliexpress/test_screenshot3.png')
        # print(cookies)
        await asyncio.sleep(random.random() + 0.5)

    async def slider(self):
        slider_ele = await self.page.xpath('//iframe[@id="baxia-dialog-content"]')
        print(f'是否存在滑块===={slider_ele}')
        if slider_ele:
            print('进入登录页滑块')
            # 移动滑块
            flag = await self.mouse_slider()
            if not flag:
                print('滑动滑块失败')
                # await asyncio.sleep(200)
        else:
            print('没滑块')
        time.sleep(3)

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
            await self.browser.close()
        except Exception as e:
            self.redis_conn.rpush('aliexpress_shop', shop_url)
            await self.browser.close()

    def run_login(self, url):
        logger.info(f'开始采集=={url}')
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(self.main(url))
        loop.run_until_complete(task)
