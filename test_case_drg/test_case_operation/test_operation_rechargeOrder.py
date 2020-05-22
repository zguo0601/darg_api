import time
import pytest
import allure
from common.common_func_operation import DRG_func
from common.common_func_merchant import Drg_merchant
from common.common_func_SJ import  SF

@allure.feature("达人馆发包方付款管理")
class Test_Recharge_order():

    @allure.story("确认充值订单")
    def test_1(self, login_fix,merchant_login_fix):
        '''确认充值订单'''
        s = login_fix
        ms = merchant_login_fix
        sf = SF()
        channelOrderNumber = sf.channelOrderNumber()
        DM = Drg_merchant(ms)
        DF = DRG_func(s)
        paytime = time.strftime("%Y" + "-" + "%m" + "-" + "%d" + " " + "%H" + ":" + "%M" + ":" + "%S")
        #查询是否有未确认订单
        r1 = DF.all_wait_order()
        #如果等于0
        if r1 == 0:
            #商户端新增充值
            DM.merchant_recharge(channelOrderNumber)
            #运营端确认订单
            sysnb = DF.wait_order()
            sysnumber = sysnb["data"]["resultList"]["dataList"][0]["systemOrderNumber"]
            result = DF.sucess_order(paytime, sysnumber)
            assert result["message"]["content"] == "确认成功"
        else:
            #不等于0查询系统单号，确认订单
            sysnb = DF.wait_order()
            sysnumber = sysnb["data"]["resultList"]["dataList"][0]["systemOrderNumber"]
            result = DF.sucess_order(paytime, sysnumber)
            assert result["message"]["content"] == "确认成功"



    @allure.story("查询所有的商户充值记录")
    def test_2(self,login_fix):
        '''查询所有的商户充值记录'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.all_recharge_order()
        assert result["message"]["content"] == "查询成功"

    @allure.story("付款详情")
    def test_3(self,login_fix):
        '''付款详情'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.rechargeOrder_detail()
        assert result["data"]["systemOrderNumber"] == "10200414103247016873002137"