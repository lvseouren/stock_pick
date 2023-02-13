# -*- coding:utf-8 -*-
import datetime
import mysql
import openpyxl
import constants
import find_stock
from MachineLearning import linear_regress

def write_to_excel(sheet, date):
    last_date = sheet.cell(sheet.max_row, 1).value
    if last_date == date:
        return False

    filename = constants.report_dir + date + constants.filename_3yang_list
    fp = open(filename, "r")
    lines = fp.readlines()
    fp.close()
    # 第1、2行为表头
    # 第3行开始写入数据
    # 遍历3yang标的，取得需要的数据，写入对应的xi，取得其次日的最高涨幅写入y

    now = datetime.date(*map(int, date.split('-')))
    today = constants.get_date_str_for_datebase(now)
    str_yestoday, yestoday = find_stock.get_pre_trade_day(now)
    str_theday_before_yestoday, theday_before_yestoday = find_stock.get_pre_trade_day(yestoday)
    str_next_day, next_day = find_stock.get_next_trade_day(now)
    conn = mysql.connector.connect(user=constants.mysql_user, password=constants.mysql_password,
                                   database=constants.mysql_database_name)
    cursor = conn.cursor()
    curr_row = sheet.max_row+1
    for x in lines:
        data = x.split(' ')
        code = data[0]
        name = data[3]

        # 需要取得date-2,date-1,date,date+1的数据
        # 1,2,3分别对应3yang标的day1,2,3的数据
        cursor.execute(
            'select * from stock_' + code + ' where date=%s or date =%s or date =%s or date =%s order by date asc' % (today,
                str_yestoday, str_theday_before_yestoday, str_next_day))  # 当天
        value = cursor.fetchall()

        change1 = float(value[0][6])
        change2 = float(value[1][6])
        change3 = float(value[2][6])
        volume1 = float(value[0][5])
        volume2 = float(value[1][5])
        volume3 = float(value[2][5])
        turnover1 = float(value[0][7])
        turnover2 = float(value[1][7])
        turnover3 = float(value[2][7])
        close3 = float(value[2][2])
        high = 0
        if len(value) > 3:
            high = float(value[3][3])
        high_change = round((high - close3)/close3 * 100, 2)
        print('%s %s %s最高涨幅为:%s' %(code, name, str_next_day, high_change))

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
        sheet.cell(curr_row, 13).value = high_change

        curr_row += 1

    return

def prepare_data(starttime, endtime):
    filename = constants.ml_data_dir + constants.ml_excel_name
    print(filename)
    f = openpyxl.open(filename)
    sheet = f[constants.ml_sheet_name_data]
    # starttime = '20230209'
    # endtime = '20230210'
    # df = ts.get_hist_data('sh', starttime, endtime)
    df = constants.get_ts_pro().trade_cal(exchange='', start_date=starttime, end_date=endtime)
    try:
        for i in range(0, len(df.is_open)):
            if df.is_open[i] == 0:
                continue
            # 获取股票日期，并转格式（这里为什么要转格式，是因为之前我2018-03-15这样的格式写入数据库的时候，通过通配符%之后他居然给我把-符号当做减号给算出来了查看数据库日期就是2000百思不得其解想了很久最后决定转换格式）
            date = df.cal_date[i]
            date = constants.change_date_str_format(date, '%Y%m%d', '%Y-%m-%d')
            write_to_excel(sheet, date)
    except:
        print('wtf')
    f.save(filename)

# prepare_data()
# linear_regress.mul_lr()



