# encoding:utf-8
"""
录入监控远程主机信息
"""

import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

import tornado.web
import paramiko
import socket
from base_handler import BaseHandler
from client_monitoring.models.host_db import HostDb


class InputHostIndexHandler(BaseHandler):
    """录入主机首页控制"""

    @tornado.web.authenticated
    def get(self):
        if self.certify_user():
            self.render('input_host.html')


class TestHostConnectionHandler(BaseHandler):
    """主机连接测试"""

    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return
        host_ip = self.get_argument('host_ip', None).strip()
        port = self.get_argument('port', None)
        login_name = self.get_argument('login_name', None).strip()
        pwd = self.get_argument('pwd', None).strip()
        error, error_info = self.test_host(host_ip, int(port), login_name, pwd)
        if error:
            self.write({'result': '服务器出错:'+str(error_info)})
        else:
            self.write({'result': '连接成功'})

    def test_host(self, host_ip, port, login_name, pwd):
        host_error = False
        client = paramiko.SSHClient()  # 创建客户端
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(host_ip, port, login_name, pwd, timeout=10)
        except paramiko.BadHostKeyException, e:
            host_error = e
        except paramiko.AuthenticationException, e:
            host_error = e
        except paramiko.SSHException, e:
            host_error = e
        except socket.error, e:
            host_error = e
        if host_error:
            return True, host_error  # 失败以及错误信息
        else:
            return False, 'success'  # 成功


class InputHostSaveHandler(BaseHandler):
    """主机信息保存"""

    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return
        user_id = self.get_current_user()
        host_ip = self.get_argument('host_ip', None).strip()
        port = self.get_argument('port', None)
        login_name = self.get_argument('login_name', None).strip()
        pwd = self.get_argument('pwd', None).strip()
        comment = self.get_argument('comment', None).strip()

        host_id = self.generate_host_id(user_id,host_ip)

        print host_id
        host_db = HostDb()
        save = host_db.save_host_info(host_id, user_id, host_ip, login_name, port, pwd, comment)
        self.write({'result': save})

    def generate_host_id(self, user_id, host_ip):
        """根据用户id、主机IP和登录名称生成主机id"""
        host_id = abs(hash(user_id + host_ip)) % (10 ** 8)
        return host_id



