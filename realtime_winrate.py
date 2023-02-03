import time

import win_rates
import constants

todays = time.strftime('%Y-%m-%d')
win_rates.cal_strategy_winrate(constants.strategy_3yang, todays)
win_rates.cal_strategy_winrate(constants.strategy_3yang1tiao, todays)
win_rates.cal_strategy_winrate(constants.strategy_2yang, todays)
