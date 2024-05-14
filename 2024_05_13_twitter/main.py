import requests
import json
import urllib.parse
import datetime

import httpx as htt
from tools import *
import socks
import socket

#亿牛云 爬虫代理加强版 代理服务器
proxyHost = "www.16yun.cn"
proxyPort = "31111"

# 代理验证信息
proxyUser = "16YUN"
proxyPass = "16IP"



# 构造代理服务器字典
proxies = {
    "http": f"http://{proxyUser}:{proxyPass}@{proxyHost}:{proxyPort}",
    "https": f"https://{proxyUser}:{proxyPass}@{proxyHost}:{proxyPort}"
}



def main(username=None, user_main_url=None):
    # 基础请求url
    user_info_url_ = "https://twitter.com/i/api/graphql/qW5u-DAuXpMEG0zA1F7UGQ/UserByScreenName"
    user_twitter_url_ = "https://twitter.com/i/api/graphql/9zyyd1hebl7oNWIPdA8HRw/UserTweets"

    # proxies = {
    #     "http": None,
    #     "https": None
    # }
    # proxies = {
    #     "http": f"http://72.10.164.178:8125",
    #     "https": f"https://72.10.164.178:8125"
    # }
    # 设置socks代理
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 32345)  # 替换为实际的代理地址和端口

    # 将socket的默认代理设置为socks代理
    socket.socket = socks.socksocket

    # 构造请求头字典
    headers = get_json_data('./configs/request_headers.json')

    # 获取用户信息
    if username is not None:
        pass
    # 构造请求体字典
    user_info_data = get_json_data("./configs/user_info_data.json")
    user_info_data["variables"]["screen_name"] = username # 要查询的用户名
    info_url_dict = get_url_params(user_info_data)
    user_info_url = user_info_url_ + str("?variables=") + str(info_url_dict["variables"]) + str("&features=") + str(info_url_dict["features"]) + str("&fieldToggles=") + str(info_url_dict["fieldToggles"])
    # 获取用户id
    response_user_info = get_response_data(url=user_info_url, headers=headers)#, proxies=proxies)
    user_id = response_user_info["data"]["user"]["result"]["rest_id"]


    # 获取用户twitter
    user_twitter_data = get_json_data("./configs/user_twitter_data.json")
    user_twitter_data["variables"]["userId"] = user_id # 替换用户id
    # 获取请求地址
    twitter_url_dict = get_url_params(user_twitter_data)
    user_twitter_url = user_twitter_url_ + str("?variables=") + str(twitter_url_dict["variables"]) + str("&features=") + str(twitter_url_dict["features"]) + str("&fieldToggles=") + str(twitter_url_dict["fieldToggles"])
    
    '''目前获取的twitter包含转发的,并且只有20条还未获取更多'''
    response_user_twitters = get_response_data(url=user_twitter_url, headers=headers)#, proxies=proxies)
    
    # print("--",response_user_twitters)
    # # client = htt.Client()
    # response = client.post(user_info_url, headers=headers, data=user_info_data)

    # 打印响应结果
    with open("./out_data/get_twitters.json", 'w', encoding='utf-8') as f:
        json.dump(response_user_twitters, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":

    username = "elonmusk"
    user_main_url = "https://twitter.com/pompdotfun"
    main(username=username, user_main_url=user_main_url)
