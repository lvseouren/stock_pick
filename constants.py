import re
import tushare as ts

# mysql
mysql_user = 'root'
mysql_password = 'abc123'
mysql_database_name = 'test'

# dir
report_dir = 'H:\\GitRoot\\stock_pick\\report\\'
log_dir = 'H:\\GitRoot\\stock_pick\\log\\'

ts_inited = False

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