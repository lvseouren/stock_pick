import constants,time
import tushare as ts
import wechat_sender

def print_sh_info():
    try:
        df = ts.get_realtime_quotes('sh')
        price = float(df.price[0])
        pre_close = float(df.pre_close[0])
        diff = round(price - pre_close, 2)
        change = round(diff / pre_close * 100, 2)
        print('上证指数:%s, %s(%s)\n' % (price, diff, change))
    except:
        print('wtf')

def check_position(is_need_alert=False):
    stockListFileName = constants.data_dir + constants.filename_position
    fp = open(stockListFileName, "r")
    lines = fp.readlines()
    pre_volume = {}

    # statistic
    timer_minute = 0
    volome_minute = {}
    pre_volume_minite = {}
    for x in lines:
        data = x.split(' ')
        code = data[0]
        pre_volume[code] = 0
        volome_minute[code] = 0
        pre_volume_minite[code] = 0

    while True:
        print_sh_info()
        for x in lines:
            data = x.split(' ')
            code = data[0]
            name = data[1].replace('\n','')
            try:
                # 获取单只股票当天的行情
                df = ts.get_realtime_quotes(code)
                price = float(df.price[0])
                pre_close = float(df.pre_close[0])
                change = round((price - pre_close)/pre_close * 100, 2)
                curr_volume = int(int(df.volume[0]) * 0.01)
                add_volume = curr_volume - pre_volume[code] if pre_volume[code] > 0 else 0
                str = '%s %s:%s(%s%%),volume:%s(+%s)' %(code, name, price, change, curr_volume, add_volume)
                print(str)
                pre_volume[code] = curr_volume

                volome_minute[code] += add_volume
                if timer_minute >= 60:
                    add = volome_minute[code] - pre_volume_minite[code]
                    time_str = df.time[0]
                    data = time_str.split(':')
                    time_str = '%s:%s' %(data[0], data[1])
                    symbol = '+' if add > 0 else ''
                    str = '%s 股价：%s(%s%%); 一分钟成交量为:%s(%s%s)手 总成交量为:%s手\n' % (time_str, price, change, volome_minute[code], symbol, add, curr_volume)
                    print(str)
                    pre_volume_minite[code] = volome_minute[code]
                    volome_minute[code] = 0
                    filename_stock = constants.log_dir + '%s_%s.txt' % (code, name)
                    file = open(filename_stock, 'a')
                    file.write(str)
                    file.close()
                    if x == lines[len(lines)-1]:
                        timer_minute = 0

                if is_need_alert and change > constants.position_alert_change:
                    wechat_sender.send_msg(constants.wechat_target_me, str)
            except:
                print('wtf')
        print('\n\n')
        time.sleep(constants.check_position_interval)
        timer_minute += constants.check_position_interval

check_position()