import allure
from common.common_func_merchant import Drg_merchant
from common.common_func_SJ import  SF
from common.connect_mysql import select_taskid_number



@allure.feature("达人馆商户端放款模块")
class Test_issu():

    @allure.story("放款列表")
    def test_1(self, merchant_login_fix):
        ''''放款列表'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        result = DM.issu_list()
        assert result["data"]["success"] == True

    @allure.story("放款详情页面-放款单号查询")
    def test_2(self,merchant_login_fix):
        '''放款详情页面-放款单号查询'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        result = DM.issu_detail_systemOrderNumber()
        assert result["data"]["batchNumber"] == "BATCH00001930"

    @allure.story("未放款-待支付")
    def test_3(self,merchant_login_fix):
        '''未放款-待支付'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        result = DM.issu_unpaid()
        assert result["data"]["success"] == True

    @allure.story("单笔放款")
    def test_4(self,merchant_login_fix):
        '''单笔放款'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        issuname = "郑国"
        issuidCard = "350181199006012155"
        issuamount = "1"
        sql = 'select * FROM spman_center.task where  merchant_name = "极限传媒" and status = 1 order by id desc limit 1;'
        r = select_taskid_number(sql)
        taskId = str(r[0]["id"])
        result1 = DM.batchIssu_form(issuname, issuidCard, issuamount, taskId)
        batchNo = result1["data"]["batchNo"]
        result2 = DM.batchIssu_loan(batchNo)
        assert result2["message"]["content"] == "处理中, 请稍后..."

    @allure.story("批量放款")
    def test_5(self,merchant_login_fix):
        '''批量放款'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        sql = 'select * FROM spman_center.task where  merchant_name = "极限传媒" and status = 1 order by id desc limit 1;'
        r = select_taskid_number(sql)
        taskId = str(r[0]["id"])
        result1 = DM.batchIssus_form(taskId)
        batchNo = result1["data"]["batchNo"]
        result2 = DM.batchIssu_loan(batchNo)
        assert result2["message"]["content"] == "处理中, 请稍后..."

    @allure.story("批量放款记录")
    def test_6(self,merchant_login_fix):
        '''批量放款记录'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        result = DM.batchIssu_list()
        assert result["data"]["success"] == True

    @allure.story("取消订单")
    def test_7(self,merchant_login_fix):
        '''取消订单'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        issuname = "张飞"
        issuidCard = "320123198507124578"
        issuamount = "1"
        sql = 'select * FROM spman_center.task where  merchant_name = "极限传媒" and status = 1 order by id desc limit 1;'
        r = select_taskid_number(sql)
        taskId = str(r[0]["id"])
        #放款未实名用户
        result1 = DM.batchIssu_form(issuname, issuidCard, issuamount,taskId)
        batchNo = result1["data"]["batchNo"]
        #放款成功，订单状态为，未放款-待支付
        DM.batchIssu_loan(batchNo)
        #通过批次号查询放款详情，获取充值单号systemOrderNumber
        result3 = DM.issu_detail_batchNumber(batchNo)
        systemOrderNumber = result3["data"]["dataList"][0]["systemOrderNumber"]
        #通过systemOrderNumber取消订单
        result4 = DM.issu_cancel(systemOrderNumber)
        assert result4["message"]["content"] == "取消成功"


