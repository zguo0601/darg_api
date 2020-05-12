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

    def __init__(self,s):
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
    def add_merchant(self,accountName,contactMail,contactName,licenceSerialNumber,shortName,managerMobile):
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
        return response.json()

    @allure.step("确认充值订单")
    def sucess_order(self,paytime,systemOrderNumber):
        url_sucess_order = host+"/operation/rechargeOrder/wait/manualConfirm"
        data = {
            "paymentTime":paytime,
            "systemOrderNumber":systemOrderNumber,
        }
        response = self.s.post(url=url_sucess_order,data=data)
        return response.json()

    @allure.step("付款详情")
    def rechargeOrder_detail(self):
        url_rechargeOrder_detail = host+"/operation/rechargeOrder/detail"
        data = {
            "systemOrderNumber":"10200414103247016873002137",
        }
        response = self.s.post(url=url_rechargeOrder_detail, data=data)
        return response.json()


    @allure.step("赏金记录查询")
    def withdrawOrder_list(self):
        url_withdrawOrder_list =  host+"/operation/withdrawOrder/list"
        data = {
            "dateType": "apply",
            "currentPage": "1",
            "pageSize": "20",
        }
        response = self.s.post(url=url_withdrawOrder_list, data=data)
        return response.json()

    @allure.step("赏金详情")
    def withdrawOrder_detail(self):
        url_withdrawOrder_detail =  host+"/operation/withdrawOrder/detail"
        data = {
            "systemOrderNumber": "30200408173431016567002015",
        }
        response = self.s.post(url=url_withdrawOrder_detail, data=data)
        return response.json()

    @allure.step("达人馆财务管理模块")
    def invoice_list(self):
        url_invoice_list =  host+"/operation/invoice/apply/list"
        data = {
            "currentPage": "1",
            "pageSize": "20",
        }
        response = self.s.post(url=url_invoice_list, data=data)
        return response.json()

    @allure.step("发票申请详情")
    def invoice_detail(self):
        url_invoice_detail =  host+"/operation/invoice/apply/list"
        data = {
            "batchNumber": "BATCH00000947",
        }
        response = self.s.post(url=url_invoice_detail, data=data)
        return response.json()

    @allure.step("已开发票")
    def invoice_info_list(self):
        url_invoice_info_list =  host+"/operation/invoice/info/list"
        data = {
            "status": "1",
            "batchNumber": "BATCH00000947",
        }
        response = self.s.post(url=url_invoice_info_list, data=data)
        return response.json()

    @allure.step("已开发票详情")
    def invoice_info_detail(self):
        url_invoice_info_detail =  host+"/operation/invoice/info/detail"
        data = {
            "id": "70",
        }
        response = self.s.post(url=url_invoice_info_detail, data=data)
        return response.json()

    @allure.step("查询待处理发票")#返回税价合计金额
    def invoice_apply_list(self):
        url_invoice_apply_list =  host+"/operation/invoice/apply/list"
        data = {
            "applyStatus": "WAIT",
            # "startDate": "2020-04-16",
            # "endDate": "2020-04-16",
        }
        response = self.s.post(url=url_invoice_apply_list, data=data)
        return response.json()

    @allure.step("新增发票信息")
    def invoice_add(self,invoiceCode,invoiceDate,invoiceNumber,taxAmount,totalAmount,amount,batchNumber,merchantNumber):
        url_invoice_add =  host+"/operation/invoice/info/add"
        data = {
            "invoiceCode": invoiceCode,
            "invoiceDate": invoiceDate,
            "invoiceNumber": invoiceNumber,
            "invoiceType": "VAT_INVOICE",
            "topCategoryId": "1",
            "topCategoryName": "现代服务",
            "secondCategoryId": "2",
            "secondCategoryName": "视频推广",
            "rate": "10",
            "taxAmount": taxAmount,#税额
            "totalAmount": totalAmount,#税价合计
            "amount": amount,#金额
            "batchNumber": batchNumber,
            "merchantNumber": merchantNumber,
        }
        response = self.s.post(url=url_invoice_add, data=data)
        return response.json()

    @allure.step("填写快递单号")
    def invoice_addEmsInfo(self,batchNumber,merchantNumber,emsOrderNumber):
        url_invoice_addEmsInfo =  host+"/operation/invoice/apply/addEmsInfo"
        data = {
            "batchNumber": batchNumber,
            "merchantNumber": merchantNumber,
            "emsOrderNumber": emsOrderNumber,
            "emsType": "SF",
        }
        response = self.s.post(url=url_invoice_addEmsInfo, data=data)
        return response.json()

    @allure.step("驳回开票申请")
    def unpass_invoice(self,batchNumber,merchantNumber):
        url_unpass_invoice =  host+"/operation/invoice/apply/unPass"
        data = {
            "batchNumber":batchNumber,
            "merchantNumber":merchantNumber,
            "reason":"贵公司当月所开发票已超过月限额。",
        }
        response = self.s.post(url=url_unpass_invoice, data=data)
        return response.json()

    @allure.step("发包方钱包查询")
    def merchantWallet_list(self):
        url_merchantWallet_list =  host+"/operation/merchantWallet/list"
        response = self.s.post(url=url_merchantWallet_list)
        return response.json()

    @allure.step("发包方钱包详情")
    def merchantWallet_selectOne(self):
        url_merchantWallet_selectOne =  host+"/operation/merchantWallet/selectOne"
        data = {"ownId":"2137",}
        response = self.s.post(url=url_merchantWallet_selectOne,data=data)
        return response.json()

    @allure.step("承揽方钱包")
    def userWallet_list(self):
        url_userWallet_list =  host+"/operation/userWallet/list"
        response = self.s.post(url=url_userWallet_list)
        return response.json()

    @allure.step("承揽方钱包详情")
    def userWallet_selectOne(self):
        url_userWallet_selectOne =  host+"/operation/userWallet/selectOne"
        data = {"ownId": "2151", }
        response = self.s.post(url=url_userWallet_selectOne, data=data)
        return response.json()

    @allure.step("平台钱包")
    def systemWallet_selectOne(self):
        url_systemWallet_selectOne =  host+"/operation/systemWallet/selectOne"
        response = self.s.post(url=url_systemWallet_selectOne)
        return response.json()

    @allure.step("通道钱包")
    def channelWallet_list(self):
        url_channelWallet_list =  host+"/operation/channelWallet/list"
        response = self.s.post(url=url_channelWallet_list)
        return response.json()

    @allure.step("通道钱包详情")
    def channelWallet_selectOne(self):
        url_channelWallet_selectOne =  host+"/operation/channelWallet/selectOne"
        data = {"ownId":"1",}
        response = self.s.post(url=url_channelWallet_selectOne,data=data)
        return response.json()

    # @allure.step("我的账户")
    # def operator_account(self):
    #     url_operator_account = "https://spman.shb02.net/#/account/index"
    #     response = self.s.get(url=url_operator_account)
    #     return response.text
    #
    #
    # @allure.step("账户安全页面")
    # def operator_js(self):
    #     url_operator_js = host+"/static/assets/operator/js/chunk-d6f12bba.bcb174fd.js"
    #     response = self.s.get(url=url_operator_js)
    #     return response.text

    @allure.step("员工管理-员工列表页面")
    def staff_management(self):
        url_staff_management = "https://spman.shb02.net/system/account/list"
        response = self.s.post(url=url_staff_management)
        return response.json()

    @allure.step("员工管理-员工角色页面")
    def the_role(self):
        url_the_role = "https://spman.shb02.net/system/role/list"
        response = self.s.post(url=url_the_role)
        return response.json()

    @allure.step("员工管理-员工角色页面-新增角色")
    def add_role(self):
        url_add_role = "https://spman.shb02.net/system/role/add"
        data = {
            "roleName":"管理员",
            "remark":"管理员",
        }
        response = self.s.post(url=url_add_role,data=data)
        return response.json()

    @allure.step("员工管理-员工角色页面-新增员工")
    def add_account(self):
        url_add_account = "https://spman.shb02.net/system/account/add"
        data = {
            "roleId": "120",
            "loginName": "PAY1589252317124",
            "passWd": "111111",
            "mobile": "18759888519",
            "userName": "1",
            "status": "1",
        }
        response = self.s.post(url=url_add_account, data=data)
        return response.json()


    @allure.step("员工管理-员工角色页面-删除员工")
    def delete_account(self,id):
        url_delete_account = "https://spman.shb02.net/system/account/delete"
        data = {
            "id": id,
        }
        response = self.s.post(url=url_delete_account, data=data)
        return response.json()

    @allure.step("员工修改密码")
    def modify_pwd(self):
        url_modify_pwd = "https://spman.shb02.net/system/account/modifyPwd"
        data = {
            "id":"14406",
            "roleId":"123",
            "loginName":"OPERATION006359002535",
            "passWd":"111111",
            "mobile":"13559936333",
            "userName":"刘主任",
            "status":"1",
        }
        response = self.s.post(url=url_modify_pwd,data=data)
        return response.json()

    @allure.step("编辑员工信息")
    def modify_account(self):
        url_modify_account = "https://spman.shb02.net/system/account/modify"
        data = {
            "id":"14644",
            "roleId":"119",
            "loginName":"OPERATION006359002930",
            "mobile":"18759888529",
            "userName":"大大",
            "status":"1",
        }
        response = self.s.post(url=url_modify_account, data=data)
        return response.json()



if __name__ == '__main__':
    s = requests.session()
    sj = SF()
    shorrtname = sj.name()
    accountName = sj.name()
    contactMail = sj.get_email()
    contactName = sj.name()
    managerMobile = sj.phone()
    emsOrderNumber = sj.phone()
    invoiceCode = sj.phone()
    invoiceNumber = sj.phone()
    licenceSerialNumber = time.strftime("%Y%m%d%H%M%S")
    smscode = licenceSerialNumber[2:8]
    invoiceDate = time.strftime("%Y"+"-"+"%m"+"-"+"%d"+" "+"%H"+":"+"%M"+":"+"%S")
    DF = DRG_func(s)
    response = DF.login_sucess(smscode)
    #sysnumber = DF.add_merchant(accountName,shorrtname,contactMail,contactName,licenceSerialNumber,managerMobile)
    r1 = DF.modify_account()

    print(r1)


    #print(sysnumber)
    # r2 = DF.invoice_wait_list()
    # totalAmount1 = r2["data"]["resultList"]["dataList"][0]["totalAmount"]
    # batchNumber = r2["data"]["resultList"]["dataList"][0]["batchNumber"]
    # merchantNumber = r2["data"]["resultList"]["dataList"][0]["merchantNumber"]
    # totalAmount = float(totalAmount1)
    # amount1 = totalAmount/(1+0.1)
    # amount= round(amount1, 2)
    # taxAmount1 = totalAmount - amount
    # taxAmount = round(taxAmount1, 2)
    # print(sysnumber)
    # print(totalAmount)
    # print(batchNumber)
    # print(merchantNumber)
    # print(amount)
    # print(taxAmount)
    # DF.invoice_add(invoiceCode,invoiceDate,invoiceNumber,taxAmount,totalAmount,amount,batchNumber,merchantNumber)
    # r = DF.invoice_addEmsInfo(batchNumber,merchantNumber,emsOrderNumber)
    # assert r["message"]["content"] == "操作成功"
    # print(r)



















