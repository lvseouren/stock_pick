import constants,time
import tushare as ts
import wechat_sender

def print_sh_info():
    df = ts.get_realtime_quotes('sh')
    price = float(df.price[0])
    pre_close = float(df.pre_close[0])
    diff = round(price - pre_close, 2)
    symbol = '+' if diff >= 0 else '-'
    change = round(diff / pre_close * 100, 2)
    print('上证指数:%s, %s%s(%s)\n' % (price, symbol, diff, change))

def check_position(is_need_alert=False):
    stockListFileName = constants.data_dir + constants.filename_position
    fp = open(stockListFileName, "r")
    lines = fp.readlines()
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
                str = '%s %s:%s(%s)' %(code, name, price, change)
                print(str)
                if is_need_alert and change > 2:
                    wechat_sender.send_msg(constants.wechat_target_me, str)
            except:
                print('wtf')
        print('\n\n')
        time.sleep(5)

check_position()