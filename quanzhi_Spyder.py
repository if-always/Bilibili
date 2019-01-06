# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 21:02:08 2018

@author: iamhexin
"""

import requests
import pymysql
import time
import random
import numpy as np
import pandas as pd


keys = [
    'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
    'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
    'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
    'Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3'
]


def get_json(num):
    # 获取网页静态源代码
    try:
        headers = {  
            'User-Agent':keys[random.randint(0, len(keys) - 1)],  
            'Host':'api.bilibili.com',                         
            'Referer':'https://www.bilibili.com/video/av1328701'
            }  
        proxies = {
            'http': 'http://183.166.129.53:8080'
        }
        url = 'https://api.bilibili.com/x/v2/reply?pn='+ str(num) +'&type=1&oid=1328701&sort=0'
        #url = 'https://api.bilibili.com/x/v2/reply?pn='+ str(num) +'&type=1&oid=9659814&sort=0'
#https://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=1328701&sort=0           
        response = requests.get(url, headers = headers,proxies=proxies)
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None

def get_comment_info(page_info):
    datas = []
    infos = page_info['data']['replies']
    for info in infos:  
        item = {}
        item['floor'] = info['floor']
        item['ctime'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(info['ctime'])) 
        item['comment'] = info['content']['message']
        if len(item['comment']) > 1000:
            item['comment'] = item['comment'][:1000]
        item['clike'] = info['like']
        item['rcount'] = info['rcount']
        item['userid'] = info['mid']
        item['username'] = info['member']['uname']
        item['usersex'] = info['member']['sex']
        try:
            item['usersign'] = info['member']['sign']
        except:
            item['usersign'] = ""
        item['userlevel'] = info['member']['level_info']['current_level']
        datas.append(item)

    return datas

def main():
    datas = []
    for n in range(445,0,-1):  
        # 对每个网页读取JSON, 获取每页数据  
        page = get_json(n)  
        data = get_comment_info(page)
        datas.extend(data)
        print('已经抓取第{}页'.format(n))  
        #time.sleep(5+random.randint(1,5))   
    floor = [item['floor'] for item in datas]
    ctime = [item['ctime'] for item in datas]
    comment = [item['comment'] for item in datas]
    clike = [item['clike'] for item in datas]
    rcount = [item['rcount'] for item in datas]
    userid = [item['userid'] for item in datas]
    username = [item['username'] for item in datas]
    usersex = [item['usersex'] for item in datas]
    usersign = [item['usersign'] for item in datas]
    userlevel = [item['userlevel'] for item in datas]

    df = pd.DataFrame({'floor':floor,'userid':userid,'usersex':usersex,'username':username,'time':ctime,'like':clike,
        'rcount':rcount,'comment':comment,'usersign':usersign,'userlevel':userlevel})
    df = df.set_index('floor')

    df.to_excel('../Data-Set/bilibili/reply.xlsx')

if __name__== "__main__":   
    main()  
    

    
    
