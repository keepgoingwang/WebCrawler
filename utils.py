'''
工具集合，包含：
（1）网页爬取及元素解析
（2）保存
'''
import re
import os

import requests
from lxml import html,etree
import random

class Pages():
    def __init__(self, urls, proxies=None):
        if isinstance(urls, list):
            self.urls = urls
        elif isinstance(urls, str):
            self.urls = [urls]
        else:
            raise TypeError("Urls must be a string or a list of strings.")

        self.proxies = proxies
        self.responses = []
        self.fail_urls = []
        self._crawl_pages()

    def _crawl_pages(self):
        for url in self.urls:
            try:
                response = self._get_page(url)
                self.responses.append(response)
            except requests.RequestException:
                self.fail_urls.append(url)

    def _get_page(self, url):
        proxy = random.choice(self.proxies) if self.proxies else None
        if proxy:
            response = requests.get(url, proxies={'http': proxy, 'https': proxy})
        else:
            response = requests.get(url)
        print(response.status_code)
        response.raise_for_status()
        return response

    def get_elements_by_xpath(self, match:str or dict):
        '''xpath'''
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
                    print(xpath)
                    elements = tree.xpath(xpath)
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
                    if elemenets:
                        data_dict[key] = data_dict.get(key, []) + elemenets

        return data_dict


def save_csv(data, col_names=None, save_path=""):
    if col_names is None:
        df = pd.DataFrame.from_dict(data)
    else:
        if len(col_names) != len(data.keys()):
            raise ValueError("Number of column names provided does not match the number of keys in the dictionary.")
        
        df = pd.DataFrame(data, columns=col_names)

    if save_path:
        file_path = save_path + "results.csv"
    else:
        file_path = "results.csv"

    df.to_csv(file_path, index=False, encoding="utf-8")
    print(f"CSV file '{file_path}' has been created.")

