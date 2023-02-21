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
	filename = constants.report_dir + dates + constants.filename_2yang_list
	flist = open(filename, 'w')
	filename = constants.report_dir + dates + constants.filename_3yang_list
	flist_3yang = open(filename, 'w')

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
			# if not constants.stock_filter_chuangyeban(code):
			# 	continue
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
				turnover1 = float(value[0][7])
				if p_change1 > constants.change_limit_2to3:
					continue

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

				# if code == '000565':
				# 	print('wtf')

				if isSatisfy_twoyang(opens1, close1, opens2, close2, volume1, volume2, p_change1, p_change2, True):
					if not isSatisfy_twoyang(opens2, close2, opens3, close3, volume2, volume3, p_change2, p_change3):
						if turnover1 <= constants.turnover_threshold_upper_bound and turnover1 >= constants.turnover_threshold_lower_bound:
							if p_change1 > constants.change_limit_2yang:
								continue
							flist.write('%s %s %s %s\n' %(code, close1, volume1, name))
							flog.write('%s票%s的开盘价是%s\n' % (code, today, opens1))
							flog.write('%s票%s的收盘价是%s\n' % (code, today, close1))
							flog.write('%s票%s的成交量是%s\n' % (code, today, volume1))
							flog.write('%s票%s的开盘价是%s\n' % (code, str_yestoday, opens2))
							flog.write('%s票%s的收盘价价是%s\n' % (code, str_yestoday, close2))
							flog.write('%s票%s的成交量是%s\n' % (code, str_yestoday, volume2))
							# 将满足条件的股票代码放进列表中，统计当天满足条件的股票
							count.append([code, name])
							a += 1
						else:
							print('%s 换手率为%s不在区间内[%s,%s]' % (code, turnover1, constants.turnover_threshold_lower_bound, constants.turnover_threshold_upper_bound))
					else:
						print("%s 3yang了" % code)
						# 3yang了
						# flist_3yang.write('%s %s %s \n' %(code, close1, volume1))
						# count_3yang.append(code)
				if isSatisfy_3yang(opens1, close1, volume1, p_change1, opens2, close2, volume2, p_change2, opens3, close3, volume3, p_change3):
					flist_3yang.write('%s %s %s %s %s\n' %(code, close1, volume1, name, p_change1))
					count_3yang.append(code)
			except:
				# 之前有次sql语句出错了，order by后面没加date，每次寻找都是0支，找了半个多小时才找出来是sql语句的问题
				f_err_log.write(
					'%s停牌无数据,或者请查看sql语句是否正确\n' % value_code[i][0])  # 一般不用管，除非执行好多天的数据都为0时那可能输sql语句有问题了

	print('总共找到%d支满足条件的股票' % a)
	flog.close()
	f_err_log.close()
	flist.close()
	flist_3yang.close()
	conn.close()
	cursor.close()
	return count, a, count_3yang

#获取2阳标的最新数据，判断其当前是否满足3阳特征
def valid_stock_2to3():
    new_time = time.strftime('%Y-%m-%d')
    filename = constants.report_dir + new_time + constants.filename_2to3
    ftoday = open(filename, 'w')
    # ftoday.write('以下为满足特征的标的列表：\n')
    # read txt method three
    now = datetime.date(*map(int, new_time.split('-')))
    yestodayStr, yestoday = get_pre_trade_day(now)
    yestodayStr = time.strptime(yestodayStr, '%Y%m%d')
    yestodayStr = time.strftime('%Y-%m-%d', yestodayStr)
    filename = constants.report_dir + yestodayStr + constants.filename_2yang_list
    fp = open(filename, "r")
    lines = fp.readlines()
    fp.close()

    count = 0
    list = []
    ##使用for循环遍历所有的2yang股票
    for x in lines:
        data = x.split(' ')
        code = data[0]
        close = float(data[1])
        volume = float(data[2])
        name = data[3]
        try:
            # 获取单只股票当天的行情
            df = ts.get_realtime_quotes(code)

            curr_price = float(df.price[0])
            curr_change = round((curr_price - close)/close * 100, 2)
            curr_high = float(df.high[0])

            if curr_change > constants.change_limit_2to3:
                print('%s %s涨幅(%s)超过阈值(%s), pass' %(code, name, curr_change, constants.change_limit_2to3))
                continue

            curr_volume = float(df.volume[0])/100

            if volume < curr_volume and close < curr_price:
                count+=1
                ftoday.write('%s %s %s %s(涨幅:%s) 最高价:%s\n' %(code, curr_price, curr_volume, df.name[0], curr_change, curr_high))
                print('%s %s满足特征' %(code, name))
                list.append([code, name, curr_price, curr_change])

            else:
                str = ''
                if volume > curr_volume:
                    str = '成交量,'
                if curr_price < close:
                    str=str+'价格'
                print('%s %s不满足(%s)， volume=%s(昨日%s),price=%s(昨日close=%s)' %(code, name, str, curr_volume, volume, curr_price, close))

        except:
            print('%s无行情' % code)
    str = '\n共找到%s支满足特征的标的' %count
    print(str)
    print("\n%s" % list)
    # ftoday.write(str)
    ftoday.close()
    return list

# 在昨天达成3阳的标的中筛选满足“1调”特征的
def find_3yang1tiao(dates):
	return

# 1今天2昨天3前天
def isSatisfy_3yang(open1, close1, volume1, p_change1, open2, close2, volume2, p_change2, open3, close3, volume3, p_change3):
	return isSatisfy_twoyang(open1, close1, open2, close2, volume1, volume2, p_change1, p_change2) and isSatisfy_twoyang(open2, close2, open3, close3, volume2, volume3, p_change2, p_change3, True)

# 2是昨天，1是今天
def isSatisfy_twoyang(opens1, close1, opens2, close2, volume1, volume2, p_change1, p_change2, is_change_limit = False):
	ret = close1 > close2 and p_change2 > 0 and volume1 > volume2

	# 如果结果太多，可以注释掉下面这行，并启用209,210行代码
	ret = ret and close1 > opens1
	# if is_change_limit:
	# 	ret = ret and close1 > opens1 and close2 > opens2
	if ret and is_change_limit:
		ret = ret and p_change1 > 2

	if is_change_limit and ret:
		ret = p_change1 <= constants.get_change_limit()
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
		now = yestodayDate
		if is_trade_day(str_yestoday):
			is_find = True
			ret = str_yestoday
	return ret, now

def get_next_trade_day(now):
	is_find = False
	ret = now
	oneday = datetime.timedelta(days=1)
	while not is_find:
		yestodayDate = now + oneday
		yestody = str(yestodayDate)
		# 将昨天日期转换为规定的字符串格式
		times = time.strptime(yestody, '%Y-%m-%d')
		str_yestoday = time.strftime('%Y%m%d', times)
		now = yestodayDate
		if is_trade_day(str_yestoday):
			is_find = True
			ret = str_yestoday
	return ret, now

# 获取n天前的交易日
def get_trade_day_before_n_day(now, n):
	ret = now
	while n > 0:
		ret, now = get_pre_trade_day(now)
		n -= 1
	return ret, now

def is_trade_day(date):
	if constants.has_cache:
		date = constants.change_date_str_from_database_to_filename(date)
		ret = date in constants.cache_df.index
		return ret
	pro = constants.get_ts_pro()
	df = pro.trade_cal(exchange='', start_date=date, end_date=date)
	value = df.is_open[0]
	return value == 1



def get_target_day_count(start_date, end_date):
	start_date = constants.get_date_str_for_datebase(start_date)
	end_date = constants.get_date_str_for_datebase(end_date)
	pro = constants.get_ts_pro()
	df = pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)
	count = -1
	for x in df.is_open:
		if x == 1:
			count += 1
	return count

#valid_stock('2018-3-1')