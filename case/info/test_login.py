import os
import requests
import allure
import pytest
from common.read_yaml import readyaml
from common.common_func import DRG_func


@allure.feature("达人馆运营登录模块")
class Test_drg_login():

    #在case文件夹下运行测试用例
    curpath = os.path.dirname(os.path.realpath(__file__))
    print(curpath)
    # yaml文件的路径
    yamlpath = os.path.join('../common/data.yaml')
    data = readyaml(yamlpath)['login_username_data']

    # # 在info文件夹下运行测试用例
    # curpath = os.path.dirname(os.path.realpath(__file__))
    # print(curpath)
    # # yaml文件的路径
    # yamlpath = os.path.join('../../common/data.yaml')
    # data = readyaml(yamlpath)['login_username_data']




    @pytest.mark.parametrize("test_input,expect", data)
    @allure.story("运营账户登录测试")
    def test_username(self,test_input,expect):
        '''登录用户名测试'''
        s = requests.session()
        DF = DRG_func(s)
        result = DF.get_Login(test_input)
        assert result["message"]["content"] == expect["message"]["content"]



    @allure.story("运营密码登录测试")
    def test_password(self):
        s = requests.session()
        DF = DRG_func(s)
        result = DF.test_password()
        assert "密码错误" in result


if __name__ == '__main__':
    a = Test_drg_login()
    curpath = os.path.dirname(os.path.realpath(__file__))
    print(curpath)
    # yaml文件的路径
    yamlpath = os.path.join('../../common/data.yaml')
    data = readyaml(yamlpath)['login_username_data']
    print(data)

