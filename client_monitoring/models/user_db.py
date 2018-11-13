# encoding:utf-8

"""
用户管理功能
"""
import torndb
from base_db import BaseDb
import base64


class UserDb(BaseDb):
    def __init__(self):
        BaseDb.__init__(self)  # 执行父类

    def get_user_info(self,user_id):
        """得到用户的邮箱和内容"""
        sql = 'select email, flag,user,user_name from user_account where user_id = "%s"' % user_id
        result = self.db.query(sql)
        return  result[0].email, result[0].flag,result[0].user,result[0].user_name

    def save_user_info(self,user_name,email,user_id):
        """保存修改后的用户信息"""
        sql = 'update user_account set user_name="%s",email="%s" where user_id="%s"'
        try:
            self.db.execute(sql%(user_name,email,user_id))
            return "更改成功"
        except:
            return "更改失败"


    def get_user_pwd(self,user_id):
        """得到用户的邮箱和内容"""
        sql = 'select pwd from user_account where user_id = "%s"' % user_id
        result = self.db.query(sql)
        return  result[0].pwd

    def save_new_pwd(self,new_pwd,user_id):
        """保存修改后的用户信息"""
        sql = 'update user_account set pwd="%s" where user_id="%s"'
        try:
            self.db.execute(sql%(new_pwd,user_id))
            return "更改成功"
        except:
            return "更改失败"


    def add_new_user(self,user_id,user_name,user,pwd,email,flag):
        """保存修改后的用户信息"""
        sql = 'insert into user_account (user_id,user_name,user,pwd,email,flag) value("%s","%s","%s","%s","%s","%s")'
        try:
            self.db.execute(sql%(user_id,user_name,user,pwd,email,flag))
            return "保存成功"
        except torndb.IntegrityError:
            return "保存失败，已有该注册用户信息"










