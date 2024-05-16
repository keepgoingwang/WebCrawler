import requests
import urllib.parse
import json
from datetime import datetime

import pandas as pd

def get_url_encoded_params(params: dict) -> dict:
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


def get_data_from_response_dict(response_dict: dict) -> list:
    """
    从响应字典中获取数据
    :param response_dict: 响应字典
    :return: 数据列表
    """
    data_list = []
    all_reviews = response_dict["data"]["comments"]
    for review in all_reviews:
        review_user_info = review["commentUser"]
        review_content = review["content"]
        review_createTime = int(review["createTime"]) / 1000 
        review_commentExt = review["commentExt"] # 房间类型
        if review["images"] is not None:
            review_images_path = str([ j["url"] for i in review["images"] if "imagesPath" in i.keys() for j in i] )
        else:
            review_images_path = ""
        review_video = review["video"]
        review_replys = str([ i["content"] for i in review["replys"]])
        review_commentScore = review["commentScore"]
        review_ipAddress = review["ipAddress"]
        review_commentScoreDes = review["commentScoreDes"]

        data_list.append({
            "user_info": json.dumps(review_user_info),
            "content": review_content,
            "createTime": datetime.fromtimestamp(review_createTime),
            "commentExt": json.dumps(review_commentExt),
            "images_path": review_images_path,
            "video": review_video,
            "replys": review_replys,
            "commentScore": review_commentScore,
            "ipAddress": review_ipAddress,
            "commentScoreDes": review_commentScoreDes
        })
    return data_list


def save_data_to_excel(data: list, file_path: str):
    """
    将数据保存为csv文件, 按照时间进行升序排序
    :param data: 数据列表, 每一个数据为字典类型
    :param file_path: 文件路径
    :return: None
    """
    df = pd.DataFrame(data)
    # df["time"] = pd.to_datetime(df["time"])
    # df = df.sort_values(by="time", ascending=True)
    df.drop_duplicates(inplace=True)
    if file_path.endswith(".csv"):
        df.to_csv(file_path, index=False)
    elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        df.to_excel(file_path, index=False, engine="xlsxwriter")

