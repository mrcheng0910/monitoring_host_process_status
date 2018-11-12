#coding=utf-8
"""
系统路由设置
"""
from handlers.login import LoginHandler
from handlers.process_handler import ProcessIndexHandler,ProcessDetailsHandler,ProcessDetailsDataHandler,ExecuteLastProcessHandler,StopProcessHandler,NofocusProcessHandler,ReadLogHandler,DownloadlogHandler,SubmitProcessHandler,ExecuteProcessHandler
from handlers.host_handler import HostIndexHandler

from handlers.input_host_handler import InputHostIndexHandler,TestHostConnectionHandler,InputHostSaveHandler
from handlers.input_process_handler import InputProcessHandler,GetUserHostHandler,GetProcessInfoHandler,ProcessSaveHandler

from handlers.development_schedule_handler import ScheduleHandler

urls = [
    (r'/login', LoginHandler),  # 登录首页
    (r'/development_schedule',ScheduleHandler), # 进度安排
    (r'/', ProcessIndexHandler),   # 默认首页

    #  进程内容
    (r'/process_index', ProcessIndexHandler),   # 首页
    ## 进程详情
    (r'/process_details',ProcessDetailsHandler),
    (r'/process_details/data',ProcessDetailsDataHandler),
    (r'/process_details/execute_last', ExecuteLastProcessHandler),
    (r'/process_details/stop',StopProcessHandler),
    (r'/process_details/nofocus',NofocusProcessHandler),
    (r'/process_details/read_log',ReadLogHandler),
    (r'/process_details/download_log',DownloadlogHandler),
    (r'/process_details/submit_process',SubmitProcessHandler),  # 提交更新的进程信息
    (r'/process_details/execute_process',ExecuteProcessHandler),  # 提交更新的进程信息


    # 主机内容
    (r'/host_index', HostIndexHandler),   # 首页


    # 录入主机功能
    (r'/input_host', InputHostIndexHandler),
    (r'/input_host/test', TestHostConnectionHandler),
    (r'/input_host/save',InputHostSaveHandler),

    # 录入进程功能
    (r'/input_process',InputProcessHandler),
    (r'/input_process/get_host', GetUserHostHandler),
    (r'/input_process/get_process',GetProcessInfoHandler),
    (r'/input_process/save',ProcessSaveHandler),




]
