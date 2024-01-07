'''
主流程:需根据具体需求进行更改步骤
'''
import os
from utils import *
from bi import *
import requests

def main():
	url = r"https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA&pvid=8858151673f941e9b1a4d2c7214b2b52&czLogin=1"
	headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
			}


	page = Pages(urls=url)

	matchs = {
		"year": '//div[@id="J_goodsList"]/ul/li/div/div[@class="p-price"]',
		"name": '//div[@id="J_goodsList"]/ul/li/div/div[@class="p-stop"]/text()',
		"actor": '//div[@id="J_goodsList"]/ul/li/div/div[@class="p-name p-name-type-2"]/text()'
	}
	data = page.get_elements_by_xpath(match=matchs)
	print(data)

if __name__ == "__main__":
	main()
