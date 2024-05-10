# -*- coding: utf-8 -*-
# @Time    : 2024/05/10
# @Author  : Wang
# 从网络上爬取题库，进行转换格式。此项目题库通过api即可获取全部

import requests
import json
import time

import pandas as pd


def get_response(url):
    
    url = "https://www.xiangda.group/datiweb/appapi/?s=Tests.getTestsListIndex&uid=2496&token=6c196a22d9ffbdae14680615771959f7"
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
    data = {
        "s": "Tests.getTrainTestsListIndex",
        "uid": "2496",
        "token": "162e96b211c9761e497abd2ce4ce808e",
        "testSign": 1
    }
    response = requests.get(url, headers=headers,data=data)

    # print(response.json())
    return response.json()

def get_all_ti(file_path, json_data=None):

    if json_data is None:
        with open('./everyday_1.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = json_data
    all_ti_list = list()
    all_ti = data["data"]["info"][0]
    print("共有{}个题目".format(len(all_ti)))

    for id,ti in enumerate(all_ti):
        title = ti["title"]
        answer = json.loads(ti["answer"])
        right_ans_index = int(answer["rs"])
        # print(answer)
        if int(answer["nums"]) == 4:
            A, B, C, D = answer["ans"]
            # right_ans = answer["ans"][right_ans_index]
            #
            if len(answer["rs"]) == 1: # 单选题
                right_ans = ["A", "B", "C", "D"][right_ans_index]
            else: # 多选题
                right_ans = "".join([["A", "B", "C", "D"][i] for i in right_ans_index])
        elif int(answer["nums"]) == 2:
            A, B, C, D= ["对", "错", "", ""]
            if int(answer["rs"]) == 1:
                right_ans = "A"
            elif int(answer["rs"]) == 0:
                right_ans = "B"
                
        one_ti = pd.Series({
            "题目": title,
            "正确答案": right_ans,
            "选项A": A,
            "选项B": B,
            "选项C": C,
            "选项D": D,
            }
        )
        all_ti_list.append(one_ti)
    
    return all_ti_list

def save_to_csv(data, out_file_path):
    df = pd.DataFrame(all_ti_list)
    df.to_csv("./everyday_1.csv", index=False, encoding='utf-8')


if __name__ == '__main__':
    url =""
    response_data = get_response(url)
    all_ti_list = get_all_ti(json_data=response_data)
    save_to_csv(all_ti_list, "./everyday_1.csv")
   