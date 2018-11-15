# encoding:utf-8
"""
主机handler（功能未实现，从进程管理那边复制过来）
"""

import tornado.web
import json
from collections import Counter

# 加载中文
import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

import base64
from client_monitoring.models.process_db import ProcessDb
from client_monitoring.models.host_db import HostDb
from fetch_process_status import connect_host as execute_connect_host
from stop_process_status import connect_host as stop_connect_host
from base_handler import BaseHandler
from read_log import connect_host as read_log_connect
from download_log import connect_host as download_log_connect


class HostIndexHandler(BaseHandler):
    """主机首页控制"""
    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return

        index_db = ProcessDb()
        user_id = self.get_current_user()
        user_process_status = index_db.fetch_user_process(user_id)
        process_status = []
        for i in user_process_status:
            i['host_ip'] = base64.decodestring(i['host_ip'])
            # i['process_id'] = str(i['process_id'])
            process_status.append(i)
            # print type(i['process_id'])
        status_counter = self.format_data(user_process_status)
        self.render(
            'host_index.html',
            host_good_running = status_counter['正常'],
            host_exception_running=status_counter['异常'],
            host_stop_running=status_counter['停止'],
            process_status = process_status
        )


    def format_data(self, user_process_status):
        status_counter = Counter()
        for i in user_process_status:
            status_counter[str(i['status'])] += 1
        return status_counter


class ProcessDetailsHandler(BaseHandler):
    """进程首页控制"""

    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return
        process_id = self.get_argument('process_id', '')
        self.render(
            'process_details.html',
            process_id = process_id
        )


class ProcessDetailsDataHandler(BaseHandler):
    """进程详细页面控制"""
    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return
        proces_id = self.get_argument('process_id',None)
        index_db = ProcessDb()
        user_id = self.get_current_user()
        process_history = index_db.fetch_process(user_id, proces_id)   # 获取进程历史信息
        cpu_history, mem_history,vsz_history,rss_history,log_size_history = self.get_resource_history(process_history)  # 提取出检测的cpu、mem、rss、vsz等历史信息
        # 获取最近进程状态信息，并将主机解析出ip地址
        current_process_status = process_history[0]
        current_process_status['host_ip'] = base64.decodestring(current_process_status['host_ip'])

        data = [current_process_status, cpu_history,mem_history,vsz_history,rss_history,log_size_history]
        self.write(json.dumps(data, default=self._date_handler))

    def get_resource_history(self, process_history):
        """解析处cpu、mem等资源的历史信息"""
        cpu_history, mem_history,vsz_history,rss_history,log_size_history = [], [], [], [],[]

        for i in process_history:
            cpu_history.insert(0, [i['detect_time'], float(i['cpu'])])
            mem_history.insert(0, [i['detect_time'], float(i['mem'])])
            vsz_history.insert(0, [i['detect_time'], int(i['vsz'])/1000])
            rss_history.insert(0, [i['detect_time'], int(i['rss'])/1000])

            log_size = i['log_size']
            if log_size == '-1':
                log_size_history.insert(0,[i['detect_time'],-1])
            elif log_size == '-2':
                log_size_history.insert(0, [i['detect_time'], -2])
            elif log_size == '-3':
                log_size_history.insert(0, [i['detect_time'], -3])
            elif log_size == '0':
                log_size_history.insert(0, [i['detect_time'], 0])
            else:
                if log_size[-1] == 'K':
                    log_size_history.insert(0,[i['detect_time'],round(float(log_size[:-1])/1000,2)])
                elif log_size[-1] == 'G':
                    log_size_history.insert(0, [i['detect_time'], float(log_size[:-1])*1000])
                elif log_size[-1] == 'M':
                    log_size_history.insert(0, [i['detect_time'], float(log_size[:-1])])

        return cpu_history, mem_history,vsz_history,rss_history,log_size_history

    def _date_handler(self, obj):
        """json支持date格式"""
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj


class ExecuteProcessHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return

        host_db = HostDb()
        # user_id = '1321313'  # 待读取
        user_id = self.get_current_user()
        host_ip = self.get_argument('host_ip', None)  # 注意，网页已在客户端进行验证，保证数据得正确性，未加密的ID值
        pid = self.get_argument('pid', None)
        log_route = self.get_argument('log_route', None)
        log_name = self.get_argument('log_name', None)
        process_id = self.get_argument('process_id', None)
        host = host_db.get_user_host_info(user_id, host_ip)  # 根据用户id和主机地址，获取主机登录信息
        cpu, mem, vsz, rss, log_size, status, error_info = execute_connect_host(host,pid,log_route,log_name)  # 连接远程主机，根据进程id或者名称获取其运行信息
        process_db = ProcessDb()
        result = process_db.save_process_status(process_id, cpu, mem, vsz, rss, log_size, status, error_info)
        self.write(json.dumps({'result':result}))


class StopProcessHandler(BaseHandler):
    """停止正在执行的程序"""
    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return

        host_db = HostDb()
        user_id = self.get_current_user()
        host_ip = self.get_argument('host_ip', None)
        pid = self.get_argument('pid', None)
        host = host_db.get_user_host_info(user_id, host_ip)  # 根据用户id和主机地址，获取主机登录信息
        stop_result = stop_connect_host(host,pid)  # 连接远程主机，根据进程id停止运行
        self.write(json.dumps({'result':stop_result}))  # 返回执行结果


class NofocusProcessHandler(BaseHandler):
    """取消关注进程"""
    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return
        process_id = self.get_argument('process_id', None)  # 注意，网页已在客户端进行验证，保证数据得正确性
        process_db = ProcessDb()
        result = process_db.no_focus_process(process_id)   # 更新数据库
        self.write(json.dumps({'result': result}))


class ReadLogHandler(BaseHandler):
    """读取日志功能"""
    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return

        host_db = HostDb()
        user_id = self.get_current_user()
        host_ip = self.get_argument('host_ip', None)
        log_route = self.get_argument('log_route', None)
        log_name = self.get_argument('log_name', None)
        host = host_db.get_user_host_info(user_id, host_ip)  # 根据用户id和主机地址，获取主机登录信息

        stop_result = read_log_connect(host,log_route,log_name)  # 连接远程主机，根据进程id停止运行
        self.write(json.dumps({'result': stop_result}))  # 返回执行结果


class DownloadlogHandler(BaseHandler):
    """读取日志功能
    todo 增加异常处理功能
    """
    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return

        host_db = HostDb()
        user_id = self.get_current_user()
        host_ip = self.get_argument('host_ip', None)
        log_route = self.get_argument('log_route', None)
        log_name = self.get_argument('log_name', None)
        host = host_db.get_user_host_info(user_id, host_ip)  # 根据用户id和主机地址，获取主机登录信息
        result, new_log_name = download_log_connect(host,log_route,log_name)  # 获取日志和日志保存名称
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=%s' % new_log_name)
        self.write(result)
        self.finish()


class SubmitProcessHandler(BaseHandler):
    """提交修改后的进程信息"""
    @tornado.web.authenticated
    def get(self):
        if not self.certify_user():
            return

        process_id = self.get_argument('process_id', None)  # 注意，网页已在客户端进行验证，保证数据得正确性，未加密的ID值
        log_route = self.get_argument('log_route', None)
        code_route = self.get_argument('code_route', None)
        log_name = self.get_argument('log_name', None)
        code_name = self.get_argument('code_name', None)
        shell = self.get_argument('shell', None)
        cmd = self.get_argument('cmd', None)
        interval_time = self.get_argument('interval_time', None)
        indexdb = ProcessDb()
        result = indexdb.update_process(process_id,log_route,code_route,log_name,code_name,shell,cmd,interval_time)
        self.write(json.dumps({'result':result}))
