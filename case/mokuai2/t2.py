import os
import pytest
import requests
import allure
from case.common_func import *
from common.read_yaml import readyaml
import time


@allure.feature("达人馆用户管理模块")
class Test_drgapi_user():

    def test_1(self,lg):
        '''获取承揽方信息'''
        s = lg
        DF = DRG_func(s)
        u_list = DF.get_user_list()
        print(u_list)
        # 3.断言
        assert u_list["data"]["pageSize"] == 20

    def test_5(self, lg):
        s = lg
        # test_2(s)
        # test_3(s)
        # test_4(s)
        url_merchant_list = 'https://spman.shb02.net/operation/merchant/list'
        data = {
            "currentPage": "1",
            "pageSize": "20"
        }
        merchant_list = s.post(url=url_merchant_list, data=data)
        print(merchant_list.json())

    #@pytest.mark.usefixtures("test_1")
    def test_6(self,lg):
        s = lg
        # test_2(s)
        # test_3(s)
        # test_4(s)
        DF = DRG_func(s)
        res = DF.get_merchant_list()
        print(res)
        # url_merchant_list = 'https://spman.shb02.net/operation/merchant/list'
        # data = {
        #     "currentPage": "1",
        #     "pageSize": "20"
        # }
        # merchant_list = s.post(url=url_merchant_list, data=data)
        # return merchant_list.json()


if __name__ == '__main__':
    # 使用python的方式去执行此命令，结果是与在终端中使用脚本执行的效果是一样的
    pytest.main(["-s","test_info_1.py","-m","drg_api_login"])

