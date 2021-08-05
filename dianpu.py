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
                             'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        self._info = []
        self._href = []

    def get_contents(self):
        requests.packages.urllib3.disable_warnings()
        # s = requests.session()
        # s.keep_alive = False

        # http代理接入服务器地址端口
        proxyHost = "http-proxy-t3.dobel.cn"
        proxyPort = "9180"

        # 账号密码
        proxyUser = "LONGZHUASHOU6GBJR1KR0"
        proxyPass = "8CDnVted"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }

        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }

        #
        # proxies={'http': 'http://LONGZHUASHOU6GBJR1KR0:8CDnVted@http-proxy-t3.dobel.cn:9180', 'https': 'http://LONGZHUASHOU6GBJR1KR0:8CDnVted@http-proxy-t3.dobel.cn:9180'}
        response = requests.get(self._url, proxies=proxies, headers=self._headers, verify=False)
        response.encoding = "utf-8"
        print(response.status_code)
        response = response.text
        allThings = BeautifulSoup(response, "html.parser")
        contents = allThings.find_all('ul')
        return contents

    def catch_data(self):
        contents = self.get_contents()
        print(contents, len(contents))
        pattern1 = re.compile('<a[^>]+href=["\'](.*?)["\']')

        href = pattern1.findall(str(contents))
        print(href)
        self._href.append(href)

        info = contents[0].get_text(" ", strip=True)
        print(info)
        self._info.append(info)

    def extract(self):
        self.catch_data()
        ticks = time.strftime("%Y-%m-%d", time.localtime())

        test = pd.DataFrame.from_dict({'info': self._info, 'url': self._href}, orient='index')
        path = '.baixing_dianpu2_' + str(ticks) + '.csv'
        test.to_csv(path, encoding='utf-8-sig', index=False)


def timer(n):
        '''''
        每n秒执行一次
        '''
        count = 0
        while True:
            print(time.strftime('%Y-%m-%d %X', time.localtime()))
            try:
                @retry(3)
                def main():
                    data = baixing("https://www.baixing.com/weishop/brands/fuwu/?&page=1")
                    data.extract()
            except Exception as ex:
                print(ex)
            count += 1
            print(count)
            time.sleep(n)

timer(0.1)


# if __name__ == '__main__':
#    main()