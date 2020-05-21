import time
import allure
from common.common_func_merchant import Drg_merchant
from common.common_func_operation import DRG_func
from common.SJ import SF


@allure.feature("达人馆商户端开票模块")
class Test_invoice_apply():


    @allure.story("开票申请")
    def test_1(self,merchant_login_fix,login_fix):
        '''开票申请'''
        sf = SF()
        channelOrderNumber = sf.channelOrderNumber()
        amount = sf.day()
        s = login_fix
        DF = DRG_func(s)
        paytime = time.strftime("%Y" + "-" + "%m" + "-" + "%d" + " " + "%H" + ":" + "%M" + ":" + "%S")
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        #查询是否有开票充值记录
        r = DM.rechargeOrder_wait()
        rechargeCount = r["data"]["rechargeCount"]
        #判断充值记录为0的情况下
        if rechargeCount == 0:
            #新增充值记录
            print("新增充值")
            DM.merchant_recharge(amount,channelOrderNumber)
            #运营端确认
            sysnumber1 = DF.wait_order()
            sysnumber = sysnumber1["data"]["resultList"]["dataList"][0]["systemOrderNumber"]
            DF.sucess_order(paytime,sysnumber)
            print("运营端确认充值记录")
            # 查询开票充值几率不为0的情况下开票申请，先查询出开票充值记录里面的充值金额和系统单号
            recharge_detail = DM.rechargeOrder_wait()
            totalAmount = recharge_detail["data"]["resultList"]["dataList"][0]["amountStr"]
            s_totalAmount = recharge_detail["data"]["resultList"]["dataList"][0]["amountStr"]
            systemOrderNumbers = recharge_detail["data"]["resultList"]["dataList"][0]["systemOrderNumber"]
            print("查询开票充值记录，返回税价合计金额、放款单号")
            # 提交开票申请
            result = DM.invoice_apply(totalAmount, systemOrderNumbers, s_totalAmount)
            print("提交开票申请成功")
            assert result["message"]["content"] == "操作成功"

        else:
            #不为0的情况下开票申请，先查询出开票充值记录里面的充值金额和系统单号
            print("查询开票充值记录，返回税价合计金额、放款单号")
            recharge_detail = DM.rechargeOrder_wait()
            totalAmount = recharge_detail["data"]["resultList"]["dataList"][0]["amountStr"]
            s_totalAmount = recharge_detail["data"]["resultList"]["dataList"][0]["amountStr"]
            systemOrderNumbers = recharge_detail["data"]["resultList"]["dataList"][0]["systemOrderNumber"]
            #提交开票申请
            result =DM.invoice_apply(totalAmount, systemOrderNumbers, s_totalAmount)
            print("提交开票申请成功")
            assert result["message"]["content"] == "操作成功"

    @allure.story("申请记录")
    def test_2(self,merchant_login_fix):
        '''申请记录'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        result = DM.apply_list()
        assert result["message"]["content"] == "查询成功"

    @allure.story("已开发票")
    def test_3(self,merchant_login_fix):
        '''已开发票'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        result = DM.info_list()
        assert result["data"]["count"] > 0

    @allure.story("已开发票详情")
    def test_4(self,merchant_login_fix):
        '''已开发票详情'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        result = DM.info_detail()
        assert result["data"]["merchantName"] == "极限传媒"

    @allure.story("邮寄地址")
    def test_5(self,merchant_login_fix):
        '''邮寄地址'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        result = DM.address_findpage()
        assert result["message"]["content"] == "查询成功"

    @allure.story("新增和删除邮寄地址")
    def test_6(self,merchant_login_fix):
        '''新增和删除邮寄地址'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        #新增邮寄地址
        result1 = DM.address_addAddress()
        result2 = DM.address_findpage()
        id =  result2["data"]["dataList"][4]["id"]
        #删除邮寄地址
        result3 = DM.def_address(id)
        assert result3["message"]["content"] == "操作成功"

