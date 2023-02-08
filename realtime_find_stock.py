import time
import datetime

import mysql

import constants
import tushare as ts
import find_stock
import email_sender

#获取2阳标的最新数据，判断其当前是否满足3阳特征
def valid_stock_2to3():
    new_time = time.strftime('%Y-%m-%d')
    filename = constants.report_dir + new_time + constants.filename_2to3
    ftoday = open(filename, 'w')
    # ftoday.write('以下为满足特征的标的列表：\n')
    # read txt method three
    now = datetime.date(*map(int, new_time.split('-')))
    yestodayStr, yestoday = find_stock.get_pre_trade_day(now)
    yestodayStr = time.strptime(yestodayStr, '%Y%m%d')
    yestodayStr = time.strftime('%Y-%m-%d', yestodayStr)
    filename = constants.report_dir + yestodayStr + constants.filename_2yang_list
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
            curr_change = round((curr_price - close)/close * 100, 2)
            if curr_change > constants.change_limit_2to3:
                print('%s %s涨幅(%s)超过阈值(%s), pass' %(code, name, curr_change, constants.change_limit_2to3))
                continue

            curr_volume = float(df.volume[0])/100

            if volume < curr_volume and close < curr_price:
                count+=1
                ftoday.write('%s %s %s %s(涨幅:%s)\n' %(code, curr_price, curr_volume, df.name[0], curr_change))
                print('%s %s满足特征' %(code, name))
                list.append([code, name])
            else:
                str = ''
                if volume > curr_volume:
                    str = '成交量,'
                if curr_price < close:
                    str=str+'价格'
                print('%s %s不满足(%s)， volume=%s(昨日%s),price=%s(昨日close=%s)' %(code, name, str, curr_volume, volume, curr_price, close))

        except:
            print('%s无行情' % code)
    str = '\n共找到%s支满足特征的标的' %count
    print(str)
    print("\n%s" % list)
    # ftoday.write(str)
    ftoday.close()

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
                continue
            else:
                print('%s %s涨幅(%s)不在范围内[%s,%s], pass' % (code, name, curr_change, constants.change_limit_3yang1tiao_lower_bound, constants.change_limit_3yang1tiao_upper_bound))


        except:
            print('%s无行情' % code)
    str = '\n%s支股票中共找到%s支满足特征的标的' % (len(lines),count)
    print(str)
    # ftoday.write(str)
    ftoday.close()

def valid_stock_3yang():
    dates = time.strftime('%Y-%m-%d')
    dir_log = constants.log_dir
    filename = dir_log + dates + '.log'
    flog = open(filename, 'w')
    errorFileName = dir_log + dates + '_error.log'
    f_err_log = open(errorFileName, 'w')
    filename = constants.report_dir + dates + constants.filename_3yang_list
    flist_3yang = open(filename, 'w')
    # 先将字符串格式的时间转换为时间格式才能计算昨天的日期
    now = datetime.date(*map(int, dates.split('-')))
    # oneday = datetime.timedelta(days=1)
    # yestody = str(now - oneday)
    # # 将昨天日期转换为规定的字符串格式
    # times = time.strptime(yestody, '%Y-%m-%d')
    # str_yestoday = time.strftime('%Y%m%d', times)
    str_yestoday, yestoday = find_stock.get_pre_trade_day(now)
    str_theday_before_yestoday, theday_before_yestoday = find_stock.get_pre_trade_day(yestoday)

    flog.write('执行的时间前一天是%s\n' % str_yestoday)
    # 将想要查找的日期转换为规定的字符串格式
    str_today = time.strptime(dates, '%Y-%m-%d')
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
                curr_change = (curr_price - close2) / close2 * 100
                curr_volume = float(df.volume[0]) * 0.01

                if curr_change > constants.change_limit_2to3:
                    continue

                # if code == '000565':
                # 	print('wtf')

                if find_stock.isSatisfy_3yang(curr_open, curr_price, curr_volume, curr_change, opens2, close2, volume2, p_change2, opens3,
                                   close3, volume3, p_change3):
                    flist_3yang.write('%s %s %s %s\n' % (code, curr_price, curr_volume, name))

            except:
                # 之前有次sql语句出错了，order by后面没加date，每次寻找都是0支，找了半个多小时才找出来是sql语句的问题
                f_err_log.write(
                    '%s停牌无数据,或者请查看sql语句是否正确\n' % value_code[i][0])  # 一般不用管，除非执行好多天的数据都为0时那可能输sql语句有问题了

valid_stock_2to3()
print('\n\n\n')
# valid_stock_3yang()
# valid_stock_3yang1tiao()
new_time = time.strftime('%Y-%m-%d')
subject = '%s 2进3标的列表' % new_time
filename = constants.report_dir + new_time + constants.filename_2to3
email_sender.send_email(subject, [filename], ["2进3标的数据"])