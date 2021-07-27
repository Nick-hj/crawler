# -*- coding: utf-8 -*-
# @Time    : 2020/8/24 13:01
# @Author  : Haijun

from pathlib import Path
from typing import Optional
from dynaconf import settings, loaders
from lib.base_fun import logger

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 4
REDIS_PASSWD = ""
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWD = "root"
MYSQL_DATABASE = ""
MYSQL_PORT = 3306

DEFAULT_PATH = "settings.toml"
BASE_SETTINGS = {
    "HOME_DIR": str(Path().absolute()),
    "REDIS": {
        "HOST": REDIS_HOST,
        "PORT": REDIS_PORT,
        "DB": REDIS_DB,
        "PASSWD": REDIS_PASSWD
    },
    "MYSQL": {
        "HOST": MYSQL_HOST,
        "USER": MYSQL_USER,
        "PASSWD": MYSQL_PASSWD,
        "DATABASE": MYSQL_DATABASE,
        "PORT": MYSQL_PORT
    },
    "WISH": {
        'USERNAME': '',
        'PASSWD': '',
        'WISH_COOKIE': 'wish_cookie',
        'WISH_XSRF': 'wish_xsrf'
    },
    'SAVE_GOODS_TO_REDIS_KEY': 'save_goods_data',  # 保存数据到redis的key
    'AE_LOGIN_COOKIE_KEY':'ae_login_cookie',
    'PROXY_USER': '',  # 代理用户名
    'PROXY_PWD': '',  # 代理密码
    "AE_COOKIE": 'ali_apache_id=11.180.122.25.1598942647381.190789.8; _fbp=fb.1.1603270072511.1320845565; e_id=pt70; af_ss_a=1; traffic_se_co=%7B%7D; _bl_uid=qIkUqm7d0qU1vR9InfXF2m89dLyb; aep_common_f=35O20gfseafTaPCBD7IoWqr6OVmNtxSac+39NoCzQGaEFlkMeeY39w==; __utmz=3375712.1617094592.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=3375712.1468672364.1598942650.1617094592.1617692399.2; af_ss_b=1; aeu_cid=6b5094abd64042049a4e1bf9c8722441-1619691082317-08706-_2aeOzjW; intl_locale=en_US; acs_usuc_t=x_csrf=1517oq2c_rhtz&acs_rt=d4528ffbe57a4c459a8d549f39ad2f55; xlly_s=1; cna=hm9PGQa2sUQCAXeIIHk+vVaW; _gid=GA1.2.203447915.1624950473; _gcl_au=1.1.936047996.1624950474; XSRF-TOKEN=d8695277-ca9d-41ee-8961-9ea0918ffc51; JSESSIONID=EC08916A295DF6BF42EC79D4F83A065E; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%091005002444927256%0932831852169%094000435091773%091005002192604260%091005002079753103%091005002345980943%091005002007845400%091005002007845400; _mle_tmp_enc0=Ey%2Fp8LswzxA3J47VsqxI%2B55ri0i40%2B9V8foPq866Qg9PfWqjG%2BSLzzJJ5%2Fxj8Kr9Z5f1YGrmgPbDo4A5Q%2FRRjGO5HXNjS%2BwuBF7R3w8hjATeIgliJ7WmJpekk2ilFj1y; _m_h5_tk=a5cedcb6cc9acab1959b3604487c3ce6_1624962597116; _m_h5_tk_enc=d648dce9bdf6a0ab919ad7f72440d823; _gat=1; havana_tgc=eyJjcmVhdGVUaW1lIjoxNjI0OTYwOTcxOTkwLCJsYW5nIjoiZW5fVVMiLCJwYXRpYWxUZ2MiOnsiYWNjSW5mb3MiOnsiMTMiOnsiYWNjZXNzVHlwZSI6MSwibWVtYmVySWQiOjIyMDEyMTA0MDY5NzEsInRndElkIjoiMXlSdGpVenFIeHIyeTJWdVlhWkJBYUEifX19fQ; _hvn_login=13; xman_us_t=x_lid=cn258600111mbaae&sign=y&rmb_pp=haijun0425@126.com&x_user=y6YT8bNTm/CsebLnKKB5oyfAHQsZn5tN80DzCN/7ETY=&ctoken=93if06tilqfn&need_popup=y&l_source=aliexpress; aep_usuc_t=ber_l=A1; bx_s_t=ho1S0T8VnZrLjwC4Z08Soss5+zdKLyAnoE6D1ovhIyOfRGKQ8mKFKtZr3MPoIIMeSfAf2E18BrBEGNSrGhbrZUO7szJQLIW5CaZEig8rWp4=; xman_f=KHAagYKfq6QkHflO72eFbigtc3xe1jj+gtO6q3CL/XDX0la9/HYDlgWcomo+cIdtDj1EzX2K6aySv3pxWyJWxTID4v8WWTXNWLuo/zMEu4iCc0zTlyoV8GoZysgcBVdztYbjnNC3Az8Ha9zLsF6DO+2fE9vVHuS6zamVO1VgKk/Rz1MbCHfAhmRmyIhiH6MA0DYT59Z2ogJGJ1YuHXTa4fYzgCK06IR0prGDuAKDIeI1AD5U4hTzzMuAdTSUF1gZcpXApbwaESdJ5bvJyzSzmXL4eeMdY6/EQGRFGwxF3kelsySDCOO7nqCvPN1PiEjkO/dm/t6fIT2WcUuYd+UNQc2JFZJgolvWY2760NHcaGhFZ8GHbn81AF3q/+GeY0sVl69rvsvciihEFkmVxPJDxkiFkH1aFYN1idmC35VklGI8q0jW5MGHyg==; xman_us_f=zero_order=y&x_locale=en_US&x_l=0&last_popup_time=1599737455866&x_user=CN|haijun|yu|ifm|1859821111&no_popup_today=n&x_lid=cn258600111mbaae&x_c_chg=0&x_c_synced=0&x_as_i=%7B%22aeuCID%22%3A%226b5094abd64042049a4e1bf9c8722441-1619691082317-08706-_2aeOzjW%22%2C%22affiliateKey%22%3A%22_2aeOzjW%22%2C%22channel%22%3A%22AFFILIATE%22%2C%22cv%22%3A%227%22%2C%22isCookieCache%22%3A%22N%22%2C%22ms%22%3A%220%22%2C%22pid%22%3A%22908725594%22%2C%22tagtime%22%3A1619691082317%7D&acs_rt=cf72780120e64a0ea51c1210227ab768; aep_usuc_f=site=glo&c_tp=USD&x_alimid=1859821111&isb=y&region=HK&b_locale=en_US; ali_apache_track=ms=|mt=1|mid=cn258600111mbaae; ali_apache_tracktmp=W_signed=Y; intl_common_forever=H8qNVjji5E6/58aOVQG12vWggQ0GGWff6wwSUxuZ81YL0EknAie4rg==; _ga_VED1YSGNC7=GS1.1.1624959980.20.1.1624960979.0; _ga=GA1.1.1468672364.1598942650; tfstk=cxfcB3iE2tJXwB9ldSOfo9iNA71cZC02Y1WNa11JUPuOcZfPiODrL7nTreIc6A1..; l=eBSlmJQqORhyHactBOfwhurza77thIRAguPzaNbMiOCPO3fW7GHhW69ZPJ8XCnGVh6owR3-IkQOzBeYBqIcTIM3CN6PrVDkmn; isg=BBsbJgYI_3j25zwbEDBoPBW8qn-F8C_yudlBEw1YkZo87DvOlcLYQ4BuhkziTIfq; xman_t=0rVSg6TIUqJnJbpxrwHK6zWBHc/9d3raJpohL2u+1qi6v12N44VCWja6d6Md55GDTkh0hW62IA1XvBuF4V3JhZ1JS1fJzCj195GIq1udJgVScr5HQwGMEL6Hjs6HY5uHWVY2gRXDnPdJcRzD56OcckV2aJCcbNmu304GumwmTEz0VX76fY8XzjiQXvABZCOIhHlK6m63iMUYeN4SbO6Z0Mf1g5GEY+iRmntulraWngsPoUTeDRM1MsjQT5GGyWIHfVWn6LS8WJBaD5aWLagOWfwGNUZ3O022rEd/hqr5AxJeQ+fm4NAmgBnuqG7sm97Ufe7M7Ta8DjPt7SLRaiQgpS16IWCtzTGVORy0uwkFUmQPjKNcBKvFGziGIAKlEgNftQ7RimpIFQa8ripx95mkLoTMUgN0aEiFNHfHn0/O9rSXvLGbKzlmtw1OtiX8vNr+gcJCZHInN45kQ/EIRB51TPhwZgekMvT0DPKexQI/591yqEd+h3vY6ZSH/B0y8a8aWa4eQn4K/7L3kX3IpA2/5e/DPerkiDagUvyvXyjZSqLHPykO+SGmJKLYIWSmpAmRCXTcuvhZI2tq5lTqf9IZd5z7MaUY/OsS7w4SWCtcI7wkYLmT8XRfaLP33CWK2A6fIKJ93hn+0vMpjy++g+bEyQ==',
    'SLEEP_TIME': 5  # 休眠时间
}


def load_or_create_settings(path: Optional[str] = ''):
    """
    创建或加载配置文件
    """
    path = path or DEFAULT_PATH
    if not Path(path).exists():
        default_settings_path = str(Path.cwd() / Path(DEFAULT_PATH))
        logger.info(
            f'没有发现配置文件 "{Path(path).absolute()}". '
            f"创建默认配置文件: {default_settings_path}",
        )
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        loaders.write(default_settings_path, BASE_SETTINGS, env="default")
    settings.load_file(path=path)
    logger.info("配置文件加载成功")
