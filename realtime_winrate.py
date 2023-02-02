import win_rates
import constants

filename = constants.report_dir + '2023-02-01' + constants.filename_3yang_list
strategy = '3yang'
win_rates.realtime_overall_winrate(strategy, filename)