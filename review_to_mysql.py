# -*- coding: utf-8 -*-
# @Time    : 2021/8/5 17:32
# @Author  : Haijun
from utils.reviews_to_mysql import ReviewsToMyswl
from lib.base_fun import run_single_fun
import redis
from dynaconf import settings


if __name__ == '__main__':
    run_single_fun('aliexpress_reviews', 100, ReviewsToMyswl().main)
