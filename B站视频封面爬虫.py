# -*- coding: UTF-8 -*-
"""
# @Time: 2022/8/29 19:12
# @Author: 爱打瞌睡的CV君
# @CSDN: https://blog.csdn.net/qq_44921056
"""

import os
import json
import requests
import chardet
from fake_useragent import UserAgent

# 随机产生请求头
ua = UserAgent(verify_ssl=False, path='D:/Pycharm/fake_useragent.json')


# 随机切换请求头
def random_ua():
    headers = {
        "accept-encoding": "gzip",  # gzip压缩编码  能提高传输文件速率
        "user-agent": ua.random
    }
    return headers


#  创建文件夹
def path_creat():
    _path = "D:/B站封面/"
    if not os.path.exists(_path):
        os.mkdir(_path)
    return _path


# 对爬取的页面内容进行json格式处理
def get_text(url):
    res = requests.get(url=url, headers=random_ua())
    res.encoding = chardet.detect(res.content)['encoding']  # 统一字符编码
    res = res.text
    data = json.loads(res)  # json格式化
    return data


# 根据bv号获取av号
def get_aid(bv):
    url_1 = 'https://api.bilibili.com/x/player/pagelist?bvid={}'.format(bv)

    response = get_text(url_1)
    cid = response['data'][0]['cid']  # 获取cid

    url_2 = 'https://api.bilibili.com/x/web-interface/view?cid={}&bvid={}'.format(cid, bv)
    response_2 = get_text(url_2)

    aid = response_2['data']['aid']  # 获取aid
    return aid


# 根据av号获取封面图片
def get_image(aid):
    url_3 = 'https://api.bilibili.com/x/web-interface/view?aid={}'.format(aid)
    response_3 = get_text(url_3)
    image_url = response_3['data']['pic']  # 获取图片的下载连接
    image = requests.get(url=image_url, headers=random_ua()).content  # 获取图片
    return image


# 下载封面
def download(image, file_name):
    with open(file_name, 'wb') as f:
        f.write(image)
        f.close()


def main():
    k = 'Y'
    while k == 'Y':  # 根据用户需要一直循环
        path = path_creat()  # 创建保存B站封面的文件夹
        bv = input("请输入视频的bv号：")
        image_name = input("请你给想要下载的封面取一个喜欢的名字叭：")
        aid = get_aid(bv)
        image = get_image(aid)
        file_name = path + '{}.jpg'.format(image_name)
        download(image, file_name)
        print("封面提取完毕^_^")
        k = input("按Y键继续提取，按Q退出：")


if __name__ == '__main__':
    main()
