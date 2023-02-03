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
    else:
        return constants.get_date_str_for_filename(yestoday)

def get_filename_by_strategy(strategy):
    if strategy == constants.strategy_3yang or strategy == constants.strategy_3yang1tiao:
        return constants.filename_3yang_list
    elif strategy == constants.strategy_2yang:
        return constants.filename_2yang_list

def cal_strategy_winrate(strategy):
    filename = ''
    # strategy = constants.strategy_3yang1tiao
    dates = time.strftime('%Y-%m-%d')
    date_str = get_date_str_by_strategy(strategy, dates)
    filename = constants.report_dir + date_str + get_filename_by_strategy(strategy)
    win_rates.realtime_overall_winrate(strategy, False, filename)

cal_strategy_winrate(constants.strategy_3yang)
cal_strategy_winrate(constants.strategy_3yang1tiao)
cal_strategy_winrate(constants.strategy_2yang)
