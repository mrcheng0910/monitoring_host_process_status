#encoding:utf-8
"""
1. 长期监测进程状态，并将状态信息存入数据库中
2. 对于出现异常或者停止的进程，发送预警电子邮件给用户
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import paramiko
import socket
from collections import defaultdict
from data_base import MySQL
from mysql_config import SOURCE_CONFIG, sql as fetch_sql
import schedule
import time
import base64
from datetime import datetime
from exception_email_user import send_process_exception


def obtain_monitoring_host_process():
    """获取待监测的进程信息"""
    db = MySQL(SOURCE_CONFIG)
    # 获取超过间隔时间的进程
    sql = fetch_sql
    db.query(sql)
    host_process_result = db.fetch_all_rows()
    host_process = group_host_process(host_process_result)
    db.close()
    return host_process


def process_id_to_user(process_id):
    """通过process_id获取用户的邮箱地址和主机地址"""
    sql = "SELECT email,host_ip,pid,code_route,process_name,warning_times FROM `process_info`,user_account,host_info WHERE process_id = '%s' AND user_account.user_id = process_info.user_id AND host_info.host_id = process_info.host_id"
    db = MySQL(SOURCE_CONFIG)
    db.query(sql % process_id)
    email_host = db.fetch_all_rows()
    email = email_host[0][0]
    host = base64.decodestring(email_host[0][1])
    pid = email_host[0][2]
    code_route = email_host[0][3]
    process_name = email_host[0][4]
    warning_times = email_host[0][5]
    db.close()
    return email, host,pid,code_route,process_name,warning_times

def reduce_warning_times(process_id):
    db = MySQL(SOURCE_CONFIG)

    sql = 'update process_info set warning_times = warning_times -1 where process_id = "%s"' % process_id
    db.update(sql)
    db.close()

def group_host_process(host_process_result):
    """相同主机的进程分组"""
    host_process = defaultdict(list)
    for hp in host_process_result:
        host_process[(hp[1],hp[2],hp[3],hp[4])].append((hp[0],hp[5],hp[6],hp[7]))
    print host_process
    return host_process


def connect_host(host,process_ids):
    """连接主机"""
    db = MySQL(SOURCE_CONFIG)
    host_error = False
    hostname, port, username, password = host
    client = paramiko.SSHClient()    # 创建客户端
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    hostname = base64.decodestring(hostname).strip()
    username = base64.decodestring(username).strip()
    password = base64.decodestring(password).strip()
    port = int(base64.decodestring(port).strip())
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
        return host_error

    for pid, process_id,log_route,log_name in process_ids:
        status_error, process_status = fetch_process_status(client, pid)
        log_size = fetch_log_info(client,log_route,log_name)
        update_process_info(db, status_error, process_status, process_id, log_size)
    client.close()
    db.close()
    return False


def fetch_log_info(client, log_route,log_name):
    """得到日志信息"""
    if log_name == '':
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
        process_status = extract_process_status(raw_process_info,pid)
        return False, process_status
    else:
        return True, error


def insert_host_error(error,process_ids):
    """更新主机错误"""
    db = MySQL(SOURCE_CONFIG)
    error_info = '主机异常:'+ str(error)
    status = '异常'
    sql = 'insert into process_status (process_id,cpu,mem,vsz,rss,status,error_info,log_size) values("%s","%s","%s","%s","%s","%s","%s","%s")'
    for _,process_id,_,_ in process_ids:
        db.insert(sql % (process_id, 0, 0, 0, 0, status, error_info,'-3'))   # -3表示日志的主机错误
        email, host, pid, code_route, code_name,warning_times = process_id_to_user(process_id)
        if warning_times > 0:
            content = (pid, host, status, error_info, code_route, code_name)
            if send_process_exception([email], content):
                print "邮件预警成功:" + email
                reduce_warning_times(process_id)
            else:
                print "邮件预警失败:" + email
    db.close()


def update_process_info(db, status_error, process_status, process_id,log_size):
    """更新进程信息"""

    cpu, mem, vsz, rss = process_status['cpu'],process_status['mem'],process_status['vsz'],process_status['rss']

    sql = 'insert into process_status (process_id,cpu,mem,vsz,rss,status,error_info,log_size) values("%s","%s","%s","%s","%s","%s","%s","%s")'
    if status_error:
        error_info = '程序异常'+str(status_error)
        status = '异常'
    else:
        if cpu == mem == vsz == rss:
            status = '停止'
            error_info = '程序停止'
        else:
            status = '正常'
            error_info='程序正常'

    db.insert(sql % (process_id, cpu, mem, vsz,rss, status, error_info,log_size))

    # 预警通知
    if status == "停止" or status=="异常":
        email,host,pid,code_route,code_name,warning_times = process_id_to_user(process_id)
        if warning_times > 0:
            content = (pid,host,status,error_info,code_route,code_name)
            if send_process_exception([email],content):
                print "邮件预警成功:"+email
                reduce_warning_times(process_id)
            else:
                print "邮件预警失败:"+email


def extract_process_status(raw_process_info,pid):
    """解析出进程的状态信息
    todo: 存在潜在多条记录的情况，默认只处理一个，潜在bug
    """
    process_info = raw_process_info.strip().split(' ')
    while '' in process_info:  # 去除空格
        process_info.remove('')
    if process_info:
        if str(pid) != str(process_info[1]):  # 可能获取的信息与pid不一样，用于判断这种情况
            cpu = mem = vsz = rss = 0
        else:
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


def main():

    # 获取待检测的进程信息
    print str(datetime.now()), '开始探测主机和进程状态'
    host_process = obtain_monitoring_host_process()
    for host in host_process:
        print host
        print host_process[host]
        error = connect_host(host, host_process[host])
        if error:
            insert_host_error(error, host_process[host])
    print str(datetime.now()), '结束探测主机和进程状态'


if __name__ == '__main__':
    # main()  # 测试使用
    # todo: 优化，循环探测时间使用配置文件，可以设置，方便修改
    schedule.every(10).minutes.do(main)  # 10分钟循环探测一遍
    while True:
        schedule.run_pending()
        time.sleep(1)
