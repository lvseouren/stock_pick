#这个文件可以联合find_stock单独运行，输入todays的日期可以直接查找当天出现过的股票
import mysql.connector
import constants
import find_stock
#统计当天满足阳包阴所有股票，在设置的这段时间里面有没有出现过类似的行情，并且计算如果出现过，那么那天之后的5天收益率是多少
def rate(todays):
	print(todays)
	#将满足阳包阴的这些股票，以及它们之前满足的时候收益率都写到报告里面方便查看整体情况
	count,a = find_stock.valid_stock(todays)
	dir_repor = constants.report_dir
	filename = dir_repor + todays +'.txt'	
	fp = open(filename,'w')
	fp.write('总共找到%d支满足条件的股票分别是\n%s\n'%(a,count))

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

				if find_stock.isSatisfy_twoyang(opens1, close1, opens2, close2, volume1, volume2, p_change1, p_change2):
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
#rate('2018-03-16')