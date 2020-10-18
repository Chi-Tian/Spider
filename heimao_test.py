# -*- coding = utf-8 -*-
# @Time : 2020/10/15 17:10
# @Author : TianChi
# @File : heimao_test.py
# @Software : PyCharm


import urllib.request, urllib.error  # 指定URL，获取网页数据
import xlwt  # 进行excel操作
import json
import requests
from lxml import etree


def main():
    base_url1 = "https://tousu.sina.com.cn/api/index/feed?callback=jQuery111206438664184326481_1602743472525&type=1&page_size=10&page="
    number_list = get_numbers(base_url1)
    get_data(number_list)
    data_list = get_data(number_list)
    savepath = r'.\黑猫投诉网站.xls'
    save_data(data_list,savepath)

def get_numbers(base_url1):  # 获得所有的投诉编号
    complaint_numbers = []
    for i in range(1, 2):
        url = base_url1 + str(i)
        jsonstr = askUrl(url)
        jsonstr = jsonstr.replace('try{jQuery111206438664184326481_1602743472525(', '')  # 将json文本字符串的头和尾去掉
        jsonstr = jsonstr.replace(');}catch(e){};', '')
        unicodeJson = json.loads(jsonstr)  # 调用JSON的load()方法将json文本字符串转为JSON对象       unicodeJson是一个字典
        # print(unicodeJson)

        itemlist = unicodeJson['result']['data']['lists']
        for item in itemlist:
            sn = item['main']['sn']
            complaint_numbers.append(sn)
    # print(complaint_numbers)
    return complaint_numbers

def get_data(number_list):
    base_url = "https://tousu.sina.com.cn/complaint/view/"
    data_list = []
    for i in number_list:
        url = base_url + i
        response = requests.get(url)
        html = response.text
        data = []
        html = etree.HTML(response.text)
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
        data_list.append(data)
    print(data_list)
    return data_list

def askUrl(url):
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=head)
    jsonstr = ''
    try:
        response = urllib.request.urlopen(request)
        jsonstr = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)

    return jsonstr

def save_data(data_list,savepath):
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = book.add_sheet('黑猫投诉网站',cell_overwrite_ok=True)
    col = ('投诉标题','投诉详情','投诉对象','投诉问题','投诉要求')
    for i in range(0,5):
        sheet.write(0,i,col[i])
    # for i in range(0,13):
    #     print('这是第%d条'%(i+1))
        data = data_list[i]
        for j in range(0,5):
            sheet.write(i+1,j,data[j])
    book.save(savepath)


if __name__ == '__main__':
    main()
    print('爬取完毕！')



