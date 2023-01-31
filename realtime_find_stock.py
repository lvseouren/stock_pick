import time
import datetime
import constants
import tushare as ts
import find_stock
import email_sender

#获取2阳标的最新数据，判断其当前是否满足3阳特征
def valid_stock():
    new_time = time.strftime('%Y-%m-%d')
    filename = constants.report_dir + new_time + '_2to3.txt'
    ftoday = open(filename, 'w')
    # read txt method three
    now = datetime.date(*map(int, new_time.split('-')))
    yestodayStr, yestoday = find_stock.get_pre_trade_day(now)
    yestodayStr = time.strptime(yestodayStr, '%Y%m%d')
    yestodayStr = time.strftime('%Y-%m-%d', yestodayStr)
    filename = constants.report_dir + yestodayStr + "_list.txt"
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
        try:
            # 获取单只股票当天的行情
            df = ts.get_realtime_quotes(code)
            curr_volume = float(df.volume[0])/100
            curr_price = float(df.price[0])
            if volume < curr_volume and close < curr_price:
                count+=1
                ftoday.write('%s\n' %code)
                print('%s满足特征' %code)

        except:
            print('%s无行情' % code)
    print('共找到%s支满足特征的标的' %count)
    ftoday.close()

valid_stock()
new_time = time.strftime('%Y-%m-%d')
subject = '%s 2进3标的列表' % new_time
filename = constants.report_dir + new_time + '_2to3.txt'
email_sender.send_email(subject, filename)