# encoding:utf-8

"""
Base handler
"""

import tornado.web

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        """
        获取用户标识
        :return:
        """
        user_id = self.get_secure_cookie("user_id")
        return user_id
    def get_current_user_name(self):
        user_name = self.get_secure_cookie("user_name")
        return user_name

    def certify_user(self):
        """
        认证用户
        :return:
        """
        if not self.get_current_user():
            self.redirect('/login')
            return False
        else:
            return True