import os
import pytest
import requests
import allure
from case.common_func import DRG_func




@allure.feature("达人馆用户管理模块")
class Test_drgapi_user():



    @allure.story("获取承揽方信息")
    # 标记测试用例，加个标签
    @pytest.mark.drg_api_login
    def test_1(self,login_fix):
        '''获取承揽方信息'''
        s = requests.session()
        DF = DRG_func(s)
        DF.login()
        result = DF.get_user_list()
        assert result["data"]["success"] == True
        #print(user_list.text)
        #s_code = user_list.status_code
        # print(s_code)
        # print(type(user_list))
        # print(type(user_list.json()["data"]["success"]))
        #assert s_code == 200



if __name__ == '__main__':
    # 使用python的方式去执行此命令，结果是与在终端中使用脚本执行的效果是一样的
    pytest.main(["-s","test_info_1.py","-m","drg_api_login"])

