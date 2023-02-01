import time
import datetime
import constants
import tushare as ts
import find_stock
import email_sender

#获取2阳标的最新数据，判断其当前是否满足3阳特征
def valid_stock():
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
            curr_change = (curr_price - close)/close * 100
            if curr_change > constants.change_limit_2to3:
                print('%s %s涨幅(%s)超过阈值(%s), pass' %(code, name, curr_change, constants.change_limit_2to3))
                continue

            curr_volume = float(df.volume[0])/100

            if volume < curr_volume and close < curr_price:
                count+=1
                ftoday.write('%s %s %s %s\n' %(code, curr_price, curr_volume, df.name[0]))
                print('%s %s满足特征' %(code, name))
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
    # ftoday.write(str)
    ftoday.close()

valid_stock()
new_time = time.strftime('%Y-%m-%d')
subject = '%s 2进3标的列表' % new_time
filename = constants.report_dir + new_time + constants.filename_2to3
email_sender.send_email(subject, filename, "2进3标的数据")