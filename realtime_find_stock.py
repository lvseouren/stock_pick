import time
import datetime

import mysql
import openpyxl

import constants
import tushare as ts
import find_stock
import email_sender

#遍历1yang集合，找出满足2yang的标的
def valid_stock_1to2():
    return

def valid_stock_3yang1tiao():
    new_time = time.strftime('%Y-%m-%d')
    filename = constants.report_dir + new_time + constants.filename_3yang1tiao
    ftoday = open(filename, 'w')
    # ftoday.write('以下为满足特征的标的列表：\n')
    # read txt method three
    now = datetime.date(*map(int, new_time.split('-')))
    yestodayStr, yestoday = find_stock.get_pre_trade_day(now)
    yestodayStr = time.strptime(yestodayStr, '%Y%m%d')
    yestodayStr = time.strftime('%Y-%m-%d', yestodayStr)
    filename = constants.report_dir + yestodayStr + constants.filename_3yang_list
    fp = open(filename, "r")
    lines = fp.readlines()
    fp.close()

    count = 0
    list = []
    ##使用for循环遍历所有的2yang股票
    for x in lines:
        data = x.split(' ')
        code = data[0]
        close = float(data[1])
        volume = float(data[2])
        name = data[3]
        try:
            # 获取单只股票当天的行情
            df = ts.get_realtime_quotes(code)

            curr_price = float(df.price[0])
            curr_change = round((curr_price - close) / close * 100, 2)
            if curr_change >= constants.change_limit_3yang1tiao_lower_bound and curr_change <= constants.change_limit_3yang1tiao_upper_bound:
                count+=1
                ftoday.write('%s %s\n' % (code, df.name[0]))
                print('%s %s满足特征' % (code, name))
                list.append([code, name, curr_price, curr_change])
                continue
            else:
                print('%s %s涨幅(%s)不在范围内[%s,%s], pass' % (code, name, curr_change, constants.change_limit_3yang1tiao_lower_bound, constants.change_limit_3yang1tiao_upper_bound))


        except:
            print('%s无行情' % code)
    str = '\n%s支股票中共找到%s支满足特征的标的' % (len(lines),count)
    print(str)
    print(list)
    # ftoday.write(str)
    ftoday.close()

def valid_stock_3yang():
    date = time.strftime('%Y-%m-%d')
    dir_log = constants.log_dir
    filename = dir_log + date + '.log'
    flog = open(filename, 'w')
    errorFileName = dir_log + date + '_error.log'
    f_err_log = open(errorFileName, 'w')
    filename = constants.report_dir + date + '_realtime' + constants.filename_3yang_list
    flist_3yang = open(filename, 'w')
    # 先将字符串格式的时间转换为时间格式才能计算昨天的日期
    now = datetime.date(*map(int, date.split('-')))
    str_yestoday, yestoday = find_stock.get_pre_trade_day(now)
    str_theday_before_yestoday, theday_before_yestoday = find_stock.get_pre_trade_day(yestoday)

    flog.write('执行的时间前一天是%s\n' % str_yestoday)
    # 将想要查找的日期转换为规定的字符串格式
    str_today = time.strptime(date, '%Y-%m-%d')
    today = time.strftime('%Y%m%d', str_today)
    flog.write('执行的时间是%s\n' % today)
    # 连接数据库
    conn = mysql.connector.connect(user=constants.mysql_user, password=constants.mysql_password,
                                   database=constants.mysql_database_name)
    cursor = conn.cursor()
    # 查找allstock表获取所有股票代码
    cursor.execute('select code, name from allstock')
    value_code = cursor.fetchall()
    a = 0
    # 遍历所有股票
    for i in range(0, len(value_code)):
        code = value_code[i][0]
        name = value_code[i][1]
        if not constants.stock_is_st(name) and constants.stock_filter_all(code):
            # 查询所有匹配到的股票，将今天与昨天的数据对比
            try:
                cursor.execute(
                    'select * from stock_' + code + ' where date=%s or date =%s order by date desc' % (
                        str_yestoday, str_theday_before_yestoday))  # 当天
                # cursor.execute('select * from stock_'+ value_code[i][0]+ ' where date=%s or date =%s'%('20180315','20180314'))
                value = cursor.fetchall()

                # 昨天的。。。。。
                opens2 = float(value[0][1])
                close2 = float(value[0][2])
                volume2 = float(value[0][5])
                p_change2 = float(value[0][6])

                # 前天的。。。。。
                opens3 = float(value[1][1])
                close3 = float(value[1][2])
                volume3 = float(value[1][5])
                p_change3 = float(value[1][6])
                str = '检查%s是否满足特征...\n' % (code)
                flog.write(str)
                print(str)

                df = ts.get_realtime_quotes(code)

                curr_open = float(df.open[0])
                curr_price = float(df.price[0])
                curr_change = round((curr_price - close2) / close2 * 100, 2)
                curr_volume = float(df.volume[0]) * 0.01

                if curr_change > constants.change_limit_2to3:
                    continue

                # if code == '000565':
                # 	print('wtf')

                if find_stock.isSatisfy_3yang(curr_open, curr_price, curr_volume, curr_change, opens2, close2, volume2, p_change2, opens3,
                                   close3, volume3, p_change3):
                    flist_3yang.write('%s %s(%s) %s %s\n' % (code, curr_price, curr_change, curr_volume, name))

            except:
                # 之前有次sql语句出错了，order by后面没加date，每次寻找都是0支，找了半个多小时才找出来是sql语句的问题
                f_err_log.write(
                    '%s停牌无数据,或者请查看sql语句是否正确\n' % value_code[i][0])  # 一般不用管，除非执行好多天的数据都为0时那可能输sql语句有问题了

def findstock_safe_3yang():
    for i in range(1, 5):
        findstock_3yang_before_n_day(i)

def findstock_3yang_before_n_day(n):
	today = time.strftime('%Y-%m-%d')
	now = datetime.date(*map(int, today.split('-')))
	target_date_str, target_date = find_stock.get_trade_day_before_n_day(now, n)
	target_date_str = constants.get_date_str_for_filename(target_date)
	findstock_not_startup_3yang(target_date_str)

# 在最近的3yang标的中寻找没怎么涨的
def findstock_not_startup_3yang(target_date_str, filer=constants.stock_filter_all):
    today = time.strftime('%Y-%m-%d')
    # if not find_stock.is_trade_day(constants.change_date_str_format(today, '%Y-%m-%d', '%Y%m%d')):
    #     return
    d1 = datetime.date(*map(int, today.split('-')))
    d2 = datetime.date(*map(int, target_date_str.split('-')))
    diff = find_stock.get_target_day_count(d2, d1)

    stockListFileName = constants.report_dir + target_date_str + constants.filename_3yang_list
    fp = open(stockListFileName, "r")
    lines = fp.readlines()
    fp.close()

    flog = open(constants.stats_dir + target_date_str + 'to%s_maybegood.txt' % (today), 'w')

    count = 0
    valid_count = 0
    list_goods = []
    for x in lines:
        data = x.split(' ')
        code = data[0]
        if not filer(code):
            continue
        close = float(data[1])
        name = data[3]
        try:
            # 获取单只股票当天的行情
            df = ts.get_realtime_quotes(code)
            high = float(df.high[0])
            if high == 0:
                continue

            valid_count += 1
            change = round((high - close) / close * 100, 2)

            open_today = float(df.open[0])
            change_open = round((open_today - close) / close * 100, 2)

            close_today = float(df.price[0])
            change_close = round((close_today - close) / close * 100, 2)

            if change < 2 and change > 0:
                industry = find_stock.get_stock_industry(code)
                list_goods.append([industry, code, name, change])

            if close < high and change > 1:
                count += 1
            str = '%s %s 涨幅：%s%%' % (code, df.name[0], change)
            flog.write(str)
            flog.write('\n')
            print(str)
        except:
            print('%s无行情' % code)

    print(stockListFileName)
    str = '\n以下标的或有机会:\n'
    print(str)
    flog.write(str)
    for x in list_goods:
        print(x)
        flog.write('%s\n' % x)
    flog.close()

findstock_safe_3yang()
find_stock.valid_stock_2to3()
print('\n\n\n')
# valid_stock_3yang1tiao()
# print('\n\n\n')
# valid_stock_3yang()

# new_time = time.strftime('%Y-%m-%d')
# subject = '%s 2进3标的列表' % new_time
# filename = constants.report_dir + new_time + constants.filename_2to3