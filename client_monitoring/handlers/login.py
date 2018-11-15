# encoding:utf-8

"""
登录页面
"""
# from client_monitoring.models.check_login import CheckLogin

from base_handler import BaseHandler
from client_monitoring.models.check_login import CheckLogin


class LoginHandler(BaseHandler):
    """首页控制"""
    def get(self):
        self.render('login.html', flag=0)

    def post(self):

        self.clear_all_cookies()
        username = self.get_argument('username')
        password = self.get_argument('password')
        user_id,user_name = CheckLogin().check_login(username, password)
        if user_id:
            self.set_secure_cookie('user_id', user_id)
            self.set_secure_cookie('user_name',user_name)
            self.redirect('/')
            return 
        else:
            self.render('login.html',flag=1)