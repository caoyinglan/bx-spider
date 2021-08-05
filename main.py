import requests
from bs4 import BeautifulSoup
import re
import sys
import time
import pandas as pd
import io
from functools import wraps

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') #改变标准输出的默认编码

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
        self._0 = []
        self._1 = []
        self._2 = []
        self._3 = []
        self._href = []

    def get_contents(self):
        requests.packages.urllib3.disable_warnings()
        # s = requests.session()
        # s.keep_alive = False
        proxies={'http': 'http://42.178.145.171:30177''http://222.37.78.224:46603''http://123.73.63.100:46603'
                         'http://123.73.209.58:46603''http://117.64.234.161:45128''http://117.88.5.237:32186'
                         'http://113.117.11.193:45102''http://49.89.92.19:45137''http://123.73.208.238:46603'
                         'http://'}
        response = requests.get(self._url, proxies=proxies, headers=self._headers, verify=False)
        response.encoding = "utf-8"
        print(response.status_code)
        response = response.text
        allThings = BeautifulSoup(response, "html.parser")
        contents = allThings.find_all('li', class_='link-block')
        return contents

    def catch_data(self):
        contents = self.get_contents()
        #print(contents,len(contents))
        pattern1 = re.compile('<a[^>]+href=["\'](.*?)["\']')
        for i in range(len(contents)):
            href = pattern1.findall(str(contents[i-1]))
            #print(href)
            self._href.append(href)

            info = contents[i-1].get_text(" ", strip=True)
            #print(info)
            if(i==0):
                self._0 = info
            if(i==1):
                self._1 = info
            if(i==2):
                self._2 = info



    def extract(self):
        self.catch_data()
        ticks = time.strftime("%Y-%m-%d", time.localtime())

        test = pd.DataFrame.from_dict({'n1': self._0, 'n2': self._1, 'n3': self._2, 'url': self._href}, orient='index')
        path = '.baixing_' + str(ticks) + '.csv'
        test.to_csv(path, encoding='utf-8-sig', index=False)

try:
    @retry(3)
    def main():
        data = baixing("https://shanghai.baixing.com/")
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
            main()  # 此处为要执行的任务
            count += 1
            print(count)
            time.sleep(n)


timer(1)


# if __name__ == '__main__':
#    main()