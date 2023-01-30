import re
import time
from pprint import pprint

import pandas as pd
import requests

#
# class Snowball:
#     xq = 'https://xueqiu.com'
#     # 雪球自选股列表相关json
#     url = {'get': xq + '/v4/stock/portfolio/stocks.json',
#            'del': xq + '/stock/portfolio/delstock.json',
#            'add': xq + '/v4/stock/portfolio/addstock.json',
#            'modify': xq + '/v4/stock/portfolio/modifystocks.json'}
#     # 默认cookie
#     df_cookie = ('s=××××××; '
#                  'xq_a_token=×××××××××××××××××××××; '
#                  'xq_r_token=×××××××××××××××××××××; '
#                  )
#
#     def __init__(self, uid, cookie=df_cookie):
#         self.uid = uid  # 用户页面如 https://xueqiu.com/×××××××××
#         self.cookie = cookie  # 操作列表需要该用户登录的cookie
#         self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) '
#                                       'Gecko/20100101 Firefox/56.0',
#                         'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
#                         'Accept-Encoding': 'gzip, deflate, br',
#                         'Referer': Snowball.xq + '/' + uid,
#                         'Cookie': cookie,
#                         'DNT': '1'}
#         self.stocks = pd.DataFrame()  # 雪球自选股清单
#
#     def get_stocks(self):
#         # 获取雪球自选股列表
#         try:
#             payload = {'size': 1000, 'tuid': self.uid, 'uid': self.uid, 'pid': -1, 'category': 2, 'type': 1}
#             response = requests.get(Snowball.url['get'], params=payload, headers=self.headers, timeout=10)
#             # pprint(response.content)
#             self.stocks = pd.DataFrame(response.json()['stocks'])
#         except Exception, e:
#             print
#             'get_stocks @', self.uid, '; error:', e
#             pprint(payload)
#             pprint(self.headers)
#             return False
#         else:
#             # pprint(self.stocks)
#             return self.stocks
#
#     def del_stock(self, code):
#         # 在雪球删除指定代码的股票
#         try:
#             payload = {'code': code}
#             response = requests.post(Snowball.url['del'], data=payload, headers=self.headers, timeout=10)
#             # pprint(response.content)
#             response = response.json()['success']
#             if response == True:
#                 print
#                 'del_stock', code, 'success.'
#             else:
#                 print
#                 'del_stock', code, 'failed.'
#         except Exception, e:
#             print
#             'del_stock', code, '@', self.uid, '; error:', e
#             pprint(payload)
#             pprint(self.headers)
#             return False
#         else:
#             self.get_stocks()
#             return response
#
#     def add_stock(self, code):
#         # 在雪球添加指定代码的股票
#         try:
#             payload = {'symbol': code, 'category': 2, 'isnotice': 1}
#             response = requests.post(Snowball.url['add'], data=payload, headers=self.headers, timeout=10)
#             # pprint(response.content)
#             response = response.json()['success']
#             if response == True:
#                 print
#                 'add_stock', code, 'success.'
#             else:
#                 print
#                 'add_stock', code, 'failed.'
#         except Exception, e:
#             print
#             'add_stock', code, '@', self.uid, '; error:', e
#             pprint(payload)
#             pprint(self.headers)
#             return False
#         else:
#             self.get_stocks()
#             return response
#
#     def modify_stocks(self, code_list=[]):
#         # 雪球自选股列表排序
#         try:
#             payload = {'pid': -1, 'type': 1, 'stocks': ','.join(code_list)}
#             response = requests.post(Snowball.url['modify'], data=payload, headers=self.headers, timeout=10)
#             # pprint(response.content)
#             response = response.json()['success']
#             if response == True:
#                 print
#                 'modify_stocks', code_list, 'success.'
#             else:
#                 print
#                 'modify_stocks', code_list, 'failed.'
#         except Exception, e:
#             print
#             'modify_stocks', code_list, '@', self.uid, '; error:', e
#             pprint(payload)
#             pprint(self.headers)
#             return False
#         else:
#             self.get_stocks()
#             return response


class Tonghuashun:
    # 同花顺自选股列表相关
    url = {'get': 'http://t.10jqka.com.cn/newcircle/user/userPersonal/?from=circle',
           'modify': 'http://stock.10jqka.com.cn/self.php'}

    def __init__(self, uid, cookie):
        self.uid = uid
        self.cookie = cookie  # 该用户登录的cookie
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) '
                                      'Gecko/20100101 Firefox/56.0',
                        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate',
                        'Referer': 'http://upass.10jqka.com.cn/',
                        'Cookie': cookie,
                        'DNT': '1'}
        self.stocks = pd.DataFrame()  # 同花顺自选股清单

    def get_stocks(self):
        # 获取同花顺自选股列表
        try:
            payload = {'callback': 'callback' + str(int(time.time() * 1000))}
            response = requests.get(Tonghuashun.url['get'], params=payload, headers=self.headers, timeout=10)
            # pprint(response.content)
            self.stocks = pd.DataFrame(response.json())
        except:
            pprint(payload)
            pprint(self.headers)
            return False
        else:
            # pprint(self.stocks)
            return self.stocks

    def modify_stock(self, code, method, pos='1'):
        # 更改同花顺自选股列表
        # method: add 添加, del 删除, exc 排序
        # pos: 排序用的序号, 从1开始
        try:
            payload = {'add': {'stockcode': code, 'op': 'add'},
                       'del': {'stockcode': code, 'op': 'del'},
                       'exc': {'stockcode': code, 'op': 'exc', 'pos': pos, 'callback': 'callbacknew'}
                       }
            # self.get_stocks()
            response = requests.get(Tonghuashun.url['modify'], params=payload[method], headers=self.headers, timeout=10)
            # pprint(response.content)
            response = response.content.decode('gbk')
            print('modify_stocks', method, pos, code, response)
            if response == u'修改自选股成功':
                response = True
        except:
            pprint(payload[method])
            pprint(self.headers)
            return False
        else:
            self.get_stocks()
            return response

ths = Tonghuashun(123, '__bid_n=185338c9440b65cf584207; FEID=v10-84dc7cbc98780f96d9b1516d79d9e930cd36fc1a; __xaf_fpstarttimer__=1671781948333; __xaf_thstime__=1671781948432; __xaf_fptokentimer__=1671781948437; user=MDpteF8zMDkxNjcwOTM6Ok5vbmU6NTAwOjMxOTE2NzA5Mzo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoxNjo6OjMwOTE2NzA5MzoxNjc0OTU4NDcyOjo6MTQ0ODAyMjM2MDoyMjk1Mjg6MDoxYTU1NGRjYTgyNWExYTY2ZWRlMjc3YTk2ODRjZWEyMzI6ZGVmYXVsdF80OjA%3D; userid=309167093; u_name=mx_309167093; escapename=mx_309167093; ticket=051ba53001348ae0cf4e874d92eb4fd9; user_status=0; utk=c972df386d119ed3c0620e9f659f85d6; Hm_lvt_da7579fd91e2c6fa5aeb9d1620a9b333=1674958474; Hm_lpvt_da7579fd91e2c6fa5aeb9d1620a9b333=1674958474; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1674958474; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1674958474; FPTOKEN=KLdl8NHubj8cWKEugzbEyKKQK32QWwO+cWP0eHh9eXru0FALD7XhUf1ZresMH00E9ZTWLXEzzTbQOcXByIXsv9wxo7TR0nOrUr14ifU8h96xyd2kO79JvmJaImbZ3x4OQfQ1WUo295kMiHZ8YO9yH7rKIWFDGteMDbVhLlG103+2MEwdtwa4ZTLwOd5Hm3tCyi1Kmehz+bZNtPW8d36rc3aWFIoueMtGVL5dG4OPvmHzjO2/3k67ML5YtukfyBlDr5gFXb5wihnMPs2wAZ0kejkLv4UCBZGihBgWAg7liC+iAXBpUxpHqMWi9gUIrx4uP01mfbWUKSs53HYIbUsmXGy5kao9T6P+K/RKfHcd4/Yaml2dU3Omhh3JIC8y1w2CWJWa9XxfJhb+/a0jVv7pYw==|FPfMxsLqBox1Dri/SJWVVzMl3YpZoRbZD6gxWyXa5OQ=|10|fe5ed5cef1ee2e793d59ad7bea0b887a; v=Aw7FXzS64azAc1WIsAMd0siEX-_Vj9525ESHcThWe83Ok6BRoB8imbTj1jwL')
stocks = ths.get_stocks()
print(stocks)