import datetime
import time
import mysql
import constants
import find_stock

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

def validate(date):
    now = datetime.date(*map(int, date.split('-')))
    str_yestoday, yestoday = find_stock.get_pre_trade_day(now)
    str_yestoday_filename = constants.change_date_str_from_database_to_filename(str_yestoday)

    filename = constants.ml_report_dir + str_yestoday_filename + constants.ml_predict_report_filename
    fp = open(filename, 'r')
    lines = fp.readlines()
    fp.close()
    filename = constants.ml_report_dir + str_yestoday_filename + constants.ml_predict_validate_report_filename
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

        change = (high - pre_close)/pre_close * 100
        change = round(change, 2)
        x = x.replace('\n', '')
        str = '%s 实际最高涨幅：%s%%\n' %(x, change)
        print(str)
        fp.write(str)

def validate_today():
    today = time.strftime('%Y-%m-%d')
    validate(today)
    validate_3yang1tiao(today)

validate_today()