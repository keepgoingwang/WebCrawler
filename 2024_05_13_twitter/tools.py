import json
import urllib.parse
from datetime import datetime
import requests
import traceback

import pandas as pd

def get_response_data(url, headers, proxies=None) -> dict:
    """
    获取响应数据
    :url: 请求url
    :headers: 请求头
    :proxies 代理
    """
    if proxies is None:
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url, headers=headers, proxies=proxies)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("请求失败,状态码: {}".format(response.status_code))


def get_json_data(path) -> dict:
    """
    获取json数据
    :param path: json文件路径
    :return: json数据字典
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def get_url_params(params: dict) -> dict:
    """
    将参数字典转换为url参数字符串
    :param params: 参数字典
    :return: url dict
    """
    str_url_dict = {}
    for key, value in params.items():
        if isinstance(value, dict):
            # print(json.dumps(value).replace(" ", ""))
            str_url = urllib.parse.quote(json.dumps(value).replace(" ", ""))
            str_url_dict[key] = str_url
        else:
            raise ValueError("参数类型错误,必须为字典类型")
    
    return str_url_dict 


def change_time_format(time_str: str) -> str:
    """
    将时间字符串转换为数字类型
    :param time_str: 时间字符串
    :return: 数字类型时间
    """
    data_time = datetime.strptime(time_str, "%a %b %d %H:%M:%S %z %Y")
    data_time = datetime.strftime(data_time, '%Y-%m-%d %H:%M:%S')
    return data_time



def get_twitter_from_response(data: json, username) -> list:
    """
    从response中获取数据
    :data 获取的json对象
    :return 数据列表, 每条数据为字典类型
    """
    # 第一层数据
    all_twitters = []
    data_instructions = data['data']["user"]["result"]["timeline_v2"]["timeline"]["instructions"]
    for instruction in data_instructions:
        if instruction["type"] != "TimelineAddEntries":
            continue
        for item in instruction["entries"]:
            try:
                if "itemContent" not in item["content"].keys():
                    continue
                if "legacy" not in item["content"]["itemContent"]["tweet_results"]["result"].keys():
                    continue

                twitter_info = item["content"]["itemContent"]["tweet_results"]["result"]["legacy"]
                text, cr_time = twitter_info["full_text"],  twitter_info["created_at"]
                cr_time = change_time_format(cr_time)
                twitter_url = 'https://twitter.com/' + username + str("/status/") + item["entryId"].split("tweet-")[-1].split("-")[0]
                # print(str(twitter_info["is_quote_status"]))
                # 判断是否转发
                if twitter_info["is_quote_status"] is True:
                    is_quote = "0"
                elif twitter_info["is_quote_status"] is False:
                    is_quote = "1"
                one_twitter = {
                    "time": cr_time,
                    "content": text,
                    "url": twitter_url,
                    "is_quote": is_quote
                }
                all_twitters.append(one_twitter)
            except:
                print(traceback.format_exc())
    
    return all_twitters

def sava_2_csv(data: list, file_path: str):
    """
    将数据保存为csv文件, 按照时间进行升序排序
    :param data: 数据列表, 每一个数据为字典类型
    :param file_path: 文件路径
    :return: None
    """
    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values(by="time", ascending=True)
    df.to_csv(file_path, index=False)


if __name__ == '__main__':
    username = "elonmusk"
    data = get_json_data("./out_data/get_twitters.json")
    twitters = get_twitter_from_response(data=data, username=username)
    # print(twitters)
    file_path = "./out_data/" + username + ".csv"
    sava_2_csv(data=twitters, file_path=file_path)