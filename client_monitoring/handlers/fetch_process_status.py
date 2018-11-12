#encoding:utf-8
"""
监测进程状态
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import paramiko
import socket

def connect_host(host,pid,log_route,log_name):
    """连接主机"""
    # db = MySQL(SOURCE_CONFIG)
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
        status = "异常"
        cpu = mem = vsz = rss = ""
        log_size = '-3' # 主机连接错误
        return cpu,mem,vsz,rss,log_size,status,error_info

    status_error, process_status = fetch_process_status(client, pid)
    log_size = fetch_log_info(client, log_route, log_name)

    cpu, mem, vsz, rss = process_status['cpu'], process_status['mem'], process_status['vsz'], process_status['rss']
    if status_error:
        error_info = '程序异常' + str(status_error)
        status = '异常'
    else:
        if cpu == mem == vsz == rss:
            status = '停止'
            error_info = '程序停止'
        else:
            status = '正常'
            error_info = '程序正常'
    client.close()
    return cpu,mem,vsz,rss,log_size,status,error_info


def fetch_log_info(client, log_route,log_name):
    """得到日志信息"""
    if log_name.strip() == '':
        return '-1'  # -1表示未设置日志路径
    command = 'du -h "%s"'  # 根据进程号显示出进程状态信息，并且不显示无用信息
    stdin, stdout,stderr = client.exec_command(command % log_route.strip()+log_name.strip())   # 执行bash命令
    raw_log_info = stdout.read()
    error = stderr.read()
    if not error:
        log_size = extract_log_size(raw_log_info)
        return log_size
    else:
        return '-2'  # -2表示未找到该路径下文件


def fetch_process_status(client, pid):
    """获取进程状态"""
    command = 'ps aux|grep "%s" -a |grep -v "grep" -a'  # 根据进程号显示出进程状态信息，并且不显示无用信息
    stdin, stdout, stderr = client.exec_command(command % pid)  # 执行bash命令
    raw_process_info = stdout.read()
    error = stderr.read()
    # 判断stderr输出是否为空，为空则打印执行结果，不为空打印报错信息
    if not error:
        process_status = extract_process_status(raw_process_info)
        return False, process_status
    else:
        return True, error

def extract_process_status(raw_process_info):
    """解析出进程的状态信息"""
    process_info = raw_process_info.strip().split(' ')
    while '' in process_info:  # 去除空格
        process_info.remove('')
    if process_info:
        cpu, mem, vsz, rss = process_info[2], process_info[3], process_info[4], process_info[5]
    else:
        cpu = mem = vsz = rss = 0
    process_status = {
        'cpu': cpu, # cpu%
        'mem': mem,  # 存储%
        'vsz': vsz,  # 虚拟内存
        'rss': rss  # 固定内存
    }
    return process_status


def extract_log_size(raw_log_info):
    """提取日志大小"""
    log_size = raw_log_info.strip().split('\t')[0]
    return log_size