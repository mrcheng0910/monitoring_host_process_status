#encoding:utf-8
"""
监测进程状态
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import paramiko
import socket


def connect_host(host, pid):
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
        return "停止失败："+str(host_error)

    result = stop_process(client, pid)
    client.close()
    return result


def stop_process(client, pid):
    """获取进程状态"""
    stop_result = ""
    command = 'kill -9 "%s" '
    stdin, stdout, stderr = client.exec_command(command % pid)  # 执行bash命令
    kill_status = stdout.read()
    error = stderr.read()
    if error or kill_status:
        error = error.split(':')[3].strip()
        stop_result = "停止失败："+str(error)

    else:
        stop_result = "停止成功"
    return stop_result

# host = ('10.245.146.208',22,'cyn','cynlmh')
# connect_host(host,'23481')
# a = '-bash: kill: (23481) - Operation not permitted'
# b = '-bash: kill: 1111111111111111: arguments must be process or job IDs'