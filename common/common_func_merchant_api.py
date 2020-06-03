import os
import time
import requests
import allure
from common.common_func_SJ import  SF
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#公共操作的函数
class API_merchant():

    def __init__(self,s):
        self.s = s

    @allure.step("商户登录")
    def merchant_login(self):
        url = "https://spman.shb02.net/login"
        data = {
            "port_key": "MERCHANT",
            "captcha_type": "LOGIN_CAPTCHA",
            "username": "M002137",
            "password": "111111",
        }
        rsp = self.s.post(url=url, data=data, verify=False, allow_redirects=False)
        return rsp

    @allure.step("获取商户信息")
    def merchant_Info(self):
        url = "https://spman.shb02.net/merchant/account/merchantInfo"
        response = self.s.post(url)
        return response.json()

    @allure.step("获取商户密码")
    def get_apimerchant_password(self,merchantPriKey,systemPubKey):
        url = "https://spman.shb02.net/test/api/util/proxy"
        data = {
            "environment": "https://spman.shb02.net/api",
            "merchantNumber": "M002137",
            #商户私钥
            "merchantPriKey":merchantPriKey,
            "method": "/util/getPassword",
            #商户公钥
            "systemPubKey":systemPubKey,
            "type": "asymmetric",
        }
        response = self.s.post(url,json=data)
        return response.json()

    @allure.step("api新增商户")
    def add_api_merchant(self,merchantPriKey,systemPubKey,password,requesterUserIdentity,idCard,mobile,name):
        url = "https://spman.shb02.net/test/api/util/proxy"
        headers = {
            "Accept":"application/json, text/plain, */*",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.66 Safari/537.36",
            "Content-Type":"application/json;charset=UTF-8",
        }
        data = {
            'merchantNumber':'M002137',
            "merchantPriKey":merchantPriKey,
            "systemPubKey":systemPubKey,
            'password':password,
            'type':'symmetry',
            'content':'[{"industryId":"1","requesterUserIdentity":"%s","idCard":"%s","mobile":"%s","name":"%s",'
                      '"idCardBackFileUrl":"https://darenguan-static-file.oss-cn-shenzhen.aliyuncs.com/drg1587699987268.jpg",'
                      '"idCardFrontFileUrl":"https://darenguan-static-file.oss-cn-shenzhen.aliyuncs.com/drg1587699987268.jpg"}]'
                      %(requesterUserIdentity,idCard,mobile,name),
            'environment':'https://spman.shb02.net/api',
            'method':'/user/auth',
        }
        respnose = self.s.post(url,json=data,headers=headers)
        return respnose.json()

    @allure.step("用户状态查询")
    def get_status(self,merchantPriKey,systemPubKey,password,idCard):
        url = "https://spman.shb02.net/test/api/util/proxy"
        json = {
            'merchantNumber': 'M002137',
            "merchantPriKey": merchantPriKey,
            "systemPubKey": systemPubKey,
            'password': password,
            'type': 'symmetry',
            'content': '{"idCard":%s}'%idCard,
            'environment': 'https://spman.shb02.net/api',
            'method': '/user/detail',
        }
        respnose = self.s.post(url, json=json)
        return respnose.json()

    @allure.step("单笔充值")
    def recharge_single(self,merchantPriKey,systemPubKey,password,amount,requesterOrderNumber):
        url = "https://spman.shb02.net/test/api/util/proxy"
        data = {
            'merchantNumber': 'M002137',
            "merchantPriKey": merchantPriKey,
            "systemPubKey": systemPubKey,
            'password': password,
            'type': 'symmetry',
            #金额1是1分
            'content': '{"amount":"%s","requesterOrderNumber":"%s","accountType":"BANK_CARD",'
                       '"paymentUrl":"https://darenguan-static-file.oss-cn-shenzhen.aliyuncs.com/drg1586763652192.jpg"}'
                       %(amount,requesterOrderNumber),
            'environment': 'https://spman.shb02.net/api',
            'method': "/recharge/single",
        }
        response = self.s.post(url,json=data)
        return response.json()

    @allure.step("充值详情查询")
    def recharge_detail(self,systemOrderNumber,merchantPriKey,password,systemPubKey):
        url = 'https://spman.shb02.net/test/api/util/proxy'
        data = {
            "content":'{"systemOrderNumber":%s}'%systemOrderNumber,
            "environment":"https://spman.shb02.net/api",
            "merchantNumber":"M002137",
            "merchantPriKey":merchantPriKey,
            "method":"/recharge/detail",
            "password":password,
            "systemPubKey":systemPubKey,
            "type":"symmetry",
        }
        response = self.s.post(url,json=data)
        return response.json()

    @allure.step("商户放款")
    def issu_batch(self,requesterOrderNumber,merchantPriKey,password,systemPubKey):
        url = 'https://spman.shb02.net/test/api/util/proxy'
        data = {
            'content':'[{"amount":"10","industryId":"1","requesterOrderNumber":"%s",'
                      '"settleUrls":"https://darenguan-static-file.oss-cn-shenzhen.aliyuncs.com/drg1587699987268.jpg",'
                      '"idCard":"350181199006012588","accountType":"BANK_CARD","name":"阿斯顿"}]'%requesterOrderNumber,
            'environment':'https://spman.shb02.net/api',
            'merchantNumber':'M002137',
            'merchantPriKey':merchantPriKey,
            'method':'/issu/batch',
            'password':password,
            'systemPubKey':systemPubKey,
            'type':'symmetry',
        }
        response = self.s.post(url,json=data)
        return response.json()

    @allure.step('放款查询')
    def issu_datail(self,systemOrderNumber,merchantPriKey,password,systemPubKey):
        url = 'https://spman.shb02.net/test/api/util/proxy'
        data = {
            "content": '{"systemOrderNumber":%s}' % systemOrderNumber,
            "environment": "https://spman.shb02.net/api",
            "merchantNumber": "M002137",
            "merchantPriKey": merchantPriKey,
            "method": "/issu/detail",
            "password": password,
            "systemPubKey": systemPubKey,
            "type": "symmetry",
        }
        response = self.s.post(url, json=data)
        return response.json()




if __name__ == '__main__':
    s = requests.session()
    api = API_merchant(s)
    sj = SF()
    requesterUserIdentity = "jx" + sj.phone()
    idCard = sj.idcard()
    mobile = sj.phone()
    name = sj.name()

    #商户端登录
    h = api.merchant_login()
    #获取商户私钥和系统公钥
    info = api.merchant_Info()
    merchantPriKey = info["data"]["merchantPriKey"]
    systemPubKey = info["data"]["systemPubKey"]
    #获取api商户密码
    result1 = api.get_apimerchant_password(merchantPriKey,systemPubKey)
    password = result1["password"]


    # #api商户新增用户
    # result2 = api_m.add_api_merchant(merchantPriKey,systemPubKey,password,requesterUserIdentity,idCard,mobile,name)
    # print(result2)


    #查询用户详情
    # id = "110109194806130490"
    # result2 = api.get_status(merchantPriKey,systemPubKey,password,id)
    # print(result2)

    #充值,金额100等于1块
    #amount = "100"
    #请求单号
    # r_n = time.strftime("%Y%m%d%H%M%S")
    # requesterOrderNumber = 'jxcz' + r_n
    # result3 = api.recharge_single(merchantPriKey,systemPubKey,password,amount,requesterOrderNumber)
    # systemOrderNumber = result3["systemOrderNumber"]
    # print(result3)
    # print(systemOrderNumber)

    #查询充值详情
    # result4 = api.recharge_detail(systemOrderNumber,merchantPriKey,password,systemPubKey)
    # print(result4)

    #商户放款
    requesterOrderNumber = 'jxfk' + time.strftime("%Y%m%d%H%M%S")
    result5 = api.issu_batch(requesterOrderNumber,merchantPriKey,password,systemPubKey)
    systemOrderNumber = result5[0]["systemOrderNumber"]
    print(result5)
    result6 = api.issu_datail(systemOrderNumber,merchantPriKey,password,systemPubKey)
    print(result6)





