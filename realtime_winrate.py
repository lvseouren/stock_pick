import datetime
import win_rates,find_stock
import constants
import time

def get_date_str_by_strategy(strategy, dates):
    now = datetime.date(*map(int, dates.split('-')))
    yestoday_str, yestoday = find_stock.get_pre_trade_day(now)
    if strategy == constants.strategy_3yang:
        return constants.get_date_str_for_filename(yestoday)
    elif strategy == constants.strategy_3yang1tiao:
        yestoday_str, yestoday = find_stock.get_pre_trade_day(yestoday)
        return constants.get_date_str_for_filename(yestoday)

filename = ''
strategy = constants.strategy_3yang
# strategy = constants.strategy_3yang1tiao
dates = time.strftime('%Y-%m-%d')
date_str = get_date_str_by_strategy(strategy, dates)
filename = constants.report_dir + date_str + constants.filename_3yang_list
win_rates.realtime_overall_winrate(strategy, False, filename)