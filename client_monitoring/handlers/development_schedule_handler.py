# encoding:utf-8
"""
输入监控远程主机信息
"""

import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

import tornado.web
import paramiko
import socket
from base_handler import BaseHandler
# from client_monitoring.models.host_db import HostDb


class ScheduleHandler(BaseHandler):
    """进程首页控制"""

    @tornado.web.authenticated
    def get(self):
        if self.certify_user():
            self.render('development_schedule.html')
