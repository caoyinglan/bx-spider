import random

import requests
from bs4 import BeautifulSoup
import re
import sys
import time
import pandas as pd
import io
from functools import wraps

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def retry(times, sleep=0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            run_times = 0
            while 1:
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    time.sleep(sleep)
                    if run_times < times:
                        run_times += 1
                    else:
                        raise ex
        return wrapper
    return decorator

class baixing(object):
    def __init__(self, url):
        self._url = url
        self._headers = {'User-agent':
                             'Mozilla/110.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.182 Safari/537.36',
                         'User-name':
                              'CCCCCYL20210723' }
        self._info = []
        self._href = []

    def get_contents(self):
        requests.packages.urllib3.disable_warnings()
        s = requests.session()
        s.keep_alive = False

        # # http代理接入服务器地址端口
        # proxyHost = "http-proxy-t3.dobel.cn"
        # proxyPort = "9180"
        #
        # # 账号密码
        # proxyUser = "LONGZHUASHOU6GBJR1KR0"
        # proxyPass = "8CDnVted"
        #
        # proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        #     "host": proxyHost,
        #     "port": proxyPort,
        #     "user": proxyUser,
        #     "pass": proxyPass,
        # }
        #
        # proxies = {
        #     "http": proxyMeta,
        #     "https": proxyMeta,
        # }

        proxies={'http': 'http://222.37.130.251:46603',
                 'https': 'http://222.37.130.251:46603'}
        '''使用随机ip爬取数据，请求头不变，同一ip至少1min内产生60条请求
           若使用隧道ip，无法控制其访问频率，还是只能用ip代理池'''
        response = requests.get(self._url, proxies=proxies, headers=self._headers, stream=True)
        ip = response.raw._connection.sock.getpeername()
        # response1 = requests.get(self._url, proxies=proxies, headers=self._headers, stream=True)
        # response2 = requests.get(self._url, proxies=proxies, headers=self._headers, stream=True)
        # response3 = requests.get(self._url, proxies=proxies, headers=self._headers, stream=True)
        # response4 = requests.get(self._url, proxies=proxies, headers=self._headers, stream=True)
        # response5 = requests.get(self._url, proxies=proxies, headers=self._headers, stream=True)
        # response6 = requests.get(self._url, proxies=proxies, headers=self._headers, stream=True)
        # response7 = requests.get(self._url, proxies=proxies, headers=self._headers, stream=True)
        # response8 = requests.get(self._url, proxies=proxies, headers=self._headers, verify=False)
        # response9 = requests.get(self._url, proxies=proxies, headers=self._headers, verify=False)

        response.encoding = "utf-8"
        print(response.status_code)
        print(ip)
        response = response.text
        allThings = BeautifulSoup(response, "html.parser")
        # contents = allThings.find_all('title')
        contents = allThings.find_all('li', class_='link-block')
        '''主站和店铺之间的切换'''
        return contents

    def catch_data(self):
        contents = self.get_contents()
        # print(contents, len(contents))
        pattern1 = re.compile('<a[^>]+href=["\'](.*?)["\']')

        href = pattern1.findall(str(contents))
        # print(href)
        self._href.append(href)

        info = contents[0].get_text(" ", strip=True)
        print(info)
        self._info.append(info)

    def extract(self):
        self.catch_data()
        ticks = time.strftime("%Y-%m-%d", time.localtime())

        test = pd.DataFrame.from_dict({'info': self._info, 'url': self._href}, orient='index')
        path = '.baixing_test_' + str(ticks) + '.csv'
        test.to_csv(path, encoding='utf-8-sig', index=False)


try:
    @retry(3)
    def main():
        data = baixing("https://shanghai.baixing.com/")
        # data = baixing("https://shop.baixing.com/yhfangshui/")
        '''主站和店铺之间的切换'''
        data.extract()
except Exception as ex:
    print(ex)

def timer(n):
        '''''
        每n秒执行一次
        '''
        count = 0
        while True:
            print(time.strftime('%Y-%m-%d %X', time.localtime()))
            main()
            count += 1
            print(count)
            time.sleep(n)

a = random.randint(1,6)
timer(a)

# if __name__ == '__main__':
#    main()
