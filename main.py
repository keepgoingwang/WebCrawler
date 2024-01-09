'''
主流程:需根据具体需求进行更改步骤
'''
import os
from utils import *
# from bi import *
import shutil
import json
import pandas as pd

def main(areas):
	
	# 读取本地临时文件夹,是否已存在房屋信息的json
	try:
		with open(r".\tmps\detail_urls.json", 'r') as f:
			level_two_urls = json.load(f)
		step1 = False
	except:
		step1 =True

	headers = {
		"User-Agent": "Mozilla/5.0",
		}
	
	# 获取每个区域对应的所有房源url
	if step1:
		
		print("step 1 >>>>>>")
		home_url = r"https://xz.lianjia.com" # https://xz.lianjia.com/zufang/tongshanqu/pg1
		level_one_urls = {}
		for area_name, pages in areas.items():
			level_one_urls[area_name] = [ str(home_url + str("/zufang/") + str(area_name) + str("/pg") + str(page)) for page in range(1, int(pages+1))]
			# print(f"{area_name}有{len(level_one_urls[area_name])}页数据")

		# 获取每套房源对应的具体url
		level_two_urls = {}
		for a_name, urls in level_one_urls.items():
			page = Pages(urls=urls, headers=headers)
			
			matchs = {
				a_name: '//div[@class="content__list--item--main"]/p/a[@class="twoline"]/@href'
			}
			
			detail_pages = page.get_elements_by_xpath(match=matchs)
			detail_urls = [str(home_url + str(page)) for _,pages in detail_pages.items() for page in pages]

			level_two_urls[a_name] = detail_urls
			print(f"{a_name}有{len(detail_urls)}条房源数据")
		
		# 新建 tmp 文件夹将获取的urls保存至本地；
		if not os.path.exists(r'.\tmps'):
			os.mkdir(r'.\tmps')
		with open(r".\tmps\detail_urls.json", "w", encoding='utf-8') as f:
			json.dump(level_two_urls, f, default=str)

	# 获取每个区域每套房源的具体信息
	if 1 == 0:
		print("step 2 >>>>>>")
		all_infos = {}
		# 
		for a_name, d_urls in level_two_urls.items():
			pages = Pages(urls=d_urls)
			d_matchs = {
				"title": '//div/p[@class="content__title"]/text()',
				"areas": '//div[@class="content__article fl"]/div[@class="content__article__info"]/ul[1]/li[2]/text()',
				"towards": '//div[@class="content__article fl"]/div[@class="content__article__info"]/ul[1]/li[3]/text()',
				"floor": '//div[@class="content__article fl"]/div[@class="content__article__info"]/ul[1]/li[8]/text()',
				"elevator": '//div[@class="content__article fl"]/div[@class="content__article__info"]/ul[1]/li[9]/text()',
				"electricity": '//div[@class="content__article fl"]/div[@class="content__article__info"]/ul[1]/li[14]/text()',
				"water": '//div[@class="content__article fl"]/div[@class="content__article__info"]/ul[1]/li[12]/text()',
				"gas": '//div[@class="content__article fl"]/div[@class="content__article__info"]/ul[1]/li[15]/text()',
				"visit": '//div[@class="content__article fl"]/div[@class="content__article__info"]/ul[2]/li[5]/text()',
				"price": '//div[@class="table_content"]/ul/li[@class="table_col font_orange"]/text()',
				"pay_method": '//div[@class="table_content"]/ul/li[@class="table_col font_gray"]/text()',
				"traffic": '//div[@class="content__article__info4 w1150"]/ul/li/span/text()'
			}

			detail_infos = pages.get_elements_by_xpath_one(match=d_matchs)
			
			all_infos[a_name] = detail_infos
		
		# 将爬取的所有信息保存至本地备用
		with open(r".\tmps\all_infos.json", "w", encoding='utf-8') as f:
			json.dump(all_infos, f)
		# df = pd.DataFrame(columns=["title", "areas", "towards", "floor", "elevator", "electricity", "water", "gas", "visit", "price", "pay_method", "traffic"])
		# for a_name, infos in all_infos.items():
		# 	df_info = dic_2_csv(infos)
		# 	df_info["region"] = a_name
		# 	df = pd.concat([df, df_info], axis=0)
		
		# df.to_csv(r".\results.csv",encoding='utf-8',index=False)
		

		# 删除本地临时文件夹 tmp
		if 1 == 0:
			shutil.rmtree(r".\tmp")

if __name__ == "__main__":

	areas = {
		"yunlongqu": 75,
		"gulouqu": 79,
		"quanshanqu": 100,
		"tongshanqu": 41	
	}
	
	main(areas)
