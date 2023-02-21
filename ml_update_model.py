import datetime
import time

import constants
import find_stock
import ml_write_excel_data
from MachineLearning import linear_regress

def update_model():
    time.sleep(3)
    # 写入今天的数据(昨日3yang今天的涨幅)
    date = time.strftime('%Y-%m-%d')
    now = datetime.date(*map(int, date.split('-')))
    str_yestoday, yestoday = find_stock.get_pre_trade_day(now)
    str_yestoday = constants.change_date_str_from_database_to_filename(str_yestoday)
    time.sleep(3)
    is_dirty = ml_write_excel_data.prepare_data(str_yestoday, str_yestoday)
    if is_dirty:
        linear_regress.mul_lr_3yang()

    time.sleep(3)
    str_yestoday_yestoday, yestoday_yestoday = find_stock.get_pre_trade_day(yestoday)
    str_yestoday_yestoday = constants.change_date_str_from_database_to_filename(str_yestoday_yestoday)
    time.sleep(3)
    is_dirty = ml_write_excel_data.prepare_data_3yang1tiao(str_yestoday_yestoday, str_yestoday_yestoday)
    if is_dirty:
        linear_regress.mul_lr_3yang1tiao()

# update_model()
# linear_regress.mul_lr_3yang1tiao()