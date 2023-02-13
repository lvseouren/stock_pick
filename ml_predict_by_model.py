# 准备当天的实时数据
import datetime
import time

import mysql
import openpyxl
import tushare as ts
import constants
import find_stock

def take_third(elem):
    return elem[2]

def prepare_data():
    find_stock.valid_stock_2to3()

    date = time.strftime('%Y-%m-%d')
    filename = constants.report_dir + date + constants.filename_2to3
    # 遍历所有2进3标的，将所需的数据写入到excel表predict页中
    fp = open(filename, 'r')
    lines = fp.readlines()
    fp.close()

    filename = constants.ml_data_dir + constants.ml_excel_name
    print(filename)
    f = openpyxl.open(filename)
    sheet = f[constants.ml_sheet_name_predict]
    curr_row = 2

    now = datetime.date(*map(int, date.split('-')))
    str_yestoday, yestoday = find_stock.get_pre_trade_day(now)
    str_theday_before_yestoday, theday_before_yestoday = find_stock.get_pre_trade_day(yestoday)
    conn = mysql.connector.connect(user=constants.mysql_user, password=constants.mysql_password,
                                   database=constants.mysql_database_name)
    cursor = conn.cursor()

    for x in lines:
        data = x.split(' ')
        code = data[0]
        name = data[3]
        # 需要取得date-2,date-1,date,date+1的数据
        # 1,2,3分别对应3yang标的day1,2,3的数据
        cursor.execute(
            'select * from stock_' + code + ' where date=%s or date =%s order by date asc' % (str_yestoday, str_theday_before_yestoday))  # 当天
        value = cursor.fetchall()

        change1 = float(value[0][6])
        change2 = float(value[1][6])
        volume1 = float(value[0][5])
        volume2 = float(value[1][5])
        turnover1 = float(value[0][7])
        turnover2 = float(value[1][7])

        df = ts.get_realtime_quotes(code)
        curr_price = float(df.price[0])
        pre_close = float(df.pre_close[0])
        change3 = round((curr_price - pre_close)/pre_close * 100, 2)
        volume3 = float(df.volume[0])/100
        turnover3 = round(turnover2 * volume3/volume2, 2)

        sheet.cell(curr_row, 1).value = date
        sheet.cell(curr_row, 2).value = code
        sheet.cell(curr_row, 3).value = name

        sheet.cell(curr_row, 4).value = change1
        sheet.cell(curr_row, 5).value = change2
        sheet.cell(curr_row, 6).value = change3
        sheet.cell(curr_row, 7).value = volume1
        sheet.cell(curr_row, 8).value = volume2
        sheet.cell(curr_row, 9).value = volume3
        sheet.cell(curr_row, 10).value = turnover1
        sheet.cell(curr_row, 11).value = turnover2
        sheet.cell(curr_row, 12).value = turnover3
        curr_row += 1
    f.save(filename)

# 从模型中取出x1~9的系数，计算y
def predict():
    filename = constants.ml_data_dir + constants.ml_model_file_name
    fmodel = open(filename, 'r')
    lines = fmodel.readlines()
    fmodel.close()
    model_dict = {}
    for x in lines:
        data = x.split(' ')
        var_name = data[0]
        var_cof = data[1]
        model_dict[var_name] = float(var_cof)
    print('%s' %model_dict)

    filename = constants.ml_data_dir + constants.ml_excel_name
    print(filename)
    f = openpyxl.open(filename)
    sheet = f[constants.ml_sheet_name_predict]

    var_value_dict = {}
    list_result = []
    for row in range(2, sheet.max_row + 1):
        code = sheet.cell(row, 2).value
        name = sheet.cell(row, 3).value
        var_value_dict['x1'] = sheet.cell(row, 4).value
        var_value_dict['x2'] = sheet.cell(row, 5).value
        var_value_dict['x3'] = sheet.cell(row, 6).value
        var_value_dict['x4'] = sheet.cell(row, 7).value
        var_value_dict['x5'] = sheet.cell(row, 8).value
        var_value_dict['x6'] = sheet.cell(row, 9).value
        var_value_dict['x7'] = sheet.cell(row, 10).value
        var_value_dict['x8'] = sheet.cell(row, 11).value
        var_value_dict['x9'] = sheet.cell(row, 12).value

        y = 0
        for key in var_value_dict:
            y += var_value_dict[key] * model_dict[key]
        y = round(y, 2)
        print('%s %s 预测下一交易日最大涨幅为:%s%%' %(code, name, y))
        list_result.append([code, name, y])
        sheet.cell(row, 13).value = y
    f.save(filename)

    list_result.sort(key=take_third, reverse=True)
    # print("%s" %list_result)
    print('\n\n')
    today = sheet.cell(2, 1).value
    filename = constants.ml_report_dir + today + constants.ml_predict_report_filename
    fp = open(filename, 'w')
    for x in list_result:
        str = '%s %s 预测涨幅：%s%%\n' %(x[0], x[1], x[2])
        print(str)
        fp.write(str)
    fp.close()

# prepare_data()
predict()