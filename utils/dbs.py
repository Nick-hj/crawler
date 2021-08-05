# -*- coding: utf-8 -*-
# @Time    : 2021/8/5 16:06
# @Author  : Haijun
from pymysql import Connect
from pymysql.cursors import DictCursor


class DBConn(object):
    def __init__(self):
        self.conn = Connect(
            host='172.31.0.155',
            db='voghion-comment',
            user='prod',
            password='Stars@2019',
            courseclass=DictCursor
        )

    def __enter__(self):
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_value, trace):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        return True

    def close(self):
        try:
            self.conn.close()
        except:
            pass

    def query(self, table, *field, where=None, args=None):
        sql = 'select %s from %s' % (','.join(field), table)
        if where:
            sql += ' where ' + where
