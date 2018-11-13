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
from client_monitoring.models.user_db import UserDb


class UserIndexHandler(BaseHandler):
    """主机首页控制"""

    @tornado.web.authenticated
    def get(self):
        if self.certify_user():
            user_db = UserDb()
            user_id = self.get_current_user()
            email, flag,login_name,user_name = user_db.get_user_info(user_id)
            if flag == '1':
                user_type = "管理员"
            elif flag == '0':
                user_type = "普通用户"
            else:
                user_type = "其他用户"
            self.render(
                'user_info.html',
                user_name = user_name,
                email = email,
                user_type = user_type,
                login_name = login_name
            )


class EditUserInfoHandler(BaseHandler):
    """主机连接测试"""
    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return
        user_id = self.get_current_user()
        user_name = self.get_argument('user_name', None).strip()
        email = self.get_argument('email', None)
        user_db = UserDb()
        result = user_db.save_user_info(user_name,email,user_id)
        self.write({'result':result})


class EditPwdHandler(BaseHandler):
    """主机连接测试"""
    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return
        user_id = self.get_current_user()
        old_pwd = self.get_argument('old_pwd', None).strip()
        new_pwd = self.get_argument('new_pwd', None).strip()
        user_db = UserDb()
        pwd_db = user_db.get_user_pwd(user_id)
        if old_pwd == pwd_db:
            result = user_db.save_new_pwd(new_pwd,user_id)
        else:
            result = "密码不正确"
        self.write({'result':result})