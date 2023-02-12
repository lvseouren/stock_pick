#总的运行文件，实现将统计报告发送邮件到自己的邮箱，将这个文件放到Jenkin上每个交易日下午3点之后运行就可以收到当天满足行情的股票了
import constants
import win_rates
import time
import os
import tushare as ts
import email_sender
# import wechat_sender

if __name__ == '__main__':
	#初始化tshare
	ts.set_token('ed4a03d581a87d8a6f95cf1f06d31bec659d785e9bf410008fe91493')

	test_report_dir = constants.report_dir
	if not os.path.exists(constants.report_dir):
		os.mkdir(constants.report_dir)
	if not os.path.exists(constants.log_dir):
		os.mkdir(constants.log_dir)

	todays = time.strftime('%Y-%m-%d')
	todays = '2023-02-10'
	win_rates.rate(todays)
	str = '今天的股票行情来啦(strict_level=%s)' % (constants.strict_level)
	filename1 = test_report_dir + todays + constants.filename_2yang
	filename2 = test_report_dir + todays + constants.filename_3yang
	subject = str
	filename3 = constants.get_winrate_filename_by_stategy(constants.strategy_3yang)
	email_sender.send_email(subject, [filename1, filename2, filename3], ['_2yang列表', '_3yang列表', '胜率信息'], True)
	# wechat_sender.send_msg('狄拉克海捕鱼人', 'cfmm已发送邮箱，请查收')