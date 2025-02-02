#总的运行文件，实现将统计报告发送邮件到自己的邮箱，将这个文件放到Jenkin上每个交易日下午3点之后运行就可以收到当天满足行情的股票了
import constants
import ml_update_model
import win_rates
import time
import os
import tushare as ts
import email_sender
# import wechat_sender

def run_date(today):
	#初始化tshare
	ts.set_token('ed4a03d581a87d8a6f95cf1f06d31bec659d785e9bf410008fe91493')

	test_report_dir = constants.report_dir
	if not os.path.exists(constants.report_dir):
		os.mkdir(constants.report_dir)
	if not os.path.exists(constants.log_dir):
		os.mkdir(constants.log_dir)

	# today = time.strftime('%Y-%m-%d')
	# today = '2023-02-16'
	win_rates.rate(today)
	str = '今天的cfmm来啦(strict_level=%s)' % (constants.strict_level)
	filename1 = test_report_dir + today + constants.filename_2yang
	filename2 = test_report_dir + today + constants.filename_3yang
	filename4 = constants.ml_report_dir + today + '_' + constants.ml_sheet_name_predict + '_' + constants.ml_predict_report_filename_3yang1tiao
	subject = str
	filename3 = constants.get_winrate_filename_by_stategy(constants.strategy_3yang)
	# email_sender.send_email(subject, [filename1, filename2, filename3, filename4], ['_2yang列表', '_3yang列表', '胜率信息', '预测信息'], True)
	# wechat_sender.send_msg('狄拉克海捕鱼人', 'cfmm已发送邮箱，请查收')
	# ml_update_model.update_model()

def run_dates(starttime, endtime):
	df = ts.get_hist_data('sh', starttime, endtime)
	# 这里使用try，except的目的是为了防止一些停牌的股票，获取数据为空，插入数据库的时候失败而报错
	# 再使用for循环遍历单只股票每一天的行情
	try:
		for i in range(0, len(df)):
			# 获取股票日期，并转格式（这里为什么要转格式，是因为之前我2018-03-15这样的格式写入数据库的时候，通过通配符%之后他居然给我把-符号当做减号给算出来了查看数据库日期就是2000百思不得其解想了很久最后决定转换格式）
			time_new = df.index[i]
			run_date(time_new)
	except:
		'run_dates出错啦'

# today = time.strftime('%Y-%m-%d')
# run_date(today)
ml_update_model.update_model()
# run_dates('2022-01-01','2023-01-13')