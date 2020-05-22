import os
import allure
import pytest
from common.common_func_merchant import Drg_merchant
from common.common_func_read_yaml import  readyaml
import requests


@allure.feature("达人馆商户登录模块")
class Test_Merchant():

    @allure.story("商户端用户名登录测试")
    def test_merchant_username(self):
        '''商户端用户名登录测试'''
        s = requests.session()
        username = "123456"
        password = "111111"
        DM = Drg_merchant(s)
        rsp = DM.merchant_login(username,password)
        assert "未知账号，请联系管理" in  rsp

    @allure.story("商户端用户密码错误测试")
    def test_mechant_password(self):
        '''商户端用户密码错误测试'''
        s = requests.session()
        username = "M002137"
        password = "00"
        DM = Drg_merchant(s)
        rsp = DM.merchant_login(username, password)
        assert "密码错误" in rsp

    @allure.story("商户登录成功")
    def test_login_sucess(self):
        '''商户登录成功'''
        s = requests.session()
        username = "M002137"
        password = "111111"
        DM = Drg_merchant(s)
        DM.merchant_login(username, password)
        rsp = DM.merchant_user_info()
        assert "极限传媒" in rsp











