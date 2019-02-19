#CCB LDZGW Test Version
import csv
import time
import random
import requests

# 参数设定
branch_no = '000000000' # 机构代码
download_times = 50 # 刷刷次数，默认50次
sleep_time_up = 300 # 刷刷间隔上限，默认300秒
sleep_time_low = 60 # 刷刷间隔下限，默认60秒

# 装载User-Agent数据库
ua_list = []
with open('ua_string.csv',encoding='UTF-8') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        ua_list.append(row[0])
base_url = 'https://mobile.ccb.com/workerharbor/servlet/client?PARAMS={"header":{"agent":"mbp1.0","version":"3.00","device":"phone","platform":"web","local":"zh_cn","ext":""},"request":[{"txCode":"WHB006","id":"id0","version":"1.0.0","preassociated":"","params":{"branch_code":"'+branch_no+'",'

# 开始
for i in range(download_times):
    # 随机User-Agent
    ua = random.choice(ua_list)
    ios_list = ('iphone','ipad','ipod')
    if any(s in ua.lower() for s in ios_list):
        #iOS
        client_type = 'ios'
        download_url = 'https://itunes.apple.com/cn/app/id1422953901?mt=8'
        headers = {'user-agent': ua}
    else:
        #Android
        client_type = 'android'
        download_url = 'http://a.app.qq.com/o/simple.jsp?pkgname=com.ccb.workerharbor'
        headers = {'user-agent': ua}
        
    # 组装URL
    final_url = base_url + '"client_type":"' + client_type + '",'
    final_url += '"download_url":"' + download_url + '",'
    final_url += '"ChanReqType":"WHB_JSONP",'
    final_url += '}}]}'

    #print(final_url,ua)

    # POST
    r = requests.post(final_url, data = {"TXCODES":"WHB006"}, headers=headers)
    sleep_time = random.randint(sleep_time_low,sleep_time_up)

    # 报文
    if '"status":"1"' in r.text:
        print("[" + str(i+1) + "/" + str(download_times) + "] Success, next wait " + str(sleep_time) + " sec.")
    else:
        print("[" + str(i+1) + "/" + str(download_times) + "] Fail, next wait " + str(sleep_time) + " sec.")

    # 随机延时
    if i != download_times - 1:
        time.sleep(sleep_time)

print("ALL DONE!")