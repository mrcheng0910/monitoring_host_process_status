#encoding:utf-8
"""
根据输入，将程序由停止运行起来
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import paramiko
import socket


def connect_host(host,code_route, shell,cmd):
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
        status = "异常"
        cpu = mem = vsz = rss = ""
        log_size = '-3' # 主机连接错误
        return cpu,mem,vsz,rss,log_size,status,error_info

    run_process(client,code_route, shell,cmd)

    client.close()

def run_process(client, code_route, shell, cmd):
    """获取进程状态"""

    shell = shell + " " + cmd
    command = 'cd ' + code_route +" ; " + shell
    print command
    stdin, stdout, stderr = client.exec_command(command)  # 执行bash命令
    raw_process_info = stdout.read()
    print raw_process_info



host = ('10.245.146.208',22,'cyn','cynlmh')

connect_host(host,'/home/cyn/cyn','nohup python','test.py &')