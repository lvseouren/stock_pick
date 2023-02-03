#总的运行文件，实现将统计报告发送邮件到自己的邮箱，将这个文件放到Jenkin上每个交易日下午3点之后运行就可以收到当天满足行情的股票了
import constants
import win_rates
# import write_everyday
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import tushare as ts
import email_sender

# #获取最新的文件
# def new_file(test_report_dir):
# 	lists = os.listdir(test_report_dir)
# 	lists.sort(key = lambda fn:os.path.getmtime(test_report_dir + fn))
# 	file_path = os.path.join(test_report_dir,lists[-1])
# 	return file_path
#发送邮件

if __name__ == '__main__':
	#初始化tshare
	ts.set_token('ed4a03d581a87d8a6f95cf1f06d31bec659d785e9bf410008fe91493')

	test_report_dir = constants.report_dir
	if not os.path.exists(constants.report_dir):
		os.mkdir(constants.report_dir)
	if not os.path.exists(constants.log_dir):
		os.mkdir(constants.log_dir)

	todays = time.strftime('%Y-%m-%d')
	win_rates.rate(todays)
	str = '今天的股票行情来啦(strict_level=%s)' % (constants.strict_level)
	filename = test_report_dir + todays + constants.filename_2yang
	subject = str + '(2yang)'
	email_sender.send_email(subject, filename, '_2yang列表')
	subject = str + '(3yang)'
	filename = test_report_dir + todays + constants.filename_3yang
	email_sender.send_email(subject, filename, '_3yang列表')
	subject = '策略胜率追踪'
	filename = test_report_dir + constants.file_winrate
	email_sender.send_email(subject, filename)
