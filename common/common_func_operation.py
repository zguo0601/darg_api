import os
import requests
from urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
import allure
from common.common_func_read_yaml import  readyaml
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import pytest
import time
from common.common_func_SJ import  SF
from requests_toolbelt import MultipartEncoder



#设置环境变量
os.environ["yy_host"] = 'https://spman.shb02.net'
host = os.environ["yy_host"]


cur_path = os.path.dirname((os.path.dirname(os.path.realpath(__file__))))
rar_path = os.path.join(cur_path, "data", "1575270331(1).rar")



#公共操作的函数
class DRG_func():

    def __init__(self,s):
        #---类下实例化----
        self.s = s

    @allure.step("获取短信验证码")
    def get_Login(self,test_input):
        """获取短信验证码，测试运营登录
        :param:test_input  用户名
        return:            r.json()
        """
        url_get_LoginSmsCode = host + "/common/reset/getLoginSmsCode"
        data = {
            "loginPort": "OPERATION",
            "principal": test_input,
        }
        r = self.s.post(url=url_get_LoginSmsCode, data=data,)
        return r.json()

    def get_password(self):
        """
        :param: smscode  登录验证码
        :return:
        """
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

    @allure.step("通过发包方名称查询")
    def inquire_merchant_list(self,test_input):
        url_inquire_merchant_list = "https://spman.shb02.net/operation/merchant/list"
        data = {
            "shortName":test_input,
        }
        response = self.s.post(url=url_inquire_merchant_list,data=data)
        return response.json()

    @allure.step("获取发包方信息")
    def get_merchant_list(self):
        url_merchant_list = host+'/operation/merchant/list'
        data = {
            "currentPage": "1",
            "pageSize": "20"
        }
        merchant_list = self.s.post(url=url_merchant_list, data=data)
        return merchant_list.json()

    @allure.step("通过发包方简称查询")
    def shortname__query(self):
        url_shortname__query = host + '/operation/merchant/list'
        data = {
            "shortName":"极限传媒",
            "currentPage": "1",
            "pageSize": "20"
        }
        response = self.s.post(url=url_shortname__query, data=data)
        return response.json()

    @allure.step("通过纳税人识别号查询")
    def taxNumber__query(self):
        url_taxNumber__query = host + '/operation/merchant/list'
        data = {
            "taxNumber": "913213223235882089",
            "currentPage": "1",
            "pageSize": "20"
        }
        response = self.s.post(url=url_taxNumber__query, data=data)
        return response.json()

    @allure.step("通过管理员姓名查询")
    def managerName__query(self):
        url_managerName__query = host + '/operation/merchant/list'
        data = {
            "managerName": "帅雷雷",
            "currentPage": "1",
            "pageSize": "20"
        }
        response = self.s.post(url=url_managerName__query, data=data)
        return response.json()




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
        """
        新增发需要传参参数
        :param accountName: 开户人
        :param contactMail: 联系邮箱
        :param contactName: 联系人
        :param licenceSerialNumber: 营业执照号
        :param shortName: 发包方简称
        :param managerMobile: 手机号
        :return:
        """
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
            "licenceCompanyName":"福清市(玉屏)葛来娣服装店",
            "licenceEstablishTime":"2017-07-02",
            "licenceFileUrl":"https://darenguan-static-file.oss-cn-shenzhen.aliyuncs.com/by1584930809853.jpg",
            "licenceLegalerName":"林志亮",
            "licenceSerialNumber":licenceSerialNumber,#营业执照号码唯一
            "licenceType":"个体工商户",
            "platformName":"4",
            "province":"福建省",
            "provinceCode":"350000",
            "shortName":shortName + "科技有限公司",
            "taxNumber":"92350181M6YCN1X71",
            "managerMobile": managerMobile,
            "checkAccountType":"PUB",
            "connectBusinessAffairs":"萌萌哒",
            "bankBranchCode":"104391011909",
            "bankCode":"244"
        }
        result = self.s.post(url=url_add_merchant,data=data)
        return result.json()

    @allure.step("修改发包方出金方式为银行卡")
    def merchant_editDetail_bybankcard(self,issuType,bankBranchCode):
        url = "https://spman.shb02.net/operation/merchant/editDetail"
        data = {
            "merchantNumber":"M002137",
            "accountName":"__极限传媒___@#*.DHF",
            "accountNumber":"6396221159666585458",
            "bankBranchName":"中国工商银行总行清算中心",
            "bankName":"中国工商银行",
            "issuType": issuType,
            "city":"北京市",
            "cityCode":"110100",
            "companyAddress":"术阳县人民医院行政楼元楼",
            "companyPhone":"8888-888-8888",
            "contactAddress":"福州仓山万达",
            "contactMail":"6365245@163.com",
            "contactMobile":"18526999857",
            "contactName":"帅雷雷",
            "invoiceName":"沐阳乐乾投资管理有限公",
            "jsonRate":'{"percent":6.5,"base":6.5,"fixed":6.5}',
            "jsonInvoiceInfoList":'[{"agreementRecordId":548,"industryId":1,"authStatus":"SUCCESS","authStatusStr":"已签署","reason":null,"industryName":"直播","invoiceContent":"0","businessType":"1","platformName":"2","businessRemark":"3","contractPdfUrl":null}]',
            "licenceAddress":"术阳县人民医院行政楼元楼",
            "licenceBusinessScope":"动日资及投资管理;投资咨询、经济信息咨询、商务信息咨询,企业管理策品、企水形象策划、会务服务、摄影服务、保洁服务;计算机网络工程路图文制作:文化办公用品及设备、日用百货、家用电器、五金交电销品、电脑及配件、音响器材、照相器材、机电设备、金属材料、算材(公化子品除外)、家具、体育用品、通讯器材、燃料油、润滑油、机械设备销包品油;汽油、般汽油、印代油:一般危化品:柴油(闭林滑用油桥内点、60C***(不得储存,经营品种涉及其行政许可的展定行相关手续)。(依法须经批准的项目,经相关部门批准后方可开营活动)",
            "licenceCapital":"50万元整",
            "licenceCompanyName":"极限传媒科技有限公司",
            "licenceEstablishTime":"2014-12-29",
            "licenceFileUrl":"https://darenguan-static-file.oss-cn-shenzhen.aliyuncs.com/drg1581907101438.jpg",
            "licenceLegalerName":"帅雷雷",
            "licenceSerialNumber":"913213223235882089",
            "licenceType":"有限责任公司",
            "limitMonthRecharge":"20000000",
            "phone":"8888-888-8888",
            "province":"北京市",
            "provinceCode":"110000",
            "shortName":"极限传媒",
            "signEndDate":"2021-02-17",
            "signStartDate":"2020-02-17",
            "taxNumber":"913213223235882089",
            "totalDayIssu":"10000000",
            "totalDayRecharge":"20000000",
            "totalMonthIssu":"10000000",
            "totalMonthRecharge":"20000000",
            "tradeMaxAmountIssu":"10000000",
            "tradeMaxAmountRecharge":"10000000",
            "tradeMinAmountIssu":"0",
            "tradeMinAmountRecharge":"0",
            "managerName":"帅雷雷",
            "managerMobile":"18526999857",
            "taxPriceType":"CONTAIN_TAX_PRICE",
            "checkAccountType":"PUB",
            "bankBranchCode":bankBranchCode,
        }
        response = self.s.post(url,data)
        return response.json()


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


    @allure.step("承揽方名称(userNumbers)查询")
    def userNumbers_query(self):
        url_userNumbers_query = host + '/operation/user/list'
        data = {
            "userNumbers":"USER002151",
            "currentPage": "1",
            "pageSize": "20"
        }
        response = self.s.post(url=url_userNumbers_query, data=data)
        return response.json()

    @allure.step("承揽方微信手机号查询")
    def wechatMobile_query(self):
        url_wechatMobile_query = host + '/operation/user/list'
        data = {
            "wechatMobile": "18120798657",
            "currentPage": "1",
            "pageSize": "20"
        }
        response = self.s.post(url=url_wechatMobile_query, data=data)
        return response.json()


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

    @allure.step("极限商户新增任务")
    def add_task(self):
        '''新增任务'''
        url_addtask = host + '/operation/task/issue'
        data_2 = {
            "title": "极限任务",
            "industryId": "1",
            "industryName": "直播",
            "merchantNumber": "M002137",
            "merchantName": "极限传媒",
            "content": "5",
            "sex": "MALE",
            "settleType": "MONTHLY",
            "theme": "5",
            "tag": "1",
            "platform": "9",
            "workPlace": "4",
            #"recruitNum": recruitNum,
            "amount": "50",
            "dateLimitType": "LONGTERM",
            "releaseDate": "2020-2-13",
            "autoStatus": "true"
        }
        task_list = self.s.post(url=url_addtask, data=data_2)
        return task_list.json()

    @allure.step("新增任务,参数组合")
    def add_task_cszh(self,sex,recruitNum,amount):
        '''新增任务'''
        url_addtask = host+'/operation/task/issue'
        data_2 = {
            "title": " ",
            "industryId": "55",
            "industryName": " ",
            "merchantNumber": "M002137",
            "merchantName": " ",
            "content": " ",
            "sex": sex,
            "settleType": "MONTHLY",
            "theme": "5",
            "tag": "1",
            "platform": "  ",
            "workPlace": "4",
            "recruitNum": recruitNum,
            "amount":amount,
            "dateLimitType": "LONGTERM",
            "releaseDate": '2020-05-28',
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

    #表单格式上传文件
    @allure.step("重新上传结算单")
    def upload_Attachment(self):
        url = "https://spman.shb02.net/operation/issu/uploadAttachment"
        m = MultipartEncoder(
            fields={
                "batchNumber":"BATCH00001059",
                # 文件名要写对 6.png
                "settleFile": ('1575270331(1).rar', open(rar_path, "rb"), "application/octet-stream")}
        )
        response = self.s.post(url, data=m, headers={"Content-Type": m.content_type})
        return response.json()

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
        """
        :param paytime: 确认订单时间
        :param systemOrderNumber: 充值单号
        :return:
        """
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
    def invoice_apply_list(self,applyStatus):
        url_invoice_apply_list =  host+"/operation/invoice/apply/list"
        data = {
            "applyStatus": applyStatus,
            # "startDate": "2020-04-16",
            # "endDate": "2020-04-16",
        }
        response = self.s.post(url=url_invoice_apply_list, data=data)
        return response.json()


    @allure.step("申请合并开票")
    def invoice_merger(self,batchNumbers,merchantNumber):
        url = "https://spman.shb02.net/operation/invoice/info/merger"
        data = {
            "batchNumbers":batchNumbers,
            "merchantNumber":merchantNumber,
        }
        response = self.s.post(url,data)
        return response.json()

    @allure.step("新增发票信息")
    def invoice_add(self,invoiceCode,invoiceDate,invoiceNumber,taxAmount,totalAmount,amount,invoiceBatchNumber,merchantNumber):
        """
        :param invoiceCode: 发票代码
        :param invoiceDate: 开票日期
        :param invoiceNumber: 发票号码
        :param taxAmount: 税额
        :param totalAmount: 税价合计
        :param amount: 金额
        :param invoiceBatchNumber: 发票批次号
        :param merchantNumber: 商户编号
        :return:
        """
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
            "invoiceBatchNumber": invoiceBatchNumber,
            "merchantNumber": merchantNumber,
        }
        response = self.s.post(url=url_invoice_add, data=data)
        return response.json()

    @allure.step("填写快递单号")
    def invoice_addEmsInfo(self,batchNumber,merchantNumber,invoiceBatchNumber,emsOrderNumber):
        """
        填写快递单号
        :param batchNumber: 发票批次号
        :param merchantNumber: 商户编号
        :param emsOrderNumber: 快递单号
        :return:
        """
        url_invoice_addEmsInfo =  host+"/operation/invoice/apply/addEmsInfo"
        data = {
            "batchNumber": batchNumber,
            "merchantNumber": merchantNumber,
            "invoiceBatchNumber": invoiceBatchNumber,
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



    emsOrderNumber = sj.phone()
    invoiceCode = sj.phone()
    invoiceNumber = sj.phone()
    licenceSerialNumber = time.strftime("%Y%m%d%H%M%S")
    smscode = licenceSerialNumber[2:8]
    invoiceDate = time.strftime("%Y"+"-"+"%m"+"-"+"%d"+" "+"%H"+":"+"%M"+":"+"%S")
    accountName = sj.name()
    contactMail = sj.get_email()
    contactName = sj.name()
    licenceSerialNumber = time.strftime("%Y%m%d%H%M%S")
    shortName = sj.name()
    managerMobile = sj.phone()

    DF = DRG_func(s)
    response = DF.login_sucess(smscode)
    result = DF.add_merchant(accountName,contactMail,contactName,licenceSerialNumber,shortName,managerMobile)
    print(result)
    #分行CODE前端随机生成
    # bankBranchCode = sj.phone()
    # #出金模式银行卡：BANK_CARD
    # #出金模式小程序钱包：APPLET_WALLET
    # issuType = "BANK_CARD"
    # r = DF.merchant_editDetail_bybankcard(issuType,bankBranchCode)
    # print(r)

    #新增发包方
    # r1 = DF.add_merchant(accountName,contactMail,contactName,licenceSerialNumber,shortName,managerMobile)
    # print(r1)



    #sysnumber = DF.add_merchant(accountName,shorrtname,contactMail,contactName,licenceSerialNumber,managerMobile)


    #确认开票待审核
    # applyStatus = 'WAIT'
    # r1 = DF.invoice_apply_list(applyStatus)
    # print(r1)
    # totalAmount1 = r1["data"]["resultList"]["dataList"][0]["totalAmount"]  # 获取税价合计金额，类型为 str
    # batchNumber = r1["data"]["resultList"]["dataList"][0]["batchNumber"]  # 获取批次号
    # merchantNumber = r1["data"]["resultList"]["dataList"][0]["merchantNumber"]  # 获取用户编号
    # print(batchNumber)
    # print(merchantNumber)
    # f_totalAmount = float(totalAmount1)  # 类型为str的金额转化为 浮点型
    # y_totalAmount = round(f_totalAmount, 2)  # 浮点型 税价合计金额 四舍五入
    # f_amount = y_totalAmount / (1 + 0.1)  # 税率10%
    # amount = round(f_amount, 2)  # 金额
    # f_taxAmount = y_totalAmount - amount
    # taxAmount = round(f_taxAmount, 2)  # 税额
    # # # 申请合并开票
    # r2 = DF.invoice_merger(batchNumber,merchantNumber)
    # print(r2)
    # applyStatus = 'HANDLE'
    # r4 = DF.invoice_apply_list(applyStatus)
    # invoiceBatchNumber = r4["data"]["resultList"]["dataList"][0]["invoiceBatchNumber"]
    # print(invoiceBatchNumber)
    # r3 = DF.invoice_add(invoiceCode, invoiceDate, invoiceNumber, taxAmount, y_totalAmount, amount, invoiceBatchNumber,merchantNumber)
    # print(r3)


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



















