import mysql.connector
import tushare as ts
#将所有的股票名称和股票代码、行业、地区写入到名为allstock的表中，这个文件只需要执行一次

#通过tushare库获取所有的A股列表
pro = ts.pro_api()
stock_info = pro.stock_basic()
#连接数据库
conn = mysql.connector.connect(user='root',password='abc123',database='test')
cursor = conn.cursor()

sqlCmd = 'create table allstock (code varchar(32),name varchar(32),industry varchar(32),area varchar(32),unique(code))'
print(sqlCmd)

cursor.execute(sqlCmd)
codes = stock_info.symbol
names = stock_info.name
industrys = stock_info.industry
areas = stock_info.area
#通过for循环遍历所有股票，然后拆分获取到需要的列，将数据写入到数据库中
a=0
for i in range(0,len(stock_info)):
	cursor.execute('insert into allstock (code,name,industry,area) values (%s,%s,%s,%s)',(codes[i],names[i],industrys[i],areas[i]))
	a += 1
#统计所有A股数量
print('共获取到%d支股票'%a)

conn.commit()
cursor.close()
conn.close()