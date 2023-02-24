#每天下午三点之后进行股票数据添加到数据库，这个文件一般只需要每天执行一次，也可以用来补行情，如果数据库缺少那天的数据的话，只需修改new_time就行，如下示例
import tushare as ts
import mysql.connector
import re,time
import constants
#每天行情出来了之后，插入当天的行情到每支股票的每个表格中
def everystock():
	#获取所有股票列表
	pro = ts.pro_api()
	stock_info = pro.stock_basic()
	#获取股票代码列
	codes = stock_info.symbol
	#连接数据库
	conn = mysql.connector.connect(user=constants.mysql_user, password=constants.mysql_password, database=constants.mysql_database_name)
	cursor = conn.cursor()
	#获取当前时间
	new_time = time.strftime('%Y-%m-%d')
	# new_time = '2023-02-10'
	# end_time = '2023-01-13'
	a = 0

	# test = ts.get_today_all()

	##使用for循环遍历所有的股票
	for x in range(0,len(stock_info)):
		code = codes[x]
		try:
			if constants.stock_filter_all(code):
				#获取单只股票当天的行情
				df = ts.get_hist_data(code, start=new_time,end=new_time)
				#将时间转换格式
				times = time.strptime(new_time,'%Y-%m-%d')
				time_new = time.strftime('%Y%m%d',times)
				#将当天的行情插入数据库
				mysqlCmd = 'insert into stock_'+code+ ' (date,open,close,high,low,volume,p_change, turnover) values (%s,%s,%s,%s,%s,%s,%s,%s)' % (time_new,df.open[0],df.close[0],df.high[0],df.low[0],df.volume[0],df.p_change[0], df.turnover[0])
				# mysqlCmd = 'update stock_'+ code + ' set turnover=%s where date =%s' %(df.turnover[0], time_new)
				cursor.execute(mysqlCmd)
					# mysqlCmd = 'update stock_'+ code + ' set turnover=%s, open =%s, close=%s, high =%s, low=%s,volume=%s,p_change=%s where date =%s' %(df.turnover[0], df.open[i],df.close[i],df.high[i],df.low[i],df.volume[i],df.p_change[i], time_new)
				
				print('%s的数据插入完成'%code)
				a += 1
		except:
			print('%s无行情或者数据库已经存在当天的数据'%code)
	df = ts.get_hist_data('sh', start=new_time, end=new_time)
	# 将时间转换格式
	times = time.strptime(new_time, '%Y-%m-%d')
	time_new = time.strftime('%Y%m%d', times)
	# 将当天的行情插入数据库
	mysqlCmd = 'insert into stock_' + code + ' (date,open,close,high,low,volume,p_change, turnover) values (%s,%s,%s,%s,%s,%s,%s,%s)' % (
	time_new, df.open[0], df.close[0], df.high[0], df.low[0], df.volume[0], df.p_change[0], 0)
	cursor.execute(mysqlCmd)

	print('%s的数据插入完成' % code)
	#统计当天插入数据库的股票数量
	dir_log = constants.log_dir
	filename = dir_log + new_time +'.log'
	flog = open(filename,'w')
	flog.write('今天的行情插入完成%s条'%a)
	#print('今天的行情插入完成%s条'%a)
	flog.close()
	conn.commit()
	conn.close()
	cursor.close()

everystock()
