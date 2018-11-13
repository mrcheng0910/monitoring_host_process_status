#! /usr/bin/env python
# -*- coding: utf-8 -*-

from base_db import BaseDb


class CheckLogin(BaseDb):

    def __init__(self):
        BaseDb.__init__ (self)  # 执行父类

    def check_login(self, username, password):
        
        if not username or not password:
            return

        sql = "SELECT user_id, pwd,user_name FROM user_account WHERE user = %s"
        result = self.db.query(sql, username)

        for value in result:
            if value.pwd == password:
                return value.user_id,value.user_name
        else:
            return '',''