 # -*- coding:utf-8 -*-

import requests
import urllib
#model name: pycryptodome

import base64

from bs4 import BeautifulSoup
import argparse

#Settings aera

#登陆模式
auth_mode = "PASSWORD"  #1:PASSWORD 2:COOKIES

#统一身份认证账号密码，仅在“PASSWORD”认证模式下需要
stu_id = ""
stu_passwd = ""

#app.nwu.edu.cn认证Cookies，仅在“COOKIES”认证模式下需要
#可以通过浏览器直接获取
stu_varify_cookies = {
    "UUkey":"",
    "eai-sess":""
    }

#调试信息开关
debug_mode = False

#是否在账号密码登陆成功后输出app.nwu.edu.cn认证Cookies（即“COOKIES”认证模式下输入参数）
is_print_cookies = False

#重试最大次数
retry_max = 3

#自定义填报参数
"""
custom_params中每个元素为一个长度为2的列表，如下：
    [字段名，要覆盖的值]
eg.
custom_params = [
    ["sfzx","0"]
]
"""

custom_params = [
    "sfzx", "1",  # 是否在校
    "tw", "1",  # 体温（list）(0-"Below 36";1-"36-36.5";2-"36.5-36.9";3-"36.9-37.3"; ... , i<=8)
    "area", "陕西省 西安市 长安区",
    "city", "西安市",
    "province", "陕西省",
    "address", "陕西省西安市长安区郭杜街道西北大学南校区学生公寓10号楼西北大学长安校区",
    "geo_api_info",
    '{"type":"complete","info":"SUCCESS","status":1,"$Da":"jsonp_687452_","position":{"Q":34.14218,"R":108.87518999999998,"lng":108.87519,"lat":34.14218},"message":"Get ipLocation success.Get address success.","location_type":"ip","accuracy":null,"isConverted":true,"addressComponent":{"citycode":"029","adcode":"610116","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"文苑南路","streetNumber":"11号","country":"中国","province":"陕西省","city":"西安市","district":"长安区","township":"郭杜街道"},"formattedAddress":"陕西省西安市长安区郭杜街道西北大学南校区学生公寓10号楼西北大学长安校区","roads":[],"crosses":[],"pois":[]}',
    # 高德SDK返回值
    "sfcyglq", "0",  # 是否隔离期
    "sfyzz", "0",  # 是否有症状
    "qtqk", "",  # 其他情况
    "ymtys", ""  # 不明（可能是一码通颜色，暂无用）

]

#日志，供其他模块查阅
log = ""

# Login functions
def get_cookies(username='2015000001',password='123456abc'):
    #cookies_res = {}
    global log

    ncov_report_url = "https://app.nwu.edu.cn/site/ncov/dailyup"
    auth_server_url = "http://authserver.nwu.edu.cn"
    action_url = "http://authserver.nwu.edu.cn/authserver/login"
    app_uc_login_url = "https://app.nwu.edu.cn/uc/wap/login"
    app_cas_login_url = "https://app.nwu.edu.cn/a_nwu/api/sso/cas"

    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58"
    }

    
    
def main(username='',password=''):

    cookies_res = {}
    global retry_max
  
    if auth_mode=="PASSWORD":
        print("USE PASSWORD MODE")
        cookies_res = get_cookies(username=stu_id,password=stu_passwd)
    elif auth_mode=="COOKIES":
        print("USE COOKIES MODE")
        cookies_res = stu_varify_cookies
    else:
        print("[ERROR] Unknow auth mode")
        return "Unknow auth mode"
    
   
    else:
        res = sent_report(cookies=cookies_res)
        if res=="操作成功":
            print("\n[FINAL] 自动填报成功")
            return res
        elif res=="您已上报过" or res=="未到上报时间":
            print("\n[FINAL] 还不用填报哦~")
            return res
        else:
            if retry_max>0:
                print("Retry "+str(retry_max)+":")
                retry_max = retry_max-1
                main()
            else:
                print("\n[ERROR] [FINAL] 超过最大重试次数，填报失败！")



if __name__ == "__main__":
    
    #CLI
    parser = argparse.ArgumentParser(description='Auto report CLI')
    parser.add_argument('--cli', type=bool, default=False,help="是否使用命令行参数")   #Is call by cli. If false, use settings at the begining of this file.
    parser.add_argument('--auth_mode', type=str, default="PASSWORD",help="认证模式")
    parser.add_argument('--username', type=str, default=None,help="学工号")
    parser.add_argument('--password', type=str, default=None,help="统一身份认证密码")

    main()
