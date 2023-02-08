#这个文件可以联合find_stock单独运行，输入todays的日期可以直接查找当天出现过的股票
import datetime
import os
import re
import time
import tushare as ts
import mysql.connector
import constants
import find_stock

#统计当天满足阳包阴所有股票，在设置的这段时间里面有没有出现过类似的行情，并且计算如果出现过，那么那天之后的5天收益率是多少
def rate(todays):
	print(todays)
	overall_winrate(todays)
	count,a,count2 = find_stock.valid_stock(todays)
	# a = 1
	# count = ['300322']
	# count2 = []
	dir_repor = constants.report_dir
	filename = dir_repor + todays + constants.filename_2yang
	fp = open(filename,'w')
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
		code = x[0]
		name = x[1]
		cursor.execute('select * from stock_'+code+' order by date desc')
		value = cursor.fetchall()
	#	print(value)
		winrate = -1
		total_3yang_times = 0
		total_3yang_win_times = 0
		for i in range(1,len(value)):  #遍历这支股票的所有天数
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

				next_high = float(value[i-1][3])

				if find_stock.isSatisfy_3yang(opens1, close1, volume1, p_change1, opens2, close2, volume2, p_change2, opens3, close3, volume3, p_change3):
						total_3yang_times += 1
						change = next_high - close1
						change = change / close1 * 100
						change = round(change, 2)
						if change >= 1:
							total_3yang_win_times += 1

			except:
				print('%s wtf'%x)
		if total_3yang_times > 0:
			winrate = total_3yang_win_times / total_3yang_times
		winrate_str = winrate > 0 and '%s%%！！！！！！！！！！！！！！！' % (winrate * 100) or '无数据'
		str = '%s %s在 %s 之前胜率为:%s\n'%(code, name,todays,winrate_str)
		fp.write(str)
		print(str)


	fp.close()
	conn.close()
	cursor.close()

def overall_winrate(dates):
	df = ts.get_hist_data('sh', start=dates, end=dates)
	close = df.close[0]
	for strategy in constants.strategy_list:
		log = cal_strategy_winrate(strategy, dates, True)
		filename = constants.get_winrate_filename_by_stategy(strategy)
		is_already_have_data = False
		if os.path.exists(filename):
			fp = open(filename, "r")
			lines = fp.readlines()
			fp.close()
			lastLines = lines[len(lines) - 1]
			if re.findall(dates, lastLines):
				is_already_have_data = True
		if is_already_have_data:
			return
		fwinrate = open(filename, 'a')
		str = '%s 上证指数:%s; %s' % (dates, close, log)
		fwinrate.write(str)
		fwinrate.close()

# 遍历集合中的标的，取得其今天的最高股价以及昨天的收盘价，看涨幅是否大于1个点
def realtime_overall_winrate(strategy, wirte_report, stockListFileName=''):
	new_time = time.strftime('%Y-%m-%d')
	print('计算胜率 卖出日期：%s,策略:%s' % (new_time, strategy))
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
	change_sum_open = 0
	change_sum_close = 0

	for x in lines:
		data = x.split(' ')
		code = data[0]
		# close = float(data[1])
		cursor.execute(
			'select * from stock_' + code + ' where date=%s' % (
				yestodayStr))
		value = cursor.fetchall()
		close = float(value[0][2])
		try:
			# 获取单只股票当天的行情
			df = ts.get_realtime_quotes(code)
			high = float(df.high[0])
			change = round((high - close)/close * 100, 2)
			change_sum += change
			open_today = float(df.open[0])
			change_open = round((open_today - close)/close * 100, 2)
			change_sum_open += change_open
			close_today = float(df.price[0])
			change_close = round((close_today - close)/close * 100, 2)
			change_sum_close += change_close
			if close < high and change > 1:
				count += 1
				str = '%s %s 涨幅：%s\n' % (code, df.name[0], change)
				ftoday.write(str)
				if strategy == constants.strategy_3yang:
					print(str)
		except:
			print('%s无行情' % code)

	totalCnt = len(lines)
	winrate = round(count/totalCnt, 2)
	average_change = round(change_sum/totalCnt, 2)
	average_change_open = round(change_sum_open/totalCnt, 2)
	average_change_close = round(change_sum_close/totalCnt, 2)
	str = '%s支标的,昨买今卖,有%s支可以盈利，胜率为%s：,最高价格平均涨幅为:%s, 开盘价平均涨幅为：%s, 收盘价平均涨幅为：%s\n' % (totalCnt, count, winrate, average_change, average_change_open, average_change_close)
	print(stockListFileName)
	print(str)
	ftoday.write(str)
	ftoday.close()
	if wirte_report:
		return '策略[%s],%s' %(strategy, str)
	return

def get_date_str_by_strategy(strategy, dates):
    now = datetime.date(*map(int, dates.split('-')))
    yestoday_str, yestoday = find_stock.get_pre_trade_day(now)
    if strategy == constants.strategy_3yang:
        return constants.get_date_str_for_filename(yestoday)
    elif strategy == constants.strategy_3yang1tiao:
        yestoday_str, yestoday = find_stock.get_pre_trade_day(yestoday)
        return constants.get_date_str_for_filename(yestoday)
    else:
        return constants.get_date_str_for_filename(yestoday)

def get_filename_by_strategy(strategy):
    if strategy == constants.strategy_3yang or strategy == constants.strategy_3yang1tiao:
        return constants.filename_3yang_list
    elif strategy == constants.strategy_2yang:
        return constants.filename_2yang_list

def cal_strategy_winrate(strategy, dates, wirte_report=False):
    date_str = get_date_str_by_strategy(strategy, dates)
    filename = constants.report_dir + date_str + get_filename_by_strategy(strategy)
    return realtime_overall_winrate(strategy, wirte_report, filename)

# realtime_overall_winrate()
#rate('2018-03-16')