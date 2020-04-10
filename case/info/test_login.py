import os
import requests
import pytest
from common.read_yaml import readyaml
from common.common_func import DRG_func



class Test_drg_login():

    curpath = os.path.dirname(os.path.realpath(__file__))
    # yaml文件的路径
    yamlpath = os.path.join('../../common/test_data.yaml')
    task_data = readyaml(yamlpath)['login_username_data']




    @pytest.mark.parametrize("test_input,expect", task_data)
    def test_username(self,test_input,expect):
        '''登录用户名测试'''
        s = requests.session()
        DF = DRG_func(s)
        result = DF.get_Login(test_input)
        assert result["message"]["content"] == expect["message"]["content"]


    def test_password(self):
        s = requests.session()
        DF = DRG_func(s)
        result = DF.test_password()
        assert "密码错误" in result




