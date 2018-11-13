#encoding:utf-8
import smtplib
from email.mime.text import MIMEText
import ConfigParser

mailto_list=['mrcheng0910@gmail.com']           # 收件人(列表)

def get_user():
    cf = ConfigParser.ConfigParser()
    cf.read('email.conf')

    mail_user = cf.get('email_user','mail_user')
    mail_pass = cf.get('email_user','mail_pass')
    mail_postfix = cf.get('email_user','mail_postfix')
    mail_host = cf.get('email_user','mail_host')
    return mail_user,mail_pass,mail_postfix,mail_host


def send_mail(to_list,sub,content):
    mail_user, mail_pass, mail_postfix, mail_host = get_user()
    me="网络安全技术研究中心-预警系统"+"<"+mail_user+"@"+mail_postfix+">"
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



if send_mail(mailto_list,"进程异常警告信息","<h1>进程1异常了</h1>"):  # 邮件主题和邮件内容
    print "done!"
else:
    print "failed!"