import time

import constants
import email_sender
import find_stock
from realtime_find_stock import valid_stock_3yang1tiao

find_stock.valid_stock_2to3()
print('\n\n\n')
# valid_stock_3yang()
valid_stock_3yang1tiao()
new_time = time.strftime('%Y-%m-%d')
subject = '%s 2进3标的列表' % new_time
filename = constants.report_dir + new_time + constants.filename_2to3
filename2 = constants.ml_report_dir + new_time + '_' + constants.ml_sheet_name_predict + '_' + constants.ml_predict_report_filename_3yang1tiao
email_sender.send_email(subject, [filename, filename2], ["2进3标的数据", '预测数据'])