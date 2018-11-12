# encoding:utf-8

"""
功能：处理主机相关数据库操作
"""
import torndb
from base_db import BaseDb
import base64


class HostDb(BaseDb):
    def __init__(self):
        BaseDb.__init__(self)  # 执行父类

    def save_host_info(self, host_id, user_id, host_ip, login_name, port, pwd, comment):
        """插入主机信息"""
        sql = 'INSERT INTO host_info (host_id, user_id,host_ip,login_name,port,pwd,comment) VALUES ("%s","%s","%s","%s","%s","%s","%s")'
        host_ip = base64.encodestring(host_ip).strip()
        login_name = base64.encodestring(login_name).strip()
        port = base64.encodestring(port).strip()
        pwd = base64.encodestring(pwd).strip()
        try:
            self.db.insert(sql % ( host_id, user_id, host_ip, login_name,port, pwd, comment.strip()))
            # self.db.close()
            return "保存成功"
        except torndb.IntegrityError:  # 已存在该结果
            # self.db.close()
            return "保存失败，数据库已有该主机信息"

    def get_user_exist_host(self,user_id):
        """获取用户已有主机ip地址"""

        hosts = [['请选择或新建主机',0]]  # 第一选项
        sql = 'select host_id, host_ip from host_info WHERE user_id = "%s"'

        result = self.db.query(sql % user_id)
        for i in result:
            try:  # 测试数据，因为之前录入的主机为进行加密
                hosts.append([base64.decodestring(i['host_ip']),i['host_id']])
            except:
                continue
        return hosts

    def get_user_host_info(self, user_id, host_ip):
        """获取用户主机的登录信息"""

        sql = 'select login_name, port, pwd from host_info WHERE user_id = "%s" AND host_ip ="%s"'
        host_ip = base64.encodestring(host_ip).strip()  # 先将ip加密，数据库存储的为加密信息,要strip（），确认数据无疑
        result = self.db.query(sql % (user_id, host_ip))
        result = result[0]
        # 解密
        login_name = base64.decodestring(result['login_name'])
        port = base64.decodestring(result['port'])
        pwd = base64.decodestring(result['pwd'])
        host_ip = base64.decodestring(host_ip)
        return (host_ip, port, login_name, pwd)























