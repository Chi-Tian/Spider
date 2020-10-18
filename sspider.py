# -*- coding = utf-8 -*-
# @Time : 2020/10/17 11:50
# @Author : TianChi
# @File : sspider.py
# @Software : PyCharm


import requests
import re
from urllib.parse import urlencode
from lxml import etree
import json
import csv


def get_numbers():
    numbers = []
    for i in range(1,11):
        url = 'https://tousu.sina.com.cn/api/index/feed?callback=jQuery111206080975127909245_1602909300444&type=1&page_size=10&page=' + str(i)
        try:
            response = requests.get(url)
            res = response.text
            # print(res)
            if response.status_code == 200:
                numbers = numbers + re.findall('sn":"(\d+)",',res)
        except requests.ConnectionError:
            print('第'+str(i)+'页地址后缀获取失败！')
    print('总共获得'+str(len(numbers))+'个后缀')
    return numbers


def get_data(numbers):
    base_url = 'https://tousu.sina.com.cn/complaint/view/'
    for i in numbers:
        url = base_url + i
        try:
            respond = requests.get(url)
            if respond.status_code == 200:
                html = etree.HTML(respond.content)
                html = etree.HTML(respond.content)
                title = html.xpath('//div[@class="ts-d-question"]/h1/text()')[0].encode("ISO-8859-1").decode("utf-8")
                cotitle = html.xpath('//ul[@class="ts-q-list"]//a/text()')[0].encode("ISO-8859-1").decode("utf-8")
                question = html.xpath('//ul[@class="ts-q-list"]/li[3]/text()')[0].encode("ISO-8859-1").decode("utf-8")
                appeal = html.xpath('//ul[@class="ts-q-list"]/li[4]/text()')[0].encode("ISO-8859-1").decode("utf-8")
                result = html.xpath('//div[@class="ts-reply"][1]/p[2]/text()')[0].encode("ISO-8859-1").decode("utf-8")
                yield {
                    '投诉标题': title,
                    '投诉详情': result,
                    '投诉对象': cotitle,
                    '投诉问题': question,
                    '投诉要求': appeal
                }
        except Exception:
            print('投诉编号' + i + '爬取失败！')

def write_csv(numbers):
    with open('heimao.csv','a',encoding='utf-8') as csvfile:
        fieldnames = ['投诉标题','投诉详情','投诉对象','投诉问题','投诉要求']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        for content in get_data(numbers):
            writer.writerow(content)

def main():
    numbers = get_numbers()
    write_csv(numbers)

if __name__ == "__main__":
    # 调用函数
    main()