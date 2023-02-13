import datetime
import time
import find_stock
import ml_write_excel_data
from MachineLearning import linear_regress

# 写入今天的数据(昨日3yang今天的涨幅)
date = time.strftime('%Y-%m-%d')
now = datetime.date(*map(int, date.split('-')))
str_yestoday, yestoday = find_stock.get_pre_trade_day(now)
ml_write_excel_data.prepare_data(str_yestoday, str_yestoday)
linear_regress.mul_lr()