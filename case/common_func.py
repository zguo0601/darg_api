import os
import requests
from urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
import allure
from common.read_yaml import readyaml
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import pytest
from common.SJ import SF
import time




os.environ["yy_host"] = 'http://120.79.243.237:10021'
host = os.environ["yy_host"]

#公共操作的函数
class DRG_func():

    def __init__(self,s):
        self.s = requests.session()


    @allure.step("登录获取cookie")
    def login(self):
        '''登录获取cookie'''
        url_login_page = host+"/login"
        data = {
            "port_key": "OPERATION",
            "captcha_type": "LOGIN_CAPTCHA",
            "username": "spman_admin",
            "password": "111111"
        }
        # verify=False（不做安全验证报错SSLerror时候）allow_redirects=False（禁止页面重定向，不禁用的话有可能会获取不到cookies）
        c = self.s.post(url=url_login_page, data=data, verify=False, allow_redirects=False)
        return c

    @allure.step("获取发包方信息")
    def get_merchant_list(self):
        url_merchant_list = host+'/operation/merchant/list'
        data = {
            "currentPage": "1",
            "pageSize": "20"
        }
        merchant_list = self.s.post(url=url_merchant_list, data=data)
        return merchant_list.json()

    @allure.step("发包方信息详情")
    def merchant_detail(self):
        url_merchant_detail = host+"/operation/merchant/detail"
        data = {
            "merchantNumber":"M002477"
        }
        merchant_detail = self.s.post(url=url_merchant_detail,data=data)
        return merchant_detail.json()


    @allure.step("新增发包方")
    def add_merchant(self):
        url_add_merchant = host+"/operation/merchant/addMerchant"
        data = {
            "industryId":"1",
            "accountFrontFileUrl":"https://darenguan-static-file.oss-cn-shenzhen.aliyuncs.com/by1584930836758.jpg",
            "accountName":"小可爱",
            "accountNumber":"798798986546546",
            "bankBranchName":"中国银行闽清支行",
            "bankName":"中国银行",
            "businessRemark":"5",
            "businessType":"3",
            "city":"福州市",
            "cityCode":"350100",
            "companyAddress":"福建省福州市福清市玉屏街道官塘乾成龙花园1号楼J102店面",
            "companyPhone":"1",
            "contactAddress":"福州仓山万达",
            "contactMail":"1611654sfih@.qq.com",
            "contactName":"小可爱",
            "invoiceContent":"2",
            "invoiceName":"福清市玉屏葛来娣服装店",
            "licenceAddress":"福建省福州市福清市玉屏街道官塘乾成龙花园1号楼J102店面",
            "licenceBusinessScope":"零售服装。(依法须经批准的项目,经相关部门批准后方可开展经营活动)(依法须经批准的项目,经相关部门批准后方可开展经营活动)",
            "licenceCapital":"1000万人民币",
            "licenceCompanyName":"福清市玉屏葛来娣服装店",
            "licenceEstablishTime":"2017-07-02",
            "licenceFileUrl":"https://darenguan-static-file.oss-cn-shenzhen.aliyuncs.com/by1584930809853.jpg",
            "licenceLegalerName":"林志亮",
            "licenceSerialNumber":"22332381M6YCN1X71",
            "licenceType":"个体工商户",
            "platformName":"4",
            "province":"福建省",
            "provinceCode":"350000",
            "shortName":"小可爱",
            "taxNumber":"92350181M6YCN1X71",
            "managerMobile": "18788588987",
            "checkAccountType":"PUB",
            "connectBusinessAffairs":"萌萌哒",
            "bankBranchCode":"104391011909",
            "bankCode":"244"
        }
        result = self.s.post(url=url_add_merchant,data=data)
        return result.json()

    @allure.step("归属用户信息")
    def user_Merchant(self):
        url_user_Merchant = host+"/operation/userMerchant/list"
        data = {
            "merchantNumber":"M002454",
            "currentPage":"1",
            "pageSize":"20"
        }
        result = self.s.post(url=url_user_Merchant,data=data)
        return result.json()


    @allure.step("获取承揽方信息")
    def get_user_list(self):
        url_user_list = host+'/operation/user/list'
        data = {
            "currentPage": "1",
            "pageSize": "20"
        }
        user_list = self.s.post(url=url_user_list, data=data)
        return user_list.json()

    @allure.step("承揽方详情")
    def get_user_detail(self):
        url_user_detail = host+'/operation/user/detail'
        data = {
            "userNumber": "USER002151",
        }
        user_list = self.s.post(url=url_user_detail, data=data)
        return user_list.json()

    @allure.step("新增子公司")
    def add_sub(self):
        url_add_sub = host+"/operation/merchant/addSub"
        data = {
            "merchantNumber":"M002137",
            "status":"true",
            "subMerchantNumber":"M002454",
            "tradePassWd":"111111",
        }
        result = self.s.post(url=url_add_sub,data=data)
        return result.json()

    @allure.step("子公司列表")
    def sub_list(self):
        url_sub_list = "http://120.79.243.237:10021/operation/merchant/subList"
        data = {
            "merchantNumber":"M002137",
        }
        result = self.s.post(url_sub_list,data)
        return result.json()

    @allure.step("删除子公司")
    def del_sub(self,merchantRelationId):
        url_del_sub = "http://120.79.243.237:10021/operation/merchant/deleteSub"
        data = {
            "merchantNumber":"M002137",
            "merchantRelationId":merchantRelationId,
        }
        result = self.s.post(url=url_del_sub,data=data)
        return result.json()



    @allure.step("新增任务,参数组合")
    def add_task_cszh(self,sex,recruitNum,amount):
        '''新增任务'''
        url_addtask = host+'/operation/task/issue'
        data_2 = {
            "title": "哈哈哈哈1",
            "industryId": "1",
            "industryName": "直播",
            "merchantNumber": "M002137",
            "merchantName": "极限传媒",
            "content": "5",
            "sex": sex,
            "settleType": "MONTHLY",
            "theme": "5",
            "tag": "1",
            "platform": "9",
            "workPlace": "4",
            "recruitNum": recruitNum,
            "amount":amount,
            "dateLimitType": "LONGTERM",
            "releaseDate": "2020-2-13",
            "autoStatus": "true"
        }
        task_list = self.s.post(url=url_addtask, data=data_2)
        return task_list.json()

    @allure.step("新增任务,读取yanl")
    def add_task_yaml(self,test_input):
        '''新增任务'''
        url_addtask = host+'/operation/task/issue'
        data_2 = {
            "title": "哈哈哈哈1",
            "industryId": "1",
            "industryName": "直播",
            "merchantNumber": "M002137",
            "merchantName": "极限传媒",
            "content": "5",
            "sex": test_input,
            "settleType": "MONTHLY",
            "theme": "5",
            "tag": "1",
            "platform": "9",
            "workPlace": "4",
            "recruitNum": "10",
            "amount": "1",
            "dateLimitType": "LONGTERM",
            "releaseDate": "2020-2-13",
            "autoStatus": "true"
        }
        task_list = self.s.post(url=url_addtask, data=data_2)
        return task_list.json()





if __name__ == '__main__':
    s = requests.session()
    sex = " "
    amount = "213132fdsa"
    recruitNum = "6d46fd"
    DF = DRG_func(s)
    DF.login()
    # 删除子公司
    sl = DF.sub_list()
    print(sl["data"]["dataList"][0]["status"])

    # d_l = sl["data"]["total"]
    # print(d_l)
    #mid = sl["data"]["dataList"][0]["merchantRelationId"]
    #print(mid)
    #DF.del_sub(mid)
    #新增子公司
    # result = DF.add_sub()
    # print(result)

   # print(eval(result1))
    #assert result["message"]["content"] == "新增成功"





