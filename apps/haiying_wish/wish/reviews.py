# -*- coding: utf-8 -*-
# @Time    : 2021/7/20 10:50
# @Author  : Haijun
import json

'''
https://haiyingshuju.com/wish_2.0/product/detail/sku
post:
data:{"index":1,"pageSize":50,"pid":"5c24229a62d5c42244032782","orderColumn":"","sort":""}

'''

import requests

url = 'https://www.wish.com/api/product-ratings/get'
data = {
    'product_id': '558a6a0e84c2e807b76f923d',
    'start': 0,
    'count': 50,
    'request_count': 1,
}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',
    'x-xsrftoken': '2|aaa565d2|7d23f3bba70d6296c1e1b69251775777|1626773936',
    # 'cookie': 'visitor_id=19a53d15a09b4096ad4d4f0469ce13a7; tatari-session-cookie=e5934199-0a0d-39d6-9727-d192537bc499; __ssid=556b8d5b45f1d1c2b700f30258fb2a6; __stripe_mid=88ee989b-8933-40e9-8cd5-66a1f908317b8f7ed2; _pin_unauth=dWlkPU1EUTFOVE16T1dVdE5UZ3dZaTAwWmprNExXSmlOamN0TmpGbE1qRTJOV0l6TjJZMw; G_ENABLED_IDPS=google; _fbp=fb.1.1626252903523.1770009377; authentication_id=d6101e62950b3588a45b497b0e43279a; _dcmn_p=x6VeY2lkPXVXSFBNMkR6MU1QeF95RjJBQk0; _dcmn_p=x6VeY2lkPXVXSFBNMkR6MU1QeF95RjJBQk0; rskxRunCookie=0; rCookie=f0aeiu1l57m1c5q9wiutw3kr8yw9ke; _ga=GA1.2.1279326244.1626252829; _gid=GA1.2.1996676516.1626624817; _ga_S8FFZTJ4RL=GS1.1.1626628281.2.0.1626628281.0; sweeper_session="2|1:0|10:1626686427|15:sweeper_session|84:NjgxZDE4NjMtZjE3Ny00YTFkLWFiZWItZjMyYzYxZDc0NGRmMjAyMS0wNy0xOSAwOToyMDoyMi43NzEyMzQ=|7a541315170db2e40865fae014a2fdf834ee8946f82a56ea3efbd16c26f75783"; sessionRefreshed_60f3d26d94fdf1d17eb88a63=true; _dcmn_p=x6VeY2lkPXVXSFBNMkR6MU1QeF95RjJBQk0; lastRskxRun=1626688513122; _xsrf=2|8b2f7b1b|cee72bc45e2c5fc38923f4af15071fe8|1626749448; vendor_user_tracker=a2246ea348a1adae09f31e014ce6ef72664ead8744a268b9f2cde3bd6bdef96b; bsid=a3e60e1ab49082c6b26f781f9609225f; _timezone=8; _is_desktop=true; sweeper_uuid=564ad85080bc4dee9b0a527cf583d3f5; _uetsid=0750ed20e79611eb97ea616a5c45d489; _uetvid=02c9c510e48111ebbd9e89268d36dcf9; IR_gbd=wish.com; IR_12396=1626749452164%7C0%7C1626749452164%7C%7C; IR_PI=807ae331-3513-11eb-99e3-42010a246309%7C1626835852164; _tq_id.TV-09458190-1.2013=c1260b1a963859e2.1626686430.0.1626749455..'
    'cookie': '_xsrf=2|aaa565d2|7d23f3bba70d6296c1e1b69251775777|1626773936'
}
res = requests.post(url=url, data=data, headers=headers)
print(res.status_code)
print(res.text)
