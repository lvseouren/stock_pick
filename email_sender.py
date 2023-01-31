import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header, make_header
import time

def send_email(subject, att_file_name, att_suffix = ' '):
    todays = time.strftime('%Y-%m-%d')
    f = open(att_file_name, 'rb')
    mail_body = f.read()
    f.close()
    # 设置自己邮件服务器和账号密码
    smtpserver = 'smtp.163.com'
    user = 'huiseouren17@163.com'
    password = 'FTVYFMEGVZGFDZSS'
    # 设置接收邮箱和主题
    sender = user
    receiver = '602633512@qq.com'

    msg = MIMEMultipart('mixed')
    att = MIMEText(mail_body, 'txt', 'utf-8')
    att['Content-Type'] = 'application/octet-stream'
    name = '%s%s.txt' %(todays, att_suffix)
    att.add_header("Content-Disposition", "attachment", filename=("gbk", "", name))

    msg.attach(att)

    msg['From'] = user
    msg['To'] = receiver
    msg['Subject'] = Header(subject, 'utf-8')

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver, 25)
    smtp.login(user, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    receiver2 = '942259616@qq.com'
    smtp.sendmail(sender, receiver2, msg.as_string())
    smtp.quit()