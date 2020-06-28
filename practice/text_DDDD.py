import os

import allure
import pytest

from common.common_func_operation import DRG_func

os.environ["yy_host"] = 'https://spman.shb02.net'
host = os.environ["yy_host"]

class DDDD():


    @allure.story("获取承揽方信息")
    # 标记测试用例，加个标签
    @pytest.mark.drg_api_login
    def test_1(self,lg):
        '''获取承揽方信息'''
        s = lg
        DF = DRG_func(s)
        u_list = DF.get_user_list()
        print(u_list)
        # 3.断言
        assert u_list["data"]["pageSize"] == 20


    @allure.story("获取发包方信息")
    def test_2(self):
        '''获取发包方信息'''
        result = self.DF.get_merchant_list()
        assert result["message"]["content"] == "查询成功"


    @allure.story("发包方详情")
    def test_3(self):
        '''发包方详情'''
        result = self.DF.merchant_detail()
        assert result["message"]["content"] == "查询成功"

# @pytest.fixture()
# def test_1():
#     print("开始请求")
#     s = requests.session()
#     print("打开首页")
#     url_merchant_list = "https://spman.shb02.net/admin/login"
#     s.get(url=url_merchant_list)
#     print("获取验证码")
#     url = "https://spman.shb02.net/common/reset/getLoginSmsCode"
#     data = {
#         "loginPort": "OPERATION",
#         "principal": "spman_admin",
#     }
#     res = s.post(url, data)
#     print("登录成功")
#     url_login = "https://spman.shb02.net/login"
#     data = {
#         "port_key": "OPERATION",
#         "captcha_type": "LOGIN_CAPTCHA",
#         "username": "spman_admin",
#         "password": "111111",
#         "mobile_key": 200402,
#     }
#     # verify=False（不做安全验证报错SSLerror时候）allow_redirects=False（禁止页面重定向，不禁用的话有可能会获取不到cookies）
#     r = s.post(url_login, data, verify=False, allow_redirects=False)
#     return s

# def test_2(test_1):
#     s = test_1
#     url_merchant_list = "https://spman.shb02.net/admin/login"
#     return s.get(url=url_merchant_list)


# def test_3(test_1):
#     s = test_1
#     #test_2(s)
#     url = "https://spman.shb02.net/common/reset/getLoginSmsCode"
#     data = {
#         "loginPort":"OPERATION",
#         "principal":"spman_admin",
#     }
#     res = s.post(url,data)
#     print(res.json())

# def test_4(test_1):
#     s = test_1
#     # test_2(s)
#     # test_3(s)
#     url_login = "https://spman.shb02.net/login"
#     data = {
#         "port_key": "OPERATION",
#         "captcha_type": "LOGIN_CAPTCHA",
#         "username": "spman_admin",
#         "password": "111111",
#         "mobile_key": 200402,
#     }
#     # verify=False（不做安全验证报错SSLerror时候）allow_redirects=False（禁止页面重定向，不禁用的话有可能会获取不到cookies）
#     r = s.post(url_login, data, verify=False, allow_redirects=False)
#     print(r.status_code)







