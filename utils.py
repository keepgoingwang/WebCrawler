'''
工具集合，包含：
（1）网页爬取及元素解析
（2）保存
'''
import re
import os

import requests
from lxml import html
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
        response = requests.get(url, proxies={'http': proxy, 'https': proxy})
        response.raise_for_status()
        return response.content

    def get_elements_by_xpath(self, match:str or dict):
        data_dict = {}

        for url_response in self.responses:
            tree = html.fromstring(url_response)

            if isinstance(match, str):
                elements = tree.xpath(match)
                data_dict[elements] = data_dict.get(elements, []) + elements
            elif isinstance(match, dict):
                for key, xpath in match.items():
                    elements = tree.xpath(xpath)
                    data_dict[key] = data_dict.get(key, []) + elements

        return data_dict

    def get_elements_by_re(self, match:str or dict):
        data_dict = {}

        for url_response in self.responses:
            for key, pattern in match.items():
                matches = re.findall(pattern, url_response.decode('utf-8'))
                data_dict[key] = data_dict.get(key, []) + matches

        return data_dict



