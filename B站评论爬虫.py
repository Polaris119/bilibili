# -*- coding: UTF-8 -*-
"""
# @Time: 2022/8/29 19:02
# @Author: 爱打瞌睡的CV君
# @CSDN: https://blog.csdn.net/qq_44921056
"""

import json
import requests
import pandas as pd

"""
需要自己根据自己的信息构造请求头信息
"""

headers = {}
cookies = {}

# 对爬取的页面内容进行json格式处理
def get_text(url):
    res = requests.get(url=url, headers=headers, cookies=cookies)
    res.encoding = 'utf-8'
    res = res.text
    data = json.loads(res)  # json格式化
    return data


# 根据bv号获取av号和cid
def get_aid(bv):
    url_1 = 'https://api.bilibili.com/x/player/pagelist?bvid={}'.format(bv)

    response = get_text(url_1)
    cid = response['data'][0]['cid']  # 获取cid

    url_2 = 'https://api.bilibili.com/x/web-interface/view?cid={}&bvid={}'.format(cid, bv)
    response_2 = get_text(url_2)

    aid = response_2['data']['aid']  # 获取aid
    # print(cid, aid)
    return cid, aid


# 获取评论信息
def get_comment(aid, csrf, i):
    url = f'https://api.bilibili.com/x/v2/reply/main?csrf={csrf}&mode=3&next={i}&oid={aid}&plat=1&type=1'
    json_data = get_text(url)  # 获取评论的json数据
    # print(json_data)
    data_s = json_data['data']['replies']  # 筛选出评论数据具体信息
    # print(data_s)
    result = []  # 创建一个空列表，用于放评论的各种信息
    if data_s is not None:
        for data in data_s:
            comment = data['content']['message']  # 评论内容
            # print(comment)
            name = data['member']['uname']  # 评论人员id
            sex = data['member']['sex']  # 评论人员性别
            sign = data['member']['sign']  # 评论人员个性签名
            try:
                location = data['reply_control']['location']  # 评论时所在的属地
            except:
                location = '评论时尚未有ip属地功能'
            '''
            评论的回复，获取方法如上，也需要一个循环不断获取
            replies = data['replies']
            for reply in replies:
                comment_reply = reply['content']['message']  # 评论回复的内容，其它信息获取同理
            '''
            person = [name, sex, location, sign, comment]
            result.append(person)
    else:
        data_s = 1  # 用于终止循环
    return data_s, result


# 对评论内容进行重新排版
def arrange_comment(aid, csrf):
    i = 1
    label = 0
    result = []
    while label != 1:
        label, comment = get_comment(aid, csrf, i)
        # print(comment)
        for data in comment:
            result.append(data)
        i += 1
    return result


def main():
    bv = input("请输入视频的BV号：")
    csrf = ''  # csrf需要输入自己的，可以百度一下，怎么找自己的
    print('爬虫正在搬运数据，请稍后。。。')
    cid, aid = get_aid(bv)
    # get_comment(aid, csrf, i)
    result = arrange_comment(aid, csrf)
    # print(result)
    df = pd.DataFrame(result, columns=['用户名', '用户性别', 'IP属地', '个性签名', '评论内容'])
    df.to_csv(f'./{bv}的评论信息.csv', encoding='utf_8_sig')  # 不加编码格式，保存的数据会出现乱码
    # df.to_excel(f'./{bv}的评论信息.xls')  # 这种方法会报警告：由于不再维护xlwt软件包，在未来版本的pandas中将删除xlwt引擎
    print('爬虫搬运数据完毕，请查收数据！！！')


if __name__ == '__main__':
    main()