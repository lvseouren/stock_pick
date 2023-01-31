import mysql.connector
import re,time
import datetime,os
import constants
import tushare as ts

#从数据库获取股票数据，统计想要查找日期的满足阳包阴并且当天涨停的股票
def valid_stock(dates):
	# return yangbaoying(dates)
	return twoyang(dates)

def yangbaoying(dates):
	print("使用阳包阴策略")
	# 载入日志，好查错（因为之前统计出来的股票我去实时查了一下完全不满足条件，所以想到了加入日志好定位是哪个地方出错了）
	dir_log = constants.log_dir
	filename = dir_log + dates + '.log'
	flog = open(filename, 'w')

	# 先将字符串格式的时间转换为时间格式才能计算昨天的日期
	now = datetime.date(*map(int, dates.split('-')))
	oneday = datetime.timedelta(days=1)
	yestody = str(now - oneday)
	# 将昨天日期转换为规定的字符串格式
	times = time.strptime(yestody, '%Y-%m-%d')
	str_yestoday = time.strftime('%Y%m%d', times)
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
	cursor.execute('select code from allstock')
	value_code = cursor.fetchall()
	a = 0
	count = []
	# 遍历所有股票
	for i in range(0, len(value_code)):
		if re.match('000', value_code[i][0]) or re.match('002', value_code[i][0]):
			# 查询所有匹配到的股票，将今天与昨天的数据对比
			try:
				cursor.execute(
					'select * from stock_' + value_code[i][0] + ' where date=%s or date =%s order by date desc' % (
					today, str_yestoday))  # 当天
				# cursor.execute('select * from stock_'+ value_code[i][0]+ ' where date=%s or date =%s'%('20180315','20180314'))
				value = cursor.fetchall()

				# 1是昨天，2是今天
				# 今天的开盘价
				opens1 = float(value[0][1])
				# 今天的收盘价
				close1 = float(value[0][2])
				# 今天的涨幅
				p_change1 = float(value[0][6])
				# 昨天的。。。。。
				opens2 = float(value[1][1])
				close2 = float(value[1][2])
				p_change2 = float(value[1][6])

				# 加入这两天的数据满足昨天下跌超过2%，而且今天的开盘价低于昨天的收盘价，且今天的收盘价高于昨天的收盘价，就满足阳包阴的条件
				if opens2 < close1 and close2 > opens1 and p_change2 < -2 and p_change1 > 9.8:
					flog.write('%s票%s的开盘价是%s\n' % (value_code[i][0], today, opens1))
					flog.write('%s票%s的收盘价是%s\n' % (value_code[i][0], today, close1))
					flog.write('%s票%s的涨幅是%s\n' % (value_code[i][0], today, p_change1))
					flog.write('%s票%s的开盘价是%s\n' % (value_code[i][0], str_yestoday, opens2))
					flog.write('%s票%s的收盘价价是%s\n' % (value_code[i][0], str_yestoday, close2))
					flog.write('%s票%s的涨幅是%s\n' % (value_code[i][0], str_yestoday, p_change2))
					# 将满足条件的股票代码放进列表中，统计当天满足条件的股票
					count.append(value_code[i][0])
					a += 1
			except:
				# 之前有次sql语句出错了，order by后面没加date，每次寻找都是0支，找了半个多小时才找出来是sql语句的问题
				flog.write(
					'%s停牌无数据,或者请查看sql语句是否正确\n' % value_code[i][0])  # 一般不用管，除非执行好多天的数据都为0时那可能输sql语句有问题了


	print('总共找到%d支满足条件的股票'%a)
	flog.close()
	conn.close()
	cursor.close()
	return count,a

def twoyang(dates):
	print("使用3阳策略")
	# 载入日志，好查错（因为之前统计出来的股票我去实时查了一下完全不满足条件，所以想到了加入日志好定位是哪个地方出错了）
	dir_log = constants.log_dir
	filename = dir_log + dates + '.log'
	flog = open(filename, 'w')
	errorFileName = dir_log +dates + '_error.log'
	f_err_log = open(errorFileName, 'w')
	filename = constants.report_dir + dates + '_list.txt'
	flist = open(filename, 'w')

	# 先将字符串格式的时间转换为时间格式才能计算昨天的日期
	now = datetime.date(*map(int, dates.split('-')))
	# oneday = datetime.timedelta(days=1)
	# yestody = str(now - oneday)
	# # 将昨天日期转换为规定的字符串格式
	# times = time.strptime(yestody, '%Y-%m-%d')
	# str_yestoday = time.strftime('%Y%m%d', times)
	str_yestoday, yestoday = get_pre_trade_day(now)
	str_theday_before_yestoday, theday_before_yestoday = get_pre_trade_day(yestoday)

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
	a = 0
	count = []
	count_3yang = []
	# 遍历所有股票
	for i in range(0, len(value_code)):
		code = value_code[i][0]
		name = value_code[i][1]
		if not constants.stock_is_st(name) and constants.stock_filter_all(code):
			# 查询所有匹配到的股票，将今天与昨天的数据对比
			try:
				cursor.execute(
					'select * from stock_' + code + ' where date=%s or date =%s or date =%s order by date desc' % (
						today, str_yestoday, str_theday_before_yestoday))  # 当天
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
				flog.write('检查%s是否满足特征...\n' % (code))

				if isSatisfy_twoyang(opens1, close1, opens2, close2, volume1, volume2, p_change1, p_change2, True):
					if not isSatisfy_twoyang(opens2, close2, opens3, close3, volume2, volume3, p_change2, p_change3):
						flist.write('%s %s %s \n' %(code, close1, volume1))
						flog.write('%s票%s的开盘价是%s\n' % (code, today, opens1))
						flog.write('%s票%s的收盘价是%s\n' % (code, today, close1))
						flog.write('%s票%s的成交量是%s\n' % (code, today, volume1))
						flog.write('%s票%s的开盘价是%s\n' % (code, str_yestoday, opens2))
						flog.write('%s票%s的收盘价价是%s\n' % (code, str_yestoday, close2))
						flog.write('%s票%s的成交量是%s\n' % (code, str_yestoday, volume2))
						# 将满足条件的股票代码放进列表中，统计当天满足条件的股票
						count.append(code)
						a += 1
					else:
						# 3yang了
						count_3yang.append(code)
			except:
				# 之前有次sql语句出错了，order by后面没加date，每次寻找都是0支，找了半个多小时才找出来是sql语句的问题
				f_err_log.write(
					'%s停牌无数据,或者请查看sql语句是否正确\n' % value_code[i][0])  # 一般不用管，除非执行好多天的数据都为0时那可能输sql语句有问题了

	print('总共找到%d支满足条件的股票' % a)
	flog.close()
	f_err_log.close()
	flist.close()
	conn.close()
	cursor.close()
	return count, a, count_3yang

# 1今天2昨天3前天
def isSatisfy_3yang(open1, close1, volume1, p_change1, open2, close2, volume2, p_change2, open3, close3, volume3, p_change3):
	return isSatisfy_twoyang(open1, close1, open2, close2, volume1, volume2, p_change1, p_change2, True) and isSatisfy_twoyang(open2, close2, open3, close3, volume2, volume3, p_change2, p_change3)


# 2是昨天，1是今天
def isSatisfy_twoyang(opens1, close1, opens2, close2, volume1, volume2, p_change1, p_change2, is_change_limit = False):
	ret = close1 > close2 and close2 > opens2 and close1 > opens1 and volume1 > volume2
	if ret and is_change_limit:
		ret = ret and p_change2 > 0 and p_change1 > 2

	if is_change_limit and ret and constants.strict_level > 1:
		ret = p_change1 <= 5
	return ret

def get_pre_trade_day(now):
	is_find = False
	ret = now
	oneday = datetime.timedelta(days=1)
	while not is_find:
		yestodayDate = now - oneday
		yestody = str(yestodayDate)
		# 将昨天日期转换为规定的字符串格式
		times = time.strptime(yestody, '%Y-%m-%d')
		str_yestoday = time.strftime('%Y%m%d', times)
		if is_trade_day(str_yestoday):
			is_find = True
			ret = str_yestoday
		now = yestodayDate
	times = time.strptime(ret, '%Y%m%d')
	ret_time = time.strftime('%Y-%m-%d', times)
	ret_time = datetime.date(*map(int, ret_time.split('-')))
	return ret, ret_time
def is_trade_day(date):
	pro = ts.pro_api()
	df = pro.trade_cal(exchange='', start_date=date, end_date=date)
	value = df.is_open[0]
	return value == 1

#valid_stock('2018-3-1')