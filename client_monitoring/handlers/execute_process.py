#encoding: utf-8
"""
读取程序日志
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import paramiko
import socket


def connect_host(host,log_route,code_route,log_name,code_name,shell,cmd):
    """连接主机"""
    host_error = False
    hostname, port, username, password = host
    client = paramiko.SSHClient()    # 创建客户端
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, port, username, password, timeout=3)
    except paramiko.BadHostKeyException, e:
        host_error = e
    except paramiko.AuthenticationException,e:
        host_error = e
    except paramiko.SSHException,e:
        host_error = e
    except socket.error,e:
        host_error = e
    if host_error:
        error_info = '主机异常:'+ str(host_error)
        return error_info
    run_process(client,log_route,code_route,log_name,shell,cmd)  # 运行程序
    pid = runing_or_not(client,code_name)  # 检测是否运行，并获取pid
    client.close()
    return pid


def run_process(client,log_route,code_route,log_name,shell,cmd):
    """运行程序"""
    log = log_route+log_name
    command = "cd " + code_route +" ; "
    command = command + "nohup "+ shell + " " + cmd +" &> "
    command = command + log_route+log_name + "&"
    client.exec_command(command)  # 执行bash命令

def runing_or_not(client, code_name):
    """判断程序是否正常运行，若运行返回pid，若无则返回空，考虑相同名称的代码的情况"""
    command = 'ps -eo pid,lstart,etime,cmd |grep "%s" |grep -v "grep" -a'
    _, stdout, _ = client.exec_command(command % code_name)  # 执行bash命令
    raw_processes_status = stdout.read()
    pid = ''
    if not raw_processes_status:   # 若未获取到则pid为空
        return pid
    raw_processes_status = raw_processes_status.strip().split('\n')
    for i in raw_processes_status:
        process_status = i.strip().split(' ')  # 分割成列表
        while '' in process_status: # 去除列表中多余的空值
            process_status.remove('')
        interval_time = int(process_status[6].split(':')[1])  # 得到已运行时间
        if interval_time < 2: # 在2秒内启动的进程，2秒是大概的时间
            pid = process_status[0]
    return pid