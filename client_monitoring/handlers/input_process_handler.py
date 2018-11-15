# encoding:utf-8
"""
录入监测进程管理
"""

import tornado.web
import json

# 加载中文
import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

import paramiko
import socket
from datetime import datetime
from client_monitoring.models.host_db import HostDb
from client_monitoring.models.process_db import ProcessDb
from base_handler import BaseHandler


class InputProcessHandler(BaseHandler):
    """加载进程录入首页"""

    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return
        self.render( 'input_process.html')


class GetUserHostHandler(BaseHandler):
    """获取用户已有主机信息"""

    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return
        host_db = HostDb()
        user_id = self.get_current_user()
        # user_id = '1321313' # 用户id待读取
        hosts = host_db.get_user_exist_host(user_id)
        self.write(json.dumps(hosts))


class GetProcessInfoHandler(BaseHandler):
    """获取进程的详细信息"""

    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return
        host_db = HostDb()
        user_id = self.get_current_user()
        host_ip = self.get_argument('host_ip', None)    # 注意，网页已在客户端进行验证，保证数据得正确性
        pid_name = self.get_argument('process_value', None)
        host = host_db.get_user_host_info(user_id, host_ip)   # 根据用户id和主机地址，获取主机登录信息
        processes_status,processes_route = self.connect_host(host, pid_name)  # 连接远程主机，根据进程id或者名称获取其运行信息
        self.write(json.dumps([processes_status, processes_route]))

    def connect_host(self, host, pid_name):
        """连接主机和获取信息"""
        host_error = False     # 主机状态异常
        hostname, port, username, password = host
        client = paramiko.SSHClient()  # 创建客户端
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname, port, username, password, timeout=3)
        except paramiko.BadHostKeyException, e:
            host_error = e
        except paramiko.AuthenticationException, e:
            host_error = e
        except paramiko.SSHException, e:
            host_error = e
        except socket.error, e:
            host_error = e
        if host_error:
            return host_error
        processes_status, processes_id = self.fetch_process_status(client, pid_name)
        processes_route = self.fetch_process_route(client, processes_id)
        client.close() # 关闭主机
        return processes_status, processes_route

    def fetch_process_status(self,client, pid_name):
        """获取进程状态"""
        command = 'ps -ef|grep "%s" -a |grep -v "grep" -a'  # 获取进程状态命令
        stdin, stdout, stderr = client.exec_command(command % pid_name)  # 执行bash命令
        raw_processes_status = stdout.read()
        error = stderr.read()  # 判断stderr输出是否为空，为空则打印执行结果，不为空打印报错信息
        processes_status, processes_id = self.extract_process_info(raw_processes_status)
        return processes_status,processes_id

    def extract_process_info(self, raw_processes_status):
        """解析出进程的状态信息"""

        if not raw_processes_status:
            return ["未查到该进程状态信息,请重新检查！"], []
        processes_id = []
        processes_status = []
        raw_processes_status = raw_processes_status.strip().split('\n')
        for i in raw_processes_status:
            process_status = i.strip().split(' ')  # 分割成列表
            # 去除列表中多余的空值
            while '' in process_status:
                process_status.remove('')
            processes_id.append(process_status[1])
            process_status = process_status[1] + ' '+ process_status[2] + ' ' + ' '.join(process_status[7:])
            processes_status.append(process_status)
        return processes_status, processes_id

    def fetch_process_route(self, client, processes_id):
        """获取进程运行路径"""
        if not processes_id:
            return ""
        processes_id = ' '.join(processes_id)
        command = 'pwdx ' + processes_id
        stdin, stdout, stderr = client.exec_command(command)  # 执行bash命令
        raw_processes_route = stdout.read()
        error = stderr.read() # 判断stderr输出是否为空，为空则打印执行结果，不为空打印报错信息
        processes_route = self.extract_process_route(raw_processes_route)
        return processes_route

    def extract_process_route(self, raw_processes_route):
        """解析出进程的状态信息"""
        pids,routes = [], []
        for r in raw_processes_route.strip().split('\n'):
            process_info = r.strip().split(' ')
            pid = process_info[0].replace(':','')
            pids.append(pid)
            try:
                routes.append(process_info[1].strip())
            except:
                routes.append("")
        return [pids, routes]


class ProcessSaveHandler(BaseHandler):
    """进程信息保存"""

    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return
        host_id = self.get_argument('host_id', None).strip()
        pid = self.get_argument('pid', None).strip()
        shell = self.get_argument('shell', None).strip()
        cmd = self.get_argument('cmd', None).strip()
        interval = self.get_argument('time', None).strip()
        log_route = self.get_argument('log_route', None).strip()
        log_name = self.get_argument('log_name', None).strip()
        code_route = self.get_argument('code_route', None).strip()
        code_name = self.get_argument('code_name', None).strip()
        comment = self.get_argument('comment', None).strip()
        create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        process_id = self.generate_process_id(pid,create_time)
        user_id = self.get_current_user()
        process_info = (process_id, user_id, host_id,code_name,pid,create_time,log_route,code_route,interval, '1', comment,cmd,shell,log_name)
        process_db = ProcessDb()
        save = process_db.save_process_info(process_info)
        self.write({
            'result': save,
            'process_id': process_id
                    })

    def generate_process_id(self, pid, create_time):
        """生成进程id"""
        process_id = abs(hash(pid+ str(create_time)))% (10 ** 8)
        return process_id

