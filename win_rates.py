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
	new_time = dates
	now = datetime.date(*map(int, new_time.split('-')))
	yestodayStr, yestoday = find_stock.get_pre_trade_day(now)
	yestodayStr2 = constants.change_date_str_format(yestodayStr, '%Y%m%d', '%Y-%m-%d')
	filename = constants.report_dir + yestodayStr2 + constants.filename_3yang_list
	strategy = '3yang'
	realtime_overall_winrate(strategy, filename)

	yestodayStr, yestoday = find_stock.get_pre_trade_day(yestoday)
	yestodayStr2 = constants.change_date_str_format(yestodayStr, '%Y%m%d', '%Y-%m-%d')
	filename = constants.report_dir + yestodayStr2 + constants.filename_3yang_list
	strategy = '3yang1tiao'
	realtime_overall_winrate(strategy, filename)

# 遍历上一交易日所有的3yang标的，取得其今天的最高股价，看涨幅是否大于1个点
def realtime_overall_winrate(strategy, stockListFileName=''):
	new_time = time.strftime('%Y-%m-%d')
	now = datetime.date(*map(int, new_time.split('-')))
	yestodayStr, yestoday = find_stock.get_pre_trade_day(now)

	filename = constants.report_dir + new_time + '_实时胜率.txt'
	ftoday = open(filename, 'w')

	# yestodayStr2 = '2023-01-31'
	if len(stockListFileName) == 0:
		yestodayStr2 = constants.change_date_str_format(yestodayStr, '%Y%m%d', '%Y-%m-%d')
		stockListFileName = constants.report_dir + yestodayStr2 + constants.filename_3yang_list
	fp = open(stockListFileName, "r")
	ftoday.write('%s中 以下标的最高涨幅超过1个点：\n' %stockListFileName)
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
			change = round((high - close)/close * 100, 2)
			change_sum += change
			if close < high and change > 1:
				count += 1
				str = '%s %s 涨幅：%s\n' % (code, df.name[0], change)
				ftoday.write(str)
				print(str)

		except:
			print('%s无行情' % code)

	totalCnt = len(lines)
	winrate = round(count/totalCnt, 2)
	average_change = round(change_sum/totalCnt, 2)
	str = '%s支标的,昨天买入,有%s支可以盈利，实时胜率为%s：,平均涨幅为:%s\n' % (totalCnt, count, winrate, average_change)
	filename = constants.report_dir + constants.file_winrate
	fwinrate = open(filename, 'a')
	df = ts.get_hist_data('sh', start=new_time, end=new_time)
	close = df.close[0]
	fwinrate.write('%s 上证指数：%s %s策略,%s' %(new_time, close, strategy, str))
	fwinrate.close()
	print(str)
	print(filename)
	ftoday.write(str)
	ftoday.close()
	return

# realtime_overall_winrate()
#rate('2018-03-16')