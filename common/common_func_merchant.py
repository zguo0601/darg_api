import json
import os
import random
import requests
import time
import allure
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from common.common_func_SJ import  SF
from common.common_func_user_import import  User_sj
from requests_toolbelt import MultipartEncoder
from common.connect_mysql import select_taskid_number


cur_path = os.path.dirname((os.path.dirname(os.path.realpath(__file__))))
png_path = os.path.join(cur_path, "data", "6.png")
user_issu_path = os.path.join(cur_path, "data", "user_issu.xls")
user_info_path = os.path.join(cur_path, "data", "user_info.xls")



#设置环境变量
os.environ["yy_host"] = 'https://spman.shb02.net'
host = os.environ["yy_host"]

class Drg_merchant():

    def __init__(self,s):
        #---类下实例化----
        self.s = s
        self.u = User_sj()
    @allure.step("商户登录")
    def merchant_login(self,username,password):
        url = host+"/login"
        data = {
            "port_key": "MERCHANT",
            "captcha_type": "LOGIN_CAPTCHA",
            "username": username,
                "password": password,
        }
        rsp = self.s.post(url=url, data=data, verify=False, allow_redirects=False)
        return rsp.text

    @allure.step("用户登录成功")
    def merchant_user_info(self):
        url_user_info = host+"/system/user/info"
        rsp = self.s.post(url_user_info)
        return rsp.text

    @allure.step("用户列表")
    def user_list(self):
        url_user_list = "https://spman.shb02.net/merchant/user/list"
        response = self.s.post(url_user_list)
        return response.json()

    #新增用户步骤  1.上传用户信息
    @allure.step("上传用户信息")
    def add_user(self,name,idcard,mobile):
        url_add_user = "https://spman.shb02.net/merchant/user/form"
        data = {
            'usersJson':'[{"name":%s,"idCard":%s,"mobile":%s}]'%(name,idcard,mobile), #多个参数转化，参数化,如果参数需要引号的情况下,写法为"%s"
        }
        response = self.s.post(url_add_user,data)
        return response.json()
    # 2.通过batchNo,注册用户
    @allure.step("通过batchNo,注册用户,单个新增，批量新增都可以注册")
    def user_batchRegister(self,batchNumber):
        url_user_batchRegister = "https://spman.shb02.net/merchant/user/batchRegister"
        data = {
            "batchNumber":batchNumber,
        }
        response = self.s.post(url_user_batchRegister, data)
        return response.json()

    #批量新增用户步骤1
    @allure.step("批量上传用户信息")
    def user_import(self):
        url_user_import = "https://spman.shb02.net/merchant/user/import"
        self.u.sj_user()
        m = MultipartEncoder(
            fields={"import": ('user_info.xlsx', open(user_info_path, "rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        )
        response = self.s.post(url_user_import,data=m,headers={"Content-Type":m.content_type})
        return response.json()


    @allure.step("充值订单查询")
    def rechargeorder_list(self):
        url_rechargeorder_list =  host+"/merchant/rechargeOrder/list"
        data = {
            "dateType":"apply",
            "orderStatus":"WAIT",
        }
        rsp = self.s.post(url=url_rechargeorder_list, data=data)
        return rsp.json()


    @allure.step("新增充值")
    def merchant_recharge(self,amount,channelOrderNumber):
        url_merchant_recharge =  host+"/merchant/rechargeOrder/rechargeSubmit"
        data = {
            "accountType":"BANK_CARD",
            "amount":amount,
            "channelOrderNumber":channelOrderNumber,#通道编号前端随机生成
            "paymentUrl":"https://darenguan-static-file.oss-cn-shenzhen.aliyuncs.com/drg1586763652192.jpg",
        }
        rsp = self.s.post(url=url_merchant_recharge,data=data)
        return rsp.json()

    @allure.step("查询放款管理页面")
    def issu_list(self):
        url_issu_list = "https://spman.shb02.net/merchant/issu/list"
        data = {
            "dateType": "apply",
        }
        response = self.s.post(url=url_issu_list, data=data)
        return response.json()

    @allure.step("放款详情页面-放款单号查询")
    def issu_detail_systemOrderNumber(self):
        url_issu_detail_systemOrderNumber = "https://spman.shb02.net/merchant/issu/detail"
        data = {
            "systemOrderNumber": "20200509103908019456002137",
        }
        response = self.s.post(url=url_issu_detail_systemOrderNumber, data=data)
        return response.json()

    @allure.step("放款详情页面-批次号查询")
    def issu_detail_batchNumber(self,batchNumber):
        url_issu_detail_batchNumber = "https://spman.shb02.net/merchant/issu/list"
        data = {
            "dateType":"apply",
            "batchNumber": batchNumber,
        }
        response = self.s.post(url=url_issu_detail_batchNumber, data=data)
        return response.json()


    @allure.step("查询未放款-待支付页面")
    def issu_unpaid(self):
        url_issu_unpaid = "https://spman.shb02.net/merchant/issu/list"
        data = {
            "dateType": "apply",
            "orderStatus": "UNPAID",
        }
        response = self.s.post(url=url_issu_unpaid, data=data)
        return response.json()

    #单笔放款步骤1:提交用户信息
    @allure.step("单笔放款-提交用户信息和结算单")
    def batchIssu_form(self,issuname,issuidCard,issuamount,taskId):
        url_batchIssu_form = "https://spman.shb02.net/merchant/batchIssu/form"
        m = MultipartEncoder(
            fields={
                "industryId":"1",
                "issusJson":'[{"name":%s,"idCard":%s,"industry":"","amount":%s}]'%(issuname,issuidCard,issuamount),
                "taskId":taskId,
                #文件名要写对 6.png
                "settle": ('6.png', open(png_path, "rb"), "image/png")}
        )
        response = self.s.post(url_batchIssu_form,data=m,headers={"Content-Type": m.content_type})
        return response.json()

    #单笔放款步骤2: 通过批次号放款，输入支付密码
    @allure.step("单笔放款-确认放款")
    def batchIssu_loan(self,batchNumber):
        url_batchIssu_loan = "https://spman.shb02.net/merchant/batchIssu/loan"
        data = {
            "batchNumber":batchNumber,
            "tradePassword":"111111",
        }
        response = self.s.post(url=url_batchIssu_loan,data=data)
        return response.json()

    @allure.step("批量放款")
    def batchIssus_form(self,taskId):
        url_batchIssus_form = "https://spman.shb02.net/merchant/batchIssu/import"
        m = MultipartEncoder(
            fields={
                "industryId":"1",
                #商户最新的未关闭的任务id
                "taskId":taskId,
                "import": ('user_issu.xlsx', open(user_issu_path, "rb"),
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
                #文件名要写对 6.png
                "settle": ('6.png', open(png_path, "rb"), "image/png")}
        )
        response = self.s.post(url_batchIssus_form,
                               data=m,
                               headers={"Content-Type": m.content_type}
                               )
        return response.json()

    @allure.step("批量放款记录")
    def batchIssu_list(self):
        url_batchIssu_list = "https://spman.shb02.net/merchant/batchIssu/list"
        response = self.s.post(url=url_batchIssu_list)
        return response.json()

    @allure.step("状态：未支付-待放款，取消订单")
    def issu_cancel(self, systemOrderNumber):
        url_issu_cancel = "https://spman.shb02.net/merchant/issu/cancel"
        data = {
            "systemOrderNumber": systemOrderNumber,
        }
        response = self.s.post(url=url_issu_cancel, data=data)
        return response.json()

    @allure.step("资金账户")
    def wallet_selectOne(self):
        url_wallet_selectOne = "https://spman.shb02.net/merchant/wallet/selectOne"
        resposne = self.s.post(url=url_wallet_selectOne)
        return resposne.json()


    @allure.step("查询待开票充值记录")
    def rechargeOrder_wait(self):
        url_rechargeOrder_wait =  host+"/merchant/rechargeOrder/list"
        data = {
            "orderStatus": "SUCCESS",
            "invoiceStatus": "INVOICE_WAIT",
            "currentPage": "1",
            "pageSize": "100",
        }
        rsponse = self.s.post(url=url_rechargeOrder_wait, data=data)
        return rsponse.json()

    @allure.step("开票申请")
    def invoice_apply(self,totalAmount,systemOrderNumbers,s):
        url_invoice_apply =  host+"/merchant/invoice/apply/apply"

        data = {
            "addressId":"2",
            "count":"1",
            "totalAmount":totalAmount,
            "invoiceApplyCategoryDTOJson":"[{'invoiceType':'VAT_INVOICE','remark': '','secondCategoryId': 2,'secondCategoryName':'视频推广','topCategoryId':1,'topCategoryName':'现代服务','totalAmount':%s}]"%s,
            "systemOrderNumbers":systemOrderNumbers
        }
        rsponse = self.s.post(url=url_invoice_apply, data=data)
        return rsponse.json()

    @allure.step("查询充值管理")
    def rechargeOrder_list(self):
        url_rechargeOrder_list = "https://spman.shb02.net/merchant/rechargeOrder/list"
        data = {
            "dateType":"apply",
            "currentPage":"1",
            "pageSize":"20",
        }
        response = self.s.post(url=url_rechargeOrder_list,data=data)
        return response.json()

    @allure.step("充值记录详情页面")
    def rechargeOrder_detail(self):
        url_rechargeOrder_detail = "https://spman.shb02.net/merchant/rechargeOrder/detail"
        data = {
            "systemOrderNumber":"10200512180603020000002137",
        }
        response = self.s.post(url=url_rechargeOrder_detail, data=data)
        return response.json()

    @allure.step("申请记录")
    def apply_list(self):
        url_apply_list = "https://spman.shb02.net/merchant/invoice/apply/list"
        data = {
            "applyStatus":"WAIT",
        }
        response = self.s.post(url=url_apply_list,data=data)
        return response.json()

    @allure.step("已开发票")
    def info_list(self):
        url_info_list = "https://spman.shb02.net/merchant/invoice/info/list"
        response = self.s.post(url=url_info_list)
        return response.json()

    @allure.step("已开发票详情")
    def info_detail(self):
        url_info_detail = "https://spman.shb02.net/merchant/invoice/info/detail"
        data = {
            "id":"207",
        }
        response = self.s.post(url=url_info_detail,data=data)
        return response.json()

    @allure.step("邮寄地址")
    def address_findpage(self):
        url_address_findpage = "https://spman.shb02.net/merchant/address/findPage"
        response = self.s.post(url=url_address_findpage)
        return response.json()

    @allure.step("新增邮寄地址")
    def address_addAddress(self):
        url_address_addAddress = "https://spman.shb02.net/merchant/address/addAddress"
        data = {
            "name":"小可爱",
            "mobile":"178644654567646546",
            "address":"32142134",
            "province":"北京市",
            "provinceCode":"110000",
            "city":"北京市",
            "cityCode":"110100",
            "county":"朝阳区",
            "countyCode":"110105",
        }
        response = self.s.post(url=url_address_addAddress,data=data)
        return response.json()

    @allure.step("删除邮寄地址")
    def def_address(self,id):
        url_def_address = "https://spman.shb02.net/merchant/address/del"
        data = {
            "id":id,
        }
        response = self.s.post(url=url_def_address,data=data)
        return response.json()

    @allure.step("商户信息")
    def account_merchantInfo(self):
        url_account_merchantInfo = "https://spman.shb02.net/merchant/account/merchantInfo"
        response = self.s.post(url=url_account_merchantInfo)
        return response.json()





if __name__ == '__main__':
    ms = requests.session()
    sj = SF()
    username = "M002137"
    password = "111111"
    DM = Drg_merchant(ms)
    DM.merchant_login(username,password)
    amout = '100'
    chanlnumber = '7976845646546'
    name = sj.name()
    idcard = sj.sf()
    mobile = sj.phone()

    #taskId = str(sj.task_id())
    # r1 = DM.user_import()
    # print(r1)

    #单笔放款成功
    issuname = "郑国"
    issuidCard = "350181199006012155"
    issuamount = "1"
    sql = 'select * FROM spman_center.task where  merchant_name = "极限传媒" and status = 1 order by id desc limit 1;'
    r = select_taskid_number(sql)
    taskId = str(r[0]["id"])
    print(taskId)
    result1 = DM.batchIssu_form(issuname,issuidCard,issuamount,taskId)
    batchNo = result1["data"]["batchNo"]
    print(batchNo)
    # result2 = DM.batchIssu_loan(batchNo)
    # print(result2)







    # r1 = DM.address_addAddress()
    # r2 = DM.address_findpage()
    # id = r2["data"]["dataList"][4]["id"]
    # r3 = DM.def_address(id)
    # print(id)
    # print(r2)
    # print(r3)




    #取消订单
    # issuname = "张飞"
    # issuidCard = "320123198507124578"
    # issuamount = "1"
    # sql = 'select * FROM spman_center.task where  merchant_name = "极限传媒" and status = 1 order by id desc limit 1;'
    # r = select_taskid_number(sql)
    # taskId = str(r[0]["id"])
    # r1 = DM.batchIssu_form(issuname,issuidCard,issuamount,taskId)
    # batchNo = r1["data"]["batchNo"]
    # r2 = DM.batchIssu_loan(batchNo)
    # r3 = DM.issu_detail_batchNumber(batchNo)
    # systemOrderNumber = r3["data"]["dataList"][0]["systemOrderNumber"]
    # r4 = DM.issu_cancel(systemOrderNumber)
    # print(r4)


