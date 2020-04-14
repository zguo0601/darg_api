import os
import requests
from urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
import allure
from common.read_yaml import readyaml
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import pytest
import time
from common.SJ import SF


#设置环境变量
os.environ["yy_host"] = 'https://spman.shb02.net'
host = os.environ["yy_host"]


#公共操作的函数
class DRG_func():

    def __init__(self,s,):
        #---类下实例化----
        self.s = s

    @allure.step("获取短信验证码")
    def get_Login(self,test_input):
        '''获取短信验证码'''
        url_get_LoginSmsCode = host + "/common/reset/getLoginSmsCode"
        data = {
            "loginPort": "OPERATION",
            "principal": test_input,
        }
        r = self.s.post(url=url_get_LoginSmsCode, data=data,)
        return r.json()

    def test_password(self):
        s = requests.session()
        DF = DRG_func(s)
        code = time.strftime("%Y%m%d%H%M%S")
        smscode = code[2:8]
        DF.get_LoginSmsCode()
        '''登录获取cookie'''
        url_login_page = "https://spman.shb02.net/login"
        data = {
            "port_key": "OPERATION",
            "captcha_type": "LOGIN_CAPTCHA",
            "username": "spman_admin",
            "password": "11111111",
            "mobile_key": smscode,
        }
        # verify=False（不做安全验证报错SSLerror时候）allow_redirects=False（禁止页面重定向，不禁用的话有可能会获取不到cookies）
        r = s.post(url=url_login_page, data=data, verify=False, allow_redirects=False)
        return r.text

    @allure.step("获取短信验证码")
    def get_LoginSmsCode(self):
        '''获取短信验证码'''
        url_get_LoginSmsCode = host + "/common/reset/getLoginSmsCode"
        data = {
            "loginPort": "OPERATION",
            "principal": "spman_admin",
        }
        r = self.s.post(url=url_get_LoginSmsCode, data=data, )
        return r

    @allure.step("登录获取cookie")
    def login(self,smscode):
        '''登录获取cookie'''
        url_login_page = host+"/login"
        data = {
            "port_key": "OPERATION",
            "captcha_type": "LOGIN_CAPTCHA",
            "username": "spman_admin",
            "password": "111111",
            "mobile_key": smscode,
        }
        # verify=False（不做安全验证报错SSLerror时候）allow_redirects=False（禁止页面重定向，不禁用的话有可能会获取不到cookies）
        r = self.s.post(url=url_login_page, data=data,verify=False,allow_redirects=False)
        return r


    @allure.step("获取验证码+登录成功")
    def login_sucess(self,smscode):
        self.get_LoginSmsCode()
        return self.login(smscode)



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
    def add_merchant(self,accountName,shortName,contactMail,contactName,licenceSerialNumber,managerMobile):
        url_add_merchant = host+"/operation/merchant/addMerchant"
        data = {
            "industryId":"1",
            "accountFrontFileUrl":"https://darenguan-static-file.oss-cn-shenzhen.aliyuncs.com/by1584930836758.jpg",
            "accountName":accountName,
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
            "contactMail":contactMail,#联系邮箱唯一
            "contactName":contactName,
            "invoiceContent":"2",
            "invoiceName":"福清市玉屏葛来娣服装店",
            "licenceAddress":"福建省福州市福清市玉屏街道官塘乾成龙花园1号楼J102店面",
            "licenceBusinessScope":"零售服装。(依法须经批准的项目,经相关部门批准后方可开展经营活动)(依法须经批准的项目,经相关部门批准后方可开展经营活动)",
            "licenceCapital":"1000万人民币",
            "licenceCompanyName":"福清市玉屏葛来娣服装店",
            "licenceEstablishTime":"2017-07-02",
            "licenceFileUrl":"https://darenguan-static-file.oss-cn-shenzhen.aliyuncs.com/by1584930809853.jpg",
            "licenceLegalerName":"林志亮",
            "licenceSerialNumber":licenceSerialNumber,#营业执照号码唯一
            "licenceType":"个体工商户",
            "platformName":"4",
            "province":"福建省",
            "provinceCode":"350000",
            "shortName":shortName+"科技有限公司",
            "taxNumber":"92350181M6YCN1X71",
            "managerMobile": managerMobile,
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
    def get_user_detail(self,):
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
    def sub_list(self,):
        url_sub_list = host + "/operation/merchant/subList"
        data = {
            "merchantNumber":"M002137",
        }
        result = self.s.post(url_sub_list,data)
        return result.json()

    @allure.step("删除子公司")
    def del_sub(self,merchantRelationId):

        url_del_sub = host + "/operation/merchant/deleteSub"
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
    def add_task_yaml(self,test_input="MALE"):
        '''新增任务'''
        url_add_task = host+'/operation/task/issue'
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
        add_task = self.s.post(url=url_add_task, data=data_2)
        return add_task.json()

    @allure.step("任务列表")
    def task_list(self,status=''):
        url_task_list = host + "/operation/task/list"
        data = {
            "status":status,
            "currentPage":"1",
            "pageSize":"20",
        }
        task_list = self.s.post(url_task_list,data)
        return task_list.json()

    @allure.step("关闭任务")
    def close_task(self,task_id):
        url_close_task= host + "/operation/task/close"
        data = {
            "id":task_id,
        }
        result = self.s.post(url_close_task,data)
        return result.json()

    @allure.step("任务报名信息")
    def task_applicants(self):
        url_task_applicants =  host +"/operation/task/applicants"
        data = {
            "currentPage":"1",
            "pageSize":"20",
            "taskId":"519",
        }
        result = self.s.post(url=url_task_applicants,data=data)
        return result.json()


    @allure.step("上传完税证明")
    def update_apply(self):
        url_update_apply =  host +"/operation/issu/uploadTaxCertificate"
        data = {
            "systemOrderNumber":"20200403161904016364001236",
            "taxesUrl":"https://darenguan-static-file.oss-cn-shenzhen.aliyuncs.com/drg1585903011042.jpg",
        }
        result = self.s.post(url=url_update_apply,data=data)
        return result.json()

    @allure.step("付款记录")
    def issu_list(self):
        url_issu_list = host+"/operation/issu/list"
        data = {
            "dateType":"apply",
            "startDate":"2020-04-01",
            "currentPage":"1",
            "pageSize":"20",
        }
        result = self.s.post(url=url_issu_list,data=data)
        return result.json()

    @allure.step("放款详情")
    def issu_detail(self):
        url_issu_detail = host+"/operation/issu/detail"
        data = {
            "systemOrderNumber":"20200410114901016767001236",
        }
        response = self.s.post(url=url_issu_detail,data=data)
        return response.json()

    @allure.step("批量放款记录")
    def issuBatchApply_detail(self):
        url_issuBatchApply_detail = host+"/operation/issuBatchApply/list"
        data = {
            "currentPage": "1",
            "pageSize": "20",
        }
        response = self.s.post(url=url_issuBatchApply_detail, data=data)
        return response.json()

    @allure.step("批次放款记录")
    def batch_issu_detail(self):
        url_batch_issu_detail = host+"/operation/issu/list"
        data = {
            "dateType": "apply",
            "batchNumber": "BATCH00001080",
            "currentPage": "1",
            "pageSize": "20",
        }
        response = self.s.post(url=url_batch_issu_detail, data=data)
        return response.json()

    @allure.step("查询商户所有的充值订单")
    def all_recharge_order(self):
        url_all_wait_order = host + "/operation/rechargeOrder/list"
        data = {
            "dateType": "apply",
            "currentPage": "1",
            "pageSize": "20",
        }
        response = self.s.post(url=url_all_wait_order, data=data)
        return response.json()

    @allure.step("查询所有未确认充值订单")
    def all_wait_order(self):
        url_all_wait_order = host + "/operation/rechargeOrder/list"
        data = {
            "dateType": "apply",
            "orderStatus": "WAIT",
            "currentPage": "1",
            "pageSize": "20",
            # "startDate": "2020-04-14",
            # "endDate": "2020-04-14",
        }
        response = self.s.post(url=url_all_wait_order, data=data)
        return response.json()["data"]["rechargeCount"]


    @allure.step("查询未确认充值订单")
    def wait_order(self):
        url_wait_order = host+"/operation/rechargeOrder/list"
        data = {
            "dateType":"apply",
            "orderStatus":"WAIT",
            "currentPage":"1",
            "pageSize":"20",
        }
        response = self.s.post(url=url_wait_order,data=data)
        return response.json()["data"]["resultList"]["dataList"][0]["systemOrderNumber"]

    @allure.step("确认充值订单")
    def sucess_order(self,paytime,systemOrderNumber):
        url_sucess_order = host+"/operation/rechargeOrder/wait/manualConfirm"
        data = {
            "paymentTime":paytime,
            "systemOrderNumber":systemOrderNumber,
        }
        response = self.s.post(url=url_sucess_order,data=data)
        return response.json()





if __name__ == '__main__':
    s = requests.session()
    sj = SF()
    shorrtname = sj.name()
    accountName = sj.name()
    contactMail = sj.get_email()
    contactName = sj.name()
    managerMobile = sj.phone()
    licenceSerialNumber = time.strftime("%Y%m%d%H%M%S")
    smscode = licenceSerialNumber[2:8]
    paytime = time.strftime("%Y"+"-"+"%m"+"-"+"%d"+" "+"%H"+":"+"%M"+":"+"%S")
    DF = DRG_func(s)
    response = DF.login_sucess(smscode)
    sysnumber = DF.add_merchant(accountName,shorrtname,contactMail,contactName,licenceSerialNumber,managerMobile)
    print(sysnumber)


















