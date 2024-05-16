import requests
import json
import itertools
import os
import math

from tools import *

'''
爬取同城网的评论数据,不同酒店或景点的评论数据爬取方式相同,只需修改payload.json中的参数即可
'''

def main(base_url=None, filename=None, reviews_num=None):

    if base_url is None:
        views_api_url_base = "https://www.ly.com/tapi/getCommentList?bodyStr=" 
    else:
        views_api_url_base = base_url
    # 获取 payload dict
    payload_dict = get_json_data("./configs/payload.json")

    # 获取headers
    headers = get_json_data("./configs/headers.json")

    # 获取页数
    if reviews_num is not None:
        pages_num = math.ceil(reviews_num / 10)
    else:
        pages_num = 2

    all_data = []
    wrong_page = 0
    if_worng = False
    print("开始爬取数据...")
    for pageindex in range(pages_num):
        print(f"正在爬取第{pageindex+1}页数据...")
        payload_dict["bodyStr"]["pageIndex"] = pageindex

    # 获取 payload 对应的url字符串
        payload_str = get_url_encoded_params(payload_dict)
        
    # 拼接完整的url
        views_api_url = views_api_url_base + payload_str["bodyStr"]

    # 发送请求
        if if_worng:
            wrong_page += 1
        else:
            wrong_page = 0

        try:
            views_response = get_response_data(views_api_url, headers)
        except Exception as e:
            print(f"第{pageindex+1}页数据爬取失败，原因：{e}")
            if_worng = True            
            continue

    # 解析数据
        views_data = get_data_from_response_dict(views_response)

    # 保存数据
        # with open("./out_data/views_1.json", "w", encoding="utf-8") as f:
        #     json.dump(views_response, f, ensure_ascii=False, indent=4)
        all_data.append(views_data)

        if_worng = False

        if wrong_page >= 3:
            print("连续三次请求失败，退出爬取...")
            break
    # 合并数据
    all_data = list(itertools.chain(*all_data))

    # 保存数据
    if filename is None:
        filename = "views_data.xlsx"
    file_path = os.path.join("./out_data", filename)
    save_data_to_excel(data=all_data, file_path=file_path)


if __name__ == '__main__':
    reviews_num = 10000
    filename = "test.xlsx"
    main(filename=filename)
