'''
工具集合，包含：
（1）网页爬取及元素解析
（2）保存
'''
import re
import os
import random
import threading
import time

import requests
from lxml import html,etree
import pandas as pd
class Pages():
    def __init__(self, urls, proxies=None, headers=None):
        if isinstance(urls, list):
            self.urls = urls
        elif isinstance(urls, str):
            self.urls = [urls]
        else:
            raise TypeError("Urls must be a string or a list of strings.")

        self.proxies = proxies
        self.responses = []
        self.fail_urls = []
        self.headers = headers
        self._crawl_pages_one()
        # self._crawl()

        try_time = 0
        while len(self.fail_urls) != 0:
            print(f"开启第{try_time+1}次重新访问")
            self.urls = self.fail_urls
            self.fail_urls = []
            self._crawl_pages_one()
            try_time += 1
            if try_time > 10:
                break

        print(f"--获取成功的数据有{len(self.responses)}条--")
        print(f"--获取失败的数据有{len(self.fail_urls)}条--")


    def _crawl(self):
        # 创建多线程
        threads = []

        # 遍历所有URL，创建线程用于抓取页面
        for url in self.urls:
            crawl_thread = threading.Thread(target=self._crawl_pages_thred, args=(url,))
            threads.append(crawl_thread)

        # 启动所有线程
        for thread in threads:
            thread.start()

        # 等待所有线程完成
        for thread in threads:
            thread.join()


    def _crawl_pages_thred(self, url):
        '''多线程'''
        try:
            response = self._get_page(url)
            self.responses.append(response)
        except requests.RequestException:
            self.fail_urls.append(url)

    def _crawl_pages_one(self):
        '''单线程'''
        for url in self.urls:
            try:
                response = self._get_page(url)
                self.responses.append(response)
            except requests.RequestException:
                self.fail_urls.append(url)

    def _get_page(self, url):
        proxy = random.choice(self.proxies) if self.proxies else None
        if proxy:
            response = requests.get(url, proxies={'http': proxy, 'https': proxy}, headers=self.headers)
        else:
            response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        print(response.status_code)
        time.sleep(random.randint(2,5))
        return response



    def get_elements_by_xpath(self, match:str or dict):
        '''xpath:
            一条match语句匹配出的的数据可为一条或多条
        '''

        data_dict = {}
        for url_response in self.responses:
            tree = html.fromstring(url_response.content)
            # tree = etree.HTML(url_response.text)
            if isinstance(match, str):
                elements = tree.xpath(match)
                if elements:
                    data_dict["elements"] = data_dict.get(elements, []) + elements
            elif isinstance(match, dict):
                for key, xpath in match.items():
                    elements = tree.xpath(xpath)
                    if elements:
                        data_dict[key] = data_dict.get(key, []) + elements
                    else:
                        print(">>>>>>>>>>>>>>>>>>","\n",url_response.text)

        return data_dict

    
    def get_elements_by_xpath_one(self, match:str or dict):
        '''xpath:
            一条match语句匹配出的的数据只能为一条，若匹配到多条数据，转为tuple作为整体
        '''
        data_dict = {}
        for url_response in self.responses:
            tree = html.fromstring(url_response.content)
            # tree = etree.HTML(url_response.text)
            if isinstance(match, str):
                elements = tree.xpath(match)
                if len(elements) > 1:
                    elements = [elements]
                if elements:
                    data_dict["elements"] = data_dict.get(elements, []) + elements
            elif isinstance(match, dict):
                for key, xpath in match.items():
                    elements = tree.xpath(xpath)
                    if len(elements) > 1:
                        elements = [elements]
                    if elements:
                        data_dict[key] = data_dict.get(key, []) + elements

        return data_dict

    def get_elements_by_re(self, match:str or dict):
        '''re'''
        data_dict = {}
        for url_response in self.responses:
            if isinstance(match, str):
                elements = re.findall(match, url_response.decode('utf-8'))
                if elements:
                    data_dict[key] = data_dict.get(key, []) + elements
            if isinstance(match, dict):
                for key, pattern in match.items():
                    elements = re.findall(pattern, url_response.decode('utf-8'))
                    if elements:
                        data_dict[key] = data_dict.get(key, []) + elements

        return data_dict


def dic_2_csv(data, col_names=None, save_path=None):
    if col_names is None:
        df = pd.DataFrame.from_dict(data)
    else:
        if len(col_names) != len(data.keys()):
            raise ValueError("Number of column names provided does not match the number of keys in the dictionary.")
        
        df = pd.DataFrame(data, columns=col_names)

    if save_path:
        file_path = save_path + "results.csv" 
        df.to_csv(file_path, index=False, encoding="utf-8")
        print(f"CSV file '{file_path}' has been created.")

    return df
