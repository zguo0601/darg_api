import allure
import pytest
from common.common_func_operation import DRG_func



@allure.feature("达人馆赏金管理模块")
class Test_withdrawOrder():


    @allure.story("赏金记录查询")
    def test_1(self,login_fix):
        '''赏金记录查询'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.withdrawOrder_list()
        assert result["data"]["resultList"]["pageSize"] == 20

    @allure.story("赏金详情")
    def test_2(self,login_fix):
        '''赏金详情'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.withdrawOrder_detail()
        assert result["data"]["orderStatusStr"] == "提取成功"