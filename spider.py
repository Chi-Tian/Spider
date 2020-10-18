# -*- coding = utf-8 -*-
# @Time : 2020/10/17 15:14
# @Author : TianChi
# @File : spider.py
# @Software : PyCharm
import urllib.request  # 制定url
import json
from lxml import etree
import csv
import time
import random
def main():
    baseurl1 = "https://tousu.sina.com.cn/api/index/feed?callback=jQuery111208038698781774218_1602671921456&type=1&page_size=30&page="
    baseurl2 = "&_=1602671921457"
    get_data(baseurl1, baseurl2)
    # write_csv(data_list)
# 获取所有页的数据
def get_data(baseurl1, baseurl2):
    # data_list = []
    with open('黑猫投诉.csv', 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # writer.writerow(['投诉标题', '投诉详情', '投诉对象', '投诉问题', '投诉要求'])

        # 拿到不同页里边的json对象
        for i in range(334,335):
            url = baseurl1 + str(i) + baseurl2
            jsonstr = askUrl(url)
            jsonstr = jsonstr.replace('try{jQuery111208038698781774218_1602671921456(', '')
            jsonstr = jsonstr.replace(');}catch(e){};', '')
            unicodeJson = json.loads(jsonstr)  # 调用JSON库的loads()方法，将JSON文本字符串转为JSON对象,文字

            itemlist = unicodeJson['result']['data']['lists']
            # 拿到不同页里边的url
            for item in itemlist:
                url = 'http:' + item['main']['url']
                # print(url)
                data = get_content(url)   # 调用get_content(url)函数，把一页的信息赋值给data
                # data_list.append(data)   # 将一页的信息append到数据列表
                # print(data)
                # print(type(data))
                writer.writerow(data)
    # return data_list
    csvfile.close()

# 爬取一个指定url的网页内容
def askUrl(url):
    i = random.random()
    time.sleep(i)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    request = urllib.request.Request(url=url, headers=headers)
    jsonstr = ""    # jsonstr用来存储json格式的字符串
    try:
        response = urllib.request.urlopen(request)
        jsonstr = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return jsonstr

# 得到一个页面的所有目的信息
def get_content(url):
    # data_list = []
    html = askUrl(url)
    # print(html)

    html = etree.HTML(html)  # 创建etree
    data = []
    #print(html)
    try:
        # 投诉标题
        title = html.xpath('//div[@class="ts-d-question"]/h1/text()')[0]
        data.append(title)
        # 投诉详情
        detail = html.xpath('//div[@class="ts-reply"][1]/p[2]/text()')[0]
        data.append(detail)
        # 投诉对象
        object = html.xpath('//ul[@class="ts-q-list"]//a/text()')[0]
        data.append(object)
        # 投诉问题
        question = html.xpath('//ul[@class="ts-q-list"]/li[3]/text()')[0]
        data.append(question)
        # 投诉要求
        ask = html.xpath('//ul[@class="ts-q-list"]/li[4]/text()')[0]
        data.append(ask)
    except Exception:
        print('这条信息有误，跳过')
        # print(data)
        # data_list.append(data)
        # print(data_list)
        # print(type(data_list))
    return data
# 将数据写入CSV文件
# def write_csv(data_list):
#     with open('黑猫投诉.csv','a',encoding='utf-8',newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['投诉标题','投诉详情','投诉对象','投诉问题','投诉要求'])
#         for i in data_list:
#             # print(i)
#             writer.writerow(i[0])



if __name__ == "__main__":
    # 调用函数
    main()
    print('爬取完毕！')