import re
import tushare as ts
import os,time

# ml


# mysql
mysql_user = 'root'
mysql_password = 'abc123'
mysql_database_name = 'test2'

# dir
report_dir = os.getcwd() + '\\report\\'
log_dir = os.getcwd() + '\\log\\'
data_dir = os.getcwd() + '\\data\\'
ml_dir = os.getcwd()
ml_data_dir = ml_dir + '\\data\\'

# strategy
strategy_3yang = '3yang'
strategy_3yang1tiao = '3yang1tiao'
strategy_2yang = '2yang'
strategy_list = [strategy_3yang, strategy_3yang1tiao, strategy_2yang]

# filename
filename_3yang_list = '_list_3yang.txt'
filename_2yang_list = '_list_2yang.txt'
filename_3yang = '_3yang.txt'
filename_2yang = '_2yang.txt'
file_winrate = 'winrate_monitor'
filename_2to3 = '_2to3.txt'
filename_3yang1tiao = '_3yang1tiao.txt'
filename_position = 'position.txt'
filename_ml_data = 'test.xlsx'

ts_inited = False

# wechat
wechat_target_me = '狄拉克海捕鱼人'

# limit
# 默认值
turnover_threshold_upper_bound_default = 100
turnover_threshold_lower_bound_default = 2

strict_level = 2
turnover_threshold_upper_bound = 100
turnover_threshold_lower_bound = 1

change_limit_level_2 = 7
change_limit_level_3 = 5
change_limit_2to3 = 8

change_limit_3yang1tiao_lower_bound = 0
change_limit_3yang1tiao_upper_bound = 2

position_alert_change = 1
check_position_interval = 5

def try_init_ts():
    if not ts_inited:
        ts.set_token('ed4a03d581a87d8a6f95cf1f06d31bec659d785e9bf410008fe91493')
def get_ts_pro():
    try_init_ts()
    return ts.pro_api()

def stock_filter_shenzhen(code):
    return re.match('000', code) or re.match('002', code)

def stock_filter_hushi(code):
    return re.match('600', code)

def stock_filter_hushen(code):
    return stock_filter_hushi(code) or stock_filter_shenzhen(code)

def stock_filter_chuangyeban(code):
    return re.match('300', code) or re.match('301', code)

def stock_filter_all(code):
    return stock_filter_hushen(code) or stock_filter_chuangyeban(code)

def stock_is_st(name):
    if re.findall('st', name) or re.findall('ST', name) or re.findall('St', name):
        return True
    else:
        return False

def get_date_str_for_datebase(date):
    # 将日期转换为规定的字符串格式
    date_str = date.strftime('%Y%m%d')
    return date_str

def get_date_str_for_filename(date):
    # 将昨天日期转换为规定的字符串格式
    date_str = date.strftime('%Y-%m-%d')
    return date_str

def change_date_str_format(date_str, from_format, target_format):
    date = time.strptime(date_str, from_format)
    return time.strftime(target_format, date)

def get_winrate_filename_by_stategy(strategy):
    filename = data_dir + file_winrate + '_' + strategy + '.txt'
    return filename