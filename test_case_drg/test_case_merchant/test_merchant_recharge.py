import allure
import os
import pytest
from common.common_func_read_yaml import  readyaml
from common.common_func_merchant import Drg_merchant
from common.common_func_SJ import  SF




@allure.feature("达人馆商户端充值模块")
class Test_Merchant_recharge():
    # 返回三层目录
    cur_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    yaml_path = os.path.join(cur_path, "data", "data.yaml")
    data = readyaml(yaml_path)["merchant_amout"]

    @pytest.mark.parametrize("test_input,expect", data)
    @allure.story("新增充值")
    def test_1(self,merchant_login_fix,test_input,expect):
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        sf = SF()
        channelOrderNumber = sf.channelOrderNumber()
        result = DM.merchant_recharge(test_input,channelOrderNumber)
        assert result["message"]["content"] == expect["message"]["content"]

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
