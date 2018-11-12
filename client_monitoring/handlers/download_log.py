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
    host_name,port,user_name,pwd = host

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host_name, port, user_name, pwd)

    new_log_name = compress_log(client,log_route,log_name)

    sftp_client = client.open_sftp()
    remote_file = sftp_client.open(log_route+new_log_name)
    log_content = remote_file.read()
    remote_file.close()
    client.close()
    return log_content, new_log_name

def compress_log(client,log_route,log_name):
    command = 'gzip -c '+ log_route + log_name + ' > '+log_route+log_name+'.gz'  # 压缩文件
    stdin, stdout, stderr = client.exec_command(command)  # 执行bash命令
    new_log_name = log_name+'.gz'
    return new_log_name


# host = ('10.245.146.208',22,'cyn','cynlmh')

# connect_host(host,'/home/cyn/cyn/malicious_domain_history/fetch_dns/','readme.md')