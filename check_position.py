import constants
import tushare as ts

def check_position():
    stockListFileName = constants.data_dir + constants.filename_position
    fp = open(stockListFileName, "r")
    lines = fp.readlines()
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
            print('%s %s:%s(%s)' %(code, name, price, change))
        except:
            print('wtf')

check_position()