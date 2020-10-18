# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from bs4 import BeautifulSoup     # 网页解析，获取数据
import re      # 正则表达式
import urllib.request,urllib.error   # 指定URL，获取网页数据
import xlwt       # 进行excel操作
import json

def main():
    baseurl1 = "https://tousu.sina.com.cn/api/index/feed?callback=jQuery111206438664184326481_1602743472525&type=1&page_size=10&page="
    get_numbers(baseurl1)





def get_numbers(baseurl1):
    complaint_numbers = []       # 将所有投诉的编号存储在一个列表里
    for i in range(1, 9):
        url = baseurl1 + str(i)
        jsonstr = askUrl(url)
        jsonstr = jsonstr.replace('try{jQuery111206438664184326481_1602743472525(', '')   # 将json文本字符串的头和尾去掉
        jsonstr = jsonstr.replace(');}catch(e){};', '')
        unicodeJson = json.loads(jsonstr)   # 调用JSON的load()方法将json文本字符串转为JSON对象       unicodeJson是一个字典
        # print(unicodeJson)


        itemlist = unicodeJson['result']['data']['lists']
        for item in itemlist:
            sn = item['main']['sn']
            complaint_numbers.append(sn)
    # print(complaint_numbers)



def askUrl(url):
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    request = urllib.request.Request(url,headers= head)
    jsonstr = ''
    try:
        response = urllib.request.urlopen(request)
        jsonstr = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)

    return jsonstr





if __name__ == '__main__':
    main()
    print('爬取完毕！')


