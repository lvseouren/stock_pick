import datetime
import os
import time
import mysql
import constants
import find_stock
import tushare as ts

def validate_3yang1tiao(date):
    now = datetime.date(*map(int, date.split('-')))
    str_yestoday, yestoday = find_stock.get_pre_trade_day(now)
    str_yestoday_filename = constants.change_date_str_from_database_to_filename(str_yestoday)

    filename = constants.ml_report_dir + str_yestoday_filename + constants.ml_predict_report_filename_3yang1tiao
    fp = open(filename, 'r')
    lines = fp.readlines()
    fp.close()
    filename = constants.ml_report_dir + str_yestoday_filename + constants.ml_predict_validate_report_filename_3yang1tiao
    fp = open(filename, 'w')

    conn = mysql.connector.connect(user=constants.mysql_user, password=constants.mysql_password,
                                   database=constants.mysql_database_name)
    cursor = conn.cursor()

    date_for_database = constants.change_date_str_form_filename_to_database(date)
    for x in lines:
        data = x.split(' ')
        if len(data) > 3:
            return
        code = data[0]
        cursor.execute(
            'select * from stock_' + code + ' where date=%s or date =%s order by date asc' % (
                date_for_database, str_yestoday))  # 当天

        value = cursor.fetchall()
        high = float(value[1][3])
        pre_close = float(value[0][2])

        change = (high - pre_close) / pre_close * 100
        change = round(change, 2)
        x = x.replace('\n', '')
        str = '%s 实际最高涨幅：%s%%\n' % (x, change)
        print(str)
        fp.write(str)

def validate_by_file(date, filename, outputfile, is_use_high=False):
    if not os.path.exists(filename):
        return
    outputfile.write('\n')
    conn = mysql.connector.connect(user=constants.mysql_user, password=constants.mysql_password,
                                   database=constants.mysql_database_name)
    cursor = conn.cursor()
    fp = open(filename, 'r')
    lines = fp.readlines()
    fp.close()
    now = datetime.date(*map(int, date.split('-')))
    str_yestoday, yestoday = find_stock.get_pre_trade_day(now)
    date_for_database = constants.change_date_str_form_filename_to_database(date)
    for x in lines:
        data = x.split(' ')
        code = data[0]
        cursor.execute(
            'select * from stock_' + code + ' where date=%s or date =%s order by date asc' % (
                date_for_database, str_yestoday))  # 当天

        value = cursor.fetchall()

        high = float(value[1][3]) if len(value) > 1 else -1
        curr_price = float(value[1][2]) if len(value) > 1 else -1
        if high < 0:
            df = ts.get_realtime_quotes(code)
            high = float(df.high)
            curr_price = float(df.price)
        pre_close = float(value[0][2])

        curr_change = (curr_price - pre_close) / pre_close * 100
        change = curr_change
        if is_use_high:
            change = (high - pre_close) / pre_close * 100
        change = round(change, 2)
        curr_change = round(curr_change, 2)
        x = x.replace('\n', '')
        type_str = '最高' if is_use_high else '收盘'
        industry = find_stock.get_stock_industry(code)
        str = '(%s)%s 实际%s涨幅：%s%%;当前涨幅:%s%%' % (industry, x, type_str, change, curr_change)
        print(str)
        str+='\n'
        outputfile.write(str)
    print('\n')
    outputfile.write('\n')

def validate(date):
    now = datetime.date(*map(int, date.split('-')))
    str_yestoday, yestoday = find_stock.get_pre_trade_day(now)
    str_yestoday_filename = constants.change_date_str_from_database_to_filename(str_yestoday)

    fp = open(constants.ml_report_dir + str_yestoday_filename + constants.ml_predict_validate_report_filename, 'w')
    filename = constants.ml_report_dir + str_yestoday_filename + constants.ml_predict_report_filename_3yang
    validate_by_file(date, filename, fp)
    filename2 = constants.get_predict_validate_filename(str_yestoday_filename, constants.strategy_3yang1tiao)
    validate_by_file(date, filename2, fp)
    filename3 = constants.get_predict_validate_filename(str_yestoday_filename, constants.strategy_3yang1tiao, 'hushen')
    validate_by_file(date, filename3, fp)
    filename4 = constants.get_predict_validate_filename(str_yestoday_filename, constants.strategy_3yang, 'hushen')
    validate_by_file(date, filename4, fp, True)
    filename5 = constants.get_predict_validate_filename(str_yestoday_filename, constants.strategy_3yang)
    validate_by_file(date, filename5, fp, True)
    fp.close()

def validate_today():
    today = time.strftime('%Y-%m-%d')
    # today = '2023-02-14'
    validate(today)
    # validate_3yang1tiao(today)

validate_today()