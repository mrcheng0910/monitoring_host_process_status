#encoding: utf-8
"""
读取程序日志
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import paramiko
import socket


def connect_host(host,log_route,log_name):
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
    result = run_process(client,log_route,log_name)
    client.close()
    return result


def run_process(client,log_route,log_name):
    """获取日志情况"""
    log = log_route+log_name
    command = "tail -n 100 " + log   # 读取后100行数据
    stdin, stdout, stderr = client.exec_command(command)  # 执行bash命令
    log_info = stdout.read()
    if log_info:
        return log_info
    else:
        return stderr.read()

# host = ('10.245.146.208',22,'cyn','cynlmh')

# connect_host(host,'/home/cyn/cyn/malicious_domain_history/fetch_dns/','nohup.out')