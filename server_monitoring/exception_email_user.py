#encoding:utf-8
"""
发送异常预警信息给用户邮箱
"""
import smtplib
from email.mime.text import MIMEText
import ConfigParser


def get_user():
    """获取发件人邮箱账号信息"""
    cf = ConfigParser.ConfigParser()
    cf.read('email.conf')
    mail_user = cf.get('email_user','mail_user')
    mail_pass = cf.get('email_user','mail_pass')
    mail_postfix = cf.get('email_user','mail_postfix')
    mail_host = cf.get('email_user','mail_host')
    return mail_user,mail_pass,mail_postfix,mail_host


def send_mail(to_list,sub,content):
    """发送邮件"""
    mail_user, mail_pass, mail_postfix, mail_host = get_user()
    me="预警系统—网络安全技术研究中心"+"<"+mail_user+"@"+mail_postfix+">"
    # msg = MIMEText(content,_subtype='plain')
    msg = MIMEText(content,'html','utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)                #将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)                            #连接服务器
        server.login(mail_user,mail_pass)               #登录操作
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print e
        return False


def send_process_exception(to_lis,content):
    """发送进程异常信息给用户"""
    sub = "程序异常"
    content = """
    <div>进程ID：<input type="text" value="%s"></div>
    <div>主机IP：<input type="text" value="%s"></div>
    <div>程序状态：<input type="text" value="%s"></div>
    <div>异常原因：<input type="text" value="%s"></div>
    <div>代码路径：<input type="text" value="%s"></div>
    <div>代码名称：<input type="text" value="%s"></div>

    """ % content

    return send_mail(to_lis,sub,content)
