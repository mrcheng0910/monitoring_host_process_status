# encoding:utf-8
"""
开发进度展示
"""

import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

import tornado.web
from base_handler import BaseHandler

class ScheduleHandler(BaseHandler):
    """进度首页控制"""

    @tornado.web.authenticated
    def get(self):
        if self.certify_user():
            self.render('development_schedule.html')
