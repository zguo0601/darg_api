import allure
from common.common_func_merchant import Drg_merchant
from common.SJ import SF




@allure.feature("达人馆商户端充值模块")
class Test_Merchant_recharge():

    @allure.story("新增充值")
    def test_1(self,merchant_login_fix):
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        sf = SF()
        amout = sf.year()
        channelOrderNumber = sf.channelOrderNumber()
        result = DM.merchant_recharge(amout,channelOrderNumber)
        assert result["message"]["content"] == "新增充值提交成功"

    @allure.story("查询充值管理")
    def test_2(self,merchant_login_fix):
        '''查询充值管理'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        result = DM.rechargeOrder_list()
        assert result["data"]["rechargeCount"] > 0

    @allure.story("充值记录详情页面")
    def test_3(self,merchant_login_fix):
        '''充值记录详情页面'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        result = DM.rechargeOrder_detail()
        assert result["data"]["systemOrderNumber"] == "10200512180603020000002137"
