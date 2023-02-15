import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header, make_header
import time

def send_email(subject, att_file_names, att_suffixs, is_send_bao=False):
    todays = time.strftime('%Y-%m-%d')
    # 设置自己邮件服务器和账号密码
    smtpserver = 'smtp.163.com'
    user = 'huiseouren17@163.com'
    password = 'FTVYFMEGVZGFDZSS'
    # 设置接收邮箱和主题
    sender = user
    receiver = '602633512@qq.com'

    index = 0
    msg = MIMEMultipart('mixed')
    for att_file_name in att_file_names:
        f = open(att_file_name, 'rb')
        mail_body = f.read()
        f.close()
        att = MIMEText(mail_body, 'txt', 'utf-8')
        att['Content-Type'] = 'application/octet-stream'
        name = '%s%s.txt' %(todays, att_suffixs[index])
        att.add_header("Content-Disposition", "attachment", filename=("gbk", "", name))
        msg.attach(att)
        index+=1

    msg['From'] = user
    msg['To'] = receiver
    msg['Subject'] = Header(subject, 'utf-8')

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver, 25)
    smtp.login(user, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    if is_send_bao:
        receiver2 = '942259616@qq.com'
        smtp.sendmail(sender, receiver2, msg.as_string())

    receiver3 = '13112355359@163.com'
    smtp.sendmail(sender, receiver3, msg.as_string())
    smtp.quit()