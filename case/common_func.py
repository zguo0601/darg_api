import os
import requests
from urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
import allure
from common.read_yaml import readyaml
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import pytest

os.environ["yy_host"] = 'https://spman.shb02.net/login'
host = os.environ["yy_host"]





class DRG_func():

    def __init__(self,s):
        self.s = requests.session()

    #公共操作的函数
    @allure.step("登录获取cookie")
    def login(self):
        '''登录获取cookie'''
        url_login_page = host
        data = {
            "port_key": "OPERATION",
            "captcha_type": "LOGIN_CAPTCHA",
            "username": "spman_admin",
            "password": "111111"
        }
        # verify=False（不做安全验证报错SSLerror时候）allow_redirects=False（禁止页面重定向，不禁用的话有可能会获取不到cookies）
        c = self.s.post(url=url_login_page, data=data, verify=False, allow_redirects=False)
        return c


    @allure.step("获取用户列表信息")
    def get_user_list(self):
        url_userlist = 'https://spman.shb02.net/operation/user/list'
        data_1 = {
            "currentPage": "1",
            "pageSize": "20"
        }
        user_list = self.s.post(url=url_userlist, data=data_1)
        return user_list.json()


    @allure.step("新增任务")
    def add_task(self,test_input,expect,delect_task):
        '''新增任务'''
        url_addtask = 'https://spman.shb02.net/operation/task/issue'
        data_2 = {
            "title": "哈哈哈哈1",
            "industryId": "1",
            "industryName": "直播",
            "merchantNumber": "M002137",
            "merchantName": "极限传媒",
            "content": "5",
            "sex": test_input,
            "settleType": "MONTHLY",
            "theme": "5",
            "tag": "1",
            "platform": "9",
            "workPlace": "4",
            "recruitNum": "3",
            "amount": "2",
            "dateLimitType": "LONGTERM",
            "releaseDate": "2020-2-13",
            "autoStatus": "true"
        }
        task_list = self.s.post(url=url_addtask, data=data_2)
        return task_list.json()





if __name__ == '__main__':
    s = requests.session()
    DF = DRG_func(s)
    DF.login()
    res = DF.get_user_list()
    assert res["data"]["success"] == True




