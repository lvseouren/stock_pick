import re
import tushare as ts
import os

# mysql
mysql_user = 'root'
mysql_password = 'abc123'
mysql_database_name = 'test2'

# dir
report_dir = os.getcwd() + '\\report\\'
log_dir = os.getcwd() + '\\log\\'

# filename
filename_3yang_list = '_list_3yang.txt'
filename_2yang_list = '_list_2yang.txt'
filename_3yang = '_3yang.txt'
filename_2yang = '_2yang.txt'
file_winrate = 'winrate_monitor.txt'
filename_2to3 = '_2to3.txt'

ts_inited = False

# limit
strict_level = 3
turnover_threshold_upper_bound = 10
turnover_threshold_lower_bound = 2
change_limit_1 = 5
change_limit_2 = 4

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