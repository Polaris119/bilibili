# -*- coding: UTF-8 -*-
"""
# @Time: 2022/8/29 19:10
# @Author: 爱打瞌睡的CV君
# @CSDN: https://blog.csdn.net/qq_44921056
"""

import os
import json
import requests
import chardet
import re
import xlwt

"""
需要根据自己的信息构造请求头信息
"""

headers = {}
cookies = {}

#  创建文件夹
def path_creat():
    _path = "./B站弹幕/"
    if not os.path.exists(_path):
        os.mkdir(_path)
    return _path


# 对爬取的页面内容进行json格式处理
def get_text(url):
    res = requests.get(url=url, headers=headers, cookies=cookies)
    res.encoding = chardet.detect(res.content)['encoding']  # 统一字符编码
    res = res.text
    data = json.loads(res)  # json格式化
    return data


# 根据bv号获取av号和cid（cid和oid是同一个值）
def get_aid(bv):
    url_1 = 'https://api.bilibili.com/x/player/pagelist?bvid={}'.format(bv)

    response = get_text(url_1)
    cid = response['data'][0]['cid']  # 获取cid

    url_2 = 'https://api.bilibili.com/x/web-interface/view?cid={}&bvid={}'.format(cid, bv)
    response_2 = get_text(url_2)

    aid = response_2['data']['aid']  # 获取aid
    return cid, aid


# 根据月份和cid得到这个月份中视频含有弹幕的日期
def get_date(month, cid):
    url = f'https://api.bilibili.com/x/v2/dm/history/index?month={month}&type=1&oid={cid}'
    response = get_text(url)
    dates = response['data']
    return dates


# 根据得到的日期和cid获得弹幕内容
def get_danmu(cid, date):
    url = f'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={cid}&date={date}'
    response = requests.get(url=url, headers=headers, cookies=cookies)
    response.encoding = chardet.detect(response.content)['encoding']
    text = response.text
    data = re.findall("[\u4e00-\u9fa5]+", text)  # 使用正则表达式进行匹配，获取中文弹幕
    return data


def main():
    path = path_creat()
    bv = input('请输入视频的BV号：')
    sheet = input('给你的excel表取一个名字叭：')
    sheet_path = path + sheet + '.xls'
    month = input('输入月份（格式示例：2022-08）：')
    print('爬虫正在搬运数据，请稍后。。。')
    cid, aid = get_aid(bv)  # 获取cid和aid
    dates = get_date(month, cid)  # 获取该月份中存在弹幕信息的日期
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)
    for date in dates:
        worksheet = workbook.add_sheet(date, cell_overwrite_ok=True)  # 以日期命名工作表名
        data = get_danmu(cid, date)  # 获取弹幕数据（列表形式）
        for i in range(len(data)):  # 将弹幕数据依次放入对应日期的工作表中
            worksheet.write(i, 0, data[i])
    workbook.save(sheet_path)  # 保存数据
    print('爬虫搬运数据完毕，请查收数据！！！')


if __name__ == '__main__':
    main()
