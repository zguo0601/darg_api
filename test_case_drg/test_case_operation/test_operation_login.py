import os
import requests
import allure
import pytest
from common.common_func_read_yaml import  readyaml
from common.common_func_operation import DRG_func




@allure.feature("达人馆运营登录模块")
class Test_drg_login():

    #返回三层目录
    cur_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    yaml_path = os.path.join(cur_path,"data","data.yaml")
    data = readyaml(yaml_path)["login_username_data"]

    @pytest.mark.parametrize("test_input,expect", data)
    @allure.story("运营登录账户测试")
    def test_username(self,test_input,expect):
        '''登录用户名测试'''
        s = requests.session()
        DF = DRG_func(s)
        result = DF.get_Login(test_input)
        assert result["message"]["content"] == expect["message"]["content"]



    @allure.story("运营登录密码错误测试")
    def test_password(self):
        '''登录密码错误11'''
        s = requests.session()
        DF = DRG_func(s)
        result = DF.get_password()
        assert "密码错误" in result



