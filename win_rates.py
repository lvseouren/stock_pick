#这个文件可以联合find_stock单独运行，输入todays的日期可以直接查找当天出现过的股票
import datetime
import time
import tushare as ts
import mysql.connector
import constants
import find_stock

#统计当天满足阳包阴所有股票，在设置的这段时间里面有没有出现过类似的行情，并且计算如果出现过，那么那天之后的5天收益率是多少
def rate(todays):
	print(todays)
	overall_winrate(todays)
	#将满足阳包阴的这些股票，以及它们之前满足的时候收益率都写到报告里面方便查看整体情况
	count,a,count2 = find_stock.valid_stock(todays)
	dir_repor = constants.report_dir
	filename = dir_repor + todays + constants.filename_2yang
	fp = open(filename,'a')
	fp.write('总共找到%d支满足条件的股票分别是\n%s\n'%(a,count))
	filename2 = dir_repor + todays + constants.filename_3yang
	fp2 = open(filename2, 'w')
	fp2.write('总共找到%d支满足条件的股票分别是\n%s\n'%(len(count2),count2))
	fp2.close()

	#连接数据库
	conn = mysql.connector.connect(user=constants.mysql_user, password=constants.mysql_password, database=constants.mysql_database_name)
	cursor = conn.cursor()
	#遍历满足条件的这些股票
	for x in count:
		#从数据库里挑出它们的行情
		cursor.execute('select * from stock_'+x+' order by date desc')
		value = cursor.fetchall()
	#	print(value)
		for i in range(0,len(value)):  #遍历这支股票的所有天数
			total_3yang_times = 0
			total_3yang_win_times = 0
			winrate = -1
			try:
				dates = value[i][0]
				opens1 = float(value[i][1])  #第i行的第一列
				opens2 = float(value[i+1][1])
				opens3 = float(value[i+2][1])
				close1 = float(value[i][2])  #第i行的第二列
				close2 = float(value[i+1][2])
				close3 = float(value[i+2][1])
				p_change1 = float(value[i][6])
				p_change2 = float(value[i+1][6])  #第i行的第六列
				p_change3 = float(value[i+2][6])
				volume1 = float(value[i][5])
				volume2 = float(value[i + 1][5])  # 第i行的第5列
				volume3 = float(value[i + 2][5])
				high4 = float[value[i+3][3]]

				if find_stock.isSatisfy_twoyang(opens1, close1, opens2, close2, volume1, volume2, p_change1, p_change2, True):
					if find_stock.isSatisfy_twoyang(opens2, close2, opens3, close3, volume2, volume3, p_change2, p_change3):
						total_3yang_times+=1
						if high4 > close3:
							total_3yang_win_times+=1

			except:
				if total_3yang_times > 0:
					winrate = total_3yang_win_times/total_3yang_times
				pass
	#			print('%s前3个月无满足条件的情况'%x)
			if total_3yang_times > 0:
				winrate = total_3yang_win_times / total_3yang_times
		fp.write('%s在%s之前胜率为%d\n'%(x,dates,winrate))


	fp.close()
	conn.close()
	cursor.close()

def overall_winrate(dates):
	print("使用3阳策略")
	# 载入日志，好查错（因为之前统计出来的股票我去实时查了一下完全不满足条件，所以想到了加入日志好定位是哪个地方出错了）
	dir_log = constants.log_dir
	filename = dir_log + dates + '_winrate.log'
	flog = open(filename, 'w')
	errorFileName = dir_log + dates + 'winrate_error.log'
	f_err_log = open(errorFileName, 'w')
	dir_repor = constants.report_dir
	filename = dir_repor + dates + constants.filename_2yang
	fp = open(filename,'w')
	filename = dir_repor + constants.file_winrate
	fwinrate = open(filename, 'a')

	# 先将字符串格式的时间转换为时间格式才能计算昨天的日期
	now = datetime.date(*map(int, dates.split('-')))
	# # 将昨天日期转换为规定的字符串格式
	str_yestoday, yestoday = find_stock.get_pre_trade_day(now)
	str_theday_before_yestoday, theday_before_yestoday = find_stock.get_pre_trade_day(yestoday)
	str_yestoday_3, yestoday_3 = find_stock.get_pre_trade_day(theday_before_yestoday)

	flog.write('执行的时间前一天是%s\n' % str_yestoday)
	# 将想要查找的日期转换为规定的字符串格式
	str_today = time.strptime(dates, '%Y-%m-%d')
	today = time.strftime('%Y%m%d', str_today)
	flog.write('执行的时间是%s\n' % today)
	# 连接数据库
	conn = mysql.connector.connect(user=constants.mysql_user, password=constants.mysql_password,
								   database=constants.mysql_database_name)
	cursor = conn.cursor()
	# 查找allstock表获取所有股票代码
	cursor.execute('select code, name from allstock')
	value_code = cursor.fetchall()
	count_3yang = 0
	count_3yang_earn = 0

	# 遍历所有股票
	for i in range(0, len(value_code)):
		code = value_code[i][0]
		name = value_code[i][1]
		if not constants.stock_is_st(name) and constants.stock_filter_all(code):
			# 查询所有匹配到的股票，将今天与昨天的数据对比
			try:
				cursor.execute(
					'select * from stock_' + code + ' where date=%s or date =%s or date =%s or date = %s order by date desc' % (
						today, str_yestoday, str_theday_before_yestoday, str_yestoday_3))  # 当天
				# cursor.execute('select * from stock_'+ value_code[i][0]+ ' where date=%s or date =%s'%('20180315','20180314'))
				value = cursor.fetchall()

				# 2是昨天，1是今天
				# 今天的开盘价
				opens1 = float(value[0][1])
				# 今天的收盘价
				close1 = float(value[0][2])
				# 今天的涨幅
				p_change1 = float(value[0][6])
				volume1 = float(value[0][5])
				high1 = float(value[0][3])
				# 昨天的。。。。。
				opens2 = float(value[1][1])
				close2 = float(value[1][2])
				volume2 = float(value[1][5])
				p_change2 = float(value[1][6])

				# 前天的。。。。。
				opens3 = float(value[2][1])
				close3 = float(value[2][2])
				volume3 = float(value[2][5])
				p_change3 = float(value[2][6])
				# 大前天的。。。。。
				opens4 = float(value[3][1])
				close4 = float(value[3][2])
				volume4 = float(value[3][5])
				p_change4 = float(value[3][6])
				# flog.write('检查%s是否满足特征...\n' % (code))

				if find_stock.isSatisfy_3yang(opens2, close2, volume2, p_change2, opens3, close3, volume3, p_change3, opens4, close4, volume4, p_change4):
					count_3yang += 1
					is_can_earn = high1 > close2 and (high1 - close2)/close2 > 0.01
					if is_can_earn:
						count_3yang_earn += 1
			except:
				# 之前有次sql语句出错了，order by后面没加date，每次寻找都是0支，找了半个多小时才找出来是sql语句的问题
				f_err_log.write(
					'%s停牌无数据,或者请查看sql语句是否正确\n' % value_code[i][0])  # 一般不用管，除非执行好多天的数据都为0时那可能输sql语句有问题了

	summary = '%s前一个交易日满足3阳策略的标的有%s支,其中%s只今日的最高涨幅超过一个点\n' % (dates, count_3yang, count_3yang_earn)
	print(summary)
	winrate = 0
	if count_3yang > 0:
		winrate = count_3yang_earn/count_3yang
	winRateStr = "%s大盘该策略的胜率为 %s\n\n" % (dates, winrate)
	print(winRateStr)
	flog.write(summary)
	flog.write(winRateStr)
	fp.write(summary)
	fp.write(winRateStr)

	df = ts.get_hist_data('sh', start=dates, end=dates)
	close = df.close[0]
	str = '%s 上证指数：%s 策略胜率(上一交易日满足特征的标的在此交易日卖出盈利的概率)：%s\n' %(dates, close, winrate)
	fwinrate.write(str)

	fwinrate.close()
	flog.close()
	f_err_log.close()
	conn.close()
	fp.close()
	cursor.close()

# 遍历上一交易日所有的3yang标的，取得其今天的最高股价，看涨幅是否大于1个点
def realtime_overall_winrate():
	new_time = time.strftime('%Y-%m-%d')
	filename = constants.report_dir + new_time + '_实时胜率.txt'
	ftoday = open(filename, 'w')

	now = datetime.date(*map(int, new_time.split('-')))
	yestodayStr, yestoday = find_stock.get_pre_trade_day(now)
	yestodayStr2 = time.strptime(yestodayStr, '%Y%m%d')
	yestodayStr2 = time.strftime('%Y-%m-%d', yestodayStr2)
	yestodayStr2 = '2023-01-30'
	filename = constants.report_dir + yestodayStr2 + constants.filename_3yang_list
	fp = open(filename, "r")
	ftoday.write('%s中 以下标的最高涨幅超过1个点：\n' %filename)
	lines = fp.readlines()
	fp.close()

	conn = mysql.connector.connect(user=constants.mysql_user, password=constants.mysql_password,
								   database=constants.mysql_database_name)
	cursor = conn.cursor()
	count = 0
	change_sum = 0
	for x in lines:
		data = x.split(' ')
		code = data[0]
		# close = float(data[1])
		cursor.execute(
			'select * from stock_' + code + ' where date=%s' % (
				yestodayStr))  # 当天
		value = cursor.fetchall()
		close = float(value[0][2])
		try:
			# 获取单只股票当天的行情
			df = ts.get_realtime_quotes(code)
			high = float(df.high[0])
			change = (high - close)/close
			change_sum += change
			if close < high and change > 0.01:
				count += 1
				ftoday.write('%s %s\n' % (code, df.name[0]))
				print('%s %s' % (code, df.name[0]))

		except:
			print('%s无行情' % code)

	totalCnt = len(lines)
	winrate = count/totalCnt
	average_change = change_sum/totalCnt
	str = '%s只标的中有%s可以盈利，实时胜率为%s：,平均涨幅为:%s\n' % (totalCnt, count, winrate, average_change)
	print(str)
	ftoday.write(str)
	ftoday.close()
	return

# realtime_overall_winrate()
#rate('2018-03-16')