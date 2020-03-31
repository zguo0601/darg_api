import os
import pytest
import requests
import allure
from case.common_func import DRG_func
from common.read_yaml import readyaml
import time


@allure.feature("达人馆用户管理模块")
class Test_drgapi_user():


    @allure.story("获取承揽方信息")
    # 标记测试用例，加个标签
    @pytest.mark.drg_api_login
    def test_1(self,login_fix):
        '''获取承揽方信息'''
        #前置条件,获取最新的cookie
        s = login_fix
        code = time.strftime("%Y%m%d%H%M%S")
        smscode = code[2:8]
        #操作步骤：1.实例化DRG_func(s)，把cookie传入调用的方法里面
        DF = DRG_func(s)
        #2.先获取短信验证码
        DF.get_LoginSmsCode()
        #3.调用登录方法（带上获取的cookie）
        DF.login(smscode)
        #3.调用获取用户列表的方法
        result = DF.get_user_list()
        #4.断言
        assert result["data"]["pageSize"] == 20
        #print(user_list.text)
        #s_code = user_list.status_code
        # print(s_code)
        # print(type(user_list))
        # print(type(user_list.json()["data"]["success"]))
        #assert s_code == 200

    @allure.story("获取发包方信息")
    def test_2(self,login_fix):
        '''获取发包方信息'''
        s = login_fix
        code = time.strftime("%Y%m%d%H%M%S")
        smscode = code[2:8]
        DF = DRG_func(s)
        DF.get_LoginSmsCode()
        DF.login(smscode)
        result = DF.get_merchant_list()
        assert result["message"]["content"] == "查询成功"

    @allure.story("发包方详情")
    def test_3(self,login_fix):
        '''发包方详情'''
        s = login_fix
        code = time.strftime("%Y%m%d%H%M%S")
        smscode = code[2:8]
        DF = DRG_func(s)
        DF.get_LoginSmsCode()
        DF.login(smscode)
        result = DF.merchant_detail()
        print(result)
        assert result["message"]["content"] == "查询成功"

    @allure.story("新增发包方")
    def test_4(self,login_fix,delect_spman_center_merchant,delect_inside_user_center_user):
        '''新增发包方'''
        s = login_fix
        code = time.strftime("%Y%m%d%H%M%S")
        smscode = code[2:8]
        DF = DRG_func(s)
        DF.get_LoginSmsCode()
        DF.login(smscode)
        result = DF.add_merchant()
        print(result)
        assert result["message"]["content"] == "新增成功"

    @allure.story("归属用户信息")
    def test_5(self,login_fix):
        '''归属用户信息'''
        s =login_fix
        code = time.strftime("%Y%m%d%H%M%S")
        smscode = code[2:8]
        DF = DRG_func(s)
        DF.get_LoginSmsCode()
        DF.login(smscode)
        result = DF.user_Merchant()
        assert result["message"]["content"] == "查询成功"

    @allure.story("承揽方详情")
    def test_6(self,login_fix):
        '''承揽方详情'''
        s = login_fix
        code = time.strftime("%Y%m%d%H%M%S")
        smscode = code[2:8]
        DF = DRG_func(s)
        DF.get_LoginSmsCode()
        DF.login(smscode)
        result = DF.get_user_detail()
        assert result["message"]["content"] == "查询成功"

    @allure.story("子公司列表")
    def test_7(self,login_fix):
        '''子公司列表'''
        s = login_fix
        code = time.strftime("%Y%m%d%H%M%S")
        smscode = code[2:8]
        DF = DRG_func(s)
        DF.get_LoginSmsCode()
        DF.login(smscode)
        result = DF.sub_list()
        assert result["data"]["dataList"][0]["status"] == True


    @allure.story("新增子公司")
    def test_8(self,login_fix):
        '''新增子公司'''
        s = login_fix
        code = time.strftime("%Y%m%d%H%M%S")
        smscode = code[2:8]
        DF = DRG_func(s)
        DF.get_LoginSmsCode()
        DF.login(smscode)
        #获取子公司列表，判断，如果有子公司的话，获取子公司id，删除之后再新增。
        # 没有的话新增子公司
        sl = DF.sub_list()
        d_l = sl["data"]["total"]
        if d_l == 0:
            result = DF.add_sub()
            assert result["message"]["content"] == "新增成功"
        else:
            mid = sl["data"]["dataList"][0]["merchantRelationId"]
            DF.del_sub(mid)
            result = DF.add_sub()
            assert result["message"]["content"] == "新增成功"


if __name__ == '__main__':
    # 使用python的方式去执行此命令，结果是与在终端中使用脚本执行的效果是一样的
    pytest.main(["-s","test_info_1.py","-m","drg_api_login"])

