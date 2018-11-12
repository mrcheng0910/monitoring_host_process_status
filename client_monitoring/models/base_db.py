# encoding:utf-8
"""
操作数据库基础类
"""
import torndb

class BaseDb(object):

    def __init__(self):
        self.db = torndb.Connection(
            host="10.245.146.44",
            database = "monitoring_host_process",
            user = "root",
            password = "platform",
            charset = "utf8",
            time_zone = "+8:00",
            connect_timeout = 30
        )