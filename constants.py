import re
import tushare as ts
import os,time

# ml
ml_excel_name = 'stock_3yang.xlsx'
ml_excel_name_3yang1tiao = 'stock_3yang1tiao.xlsx'
ml_sheetname_data = 'data'
ml_sheetname_data_hushen = 'data_hushen'
ml_sheet_name_predict = 'predict'
ml_sheet_name_predict_hushen = 'predict_hushen'
ml_model_file_name = 'model_3yang.txt'
ml_model_file_name_hushen = 'model_3yang_hushen.txt'
ml_model_file_name_3yang1tiao = 'model_3yang1tiao.txt'
ml_model_file_name_3yang1tiao_hushen = 'model_3yang1tiao_hushen.txt'
ml_predict_report_filename_3yang = '_predict_3yang.txt'
ml_predict_validate_report_filename = '_predict_validte.txt'
ml_predict_report_filename_3yang1tiao = '_predict_3yang1tiao.txt'
ml_predict_validate_report_filename_3yang1tiao = '_predict_validte_3yang1tiao.txt'

cache_trade_day_data = False
has_cache_trade_day_data = False

def get_predict_validate_filename(date, strategy, type=''):
    if len(type) > 0:
        return ml_report_dir + '%s_predict_%s__predict_%s.txt' %(date, type, strategy)
    else:
        return ml_report_dir + '%s_predict__predict_%s.txt' % (date, strategy)

# mysql
mysql_user = 'root'
mysql_password = 'abc123'
mysql_database_name = 'test2'

# dir
report_dir = os.getcwd() + '\\report\\'
log_dir = os.getcwd() + '\\log\\'
data_dir = os.getcwd() + '\\data\\'
ml_dir = os.getcwd() + "\\MachineLearning"
ml_data_dir = ml_dir + '\\data\\'
ml_report_dir = ml_dir + '\\report\\'
stats_dir = os.getcwd() + '\\statistic\\'

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
change_limit_2yang = 6

change_limit_3yang1tiao_lower_bound = -10
change_limit_3yang1tiao_upper_bound = 2

position_alert_change = 10
check_position_interval = 5

def get_change_limit():
    ret = 20
    if strict_level > 1:
        ret = change_limit_level_2
    if strict_level > 2:
        ret = change_limit_level_3
    return ret

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

def change_date_str_from_database_to_filename(date_str):
    return change_date_str_format(date_str, '%Y%m%d', '%Y-%m-%d')

def change_date_str_form_filename_to_database(date_str):
    return change_date_str_format(date_str, '%Y-%m-%d', '%Y%m%d')

def change_date_str_format(date_str, from_format, target_format):
    date = time.strptime(date_str, from_format)
    return time.strftime(target_format, date)

def get_winrate_filename_by_stategy(strategy):
    filename = data_dir + file_winrate + '_' + strategy + '.txt'
    return filename
