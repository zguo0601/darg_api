import os
import pytest
import requests
import json
import time
from common.connect_mysql import excute_sql
from common.read_yaml import readyaml
import allure
from case.common_func import DRG_func



@allure.feature("达人馆用任务模块")
class Test_drgapi_task():

    @classmethod
    def setup_class(cls):
        # 前置条件，打开浏览器
        cls.s = requests.session()
        # 操作步骤：1.实例化DRG_func(s)
        cls.DF = DRG_func(cls.s)
        code = time.strftime("%Y%m%d%H%M%S")
        smscode = code[2:8]
        # 2.获取验证码+获取登录成功
        cls.DF.login_sucess(smscode)

    @classmethod
    def teardown_class(cls):
        cls.s = requests.session()
        cls.s.close()



    # 暂时不执行该用用例@pytest.mark.skip("阻塞bug")，执行时会跳过这个测试用例，开发把这个问题解决了，就可以把这个skip注释掉
    # @pytest.mark.skip("阻塞bug")
    # 标记测试用例，可以区分之后想要执行按标记来执行测试用例,
    # 执行方法在终端中使用命令脚本命令去执行： pytest 文件名 -m 标记名称
    # （pytest test_b.py -m drgapi）,
    # 反选（pytest test_b.py -m not drgapi）
    @allure.story("新增任务,参数组合")
    @pytest.mark.drg_api_task
    @pytest.mark.parametrize("sex",["123","dshfsdh"])
    @pytest.mark.parametrize("amount",[" ","dshfsdh"])
    @pytest.mark.parametrize("recruitNum",[" ","dshfsdh"])
    def test_1(self,delect_task,sex,recruitNum,amount):
        '''新增任务'''

        result = self.DF.add_task_cszh(sex,recruitNum,amount)
        assert result["message"]["content"] == "系统异常"


    # 绝对路径,先找出文件的上一层，在把文件加到上一层路径后面就等于文件的绝对路径
    # 测试用例的路径
    curpath = os.path.dirname(os.path.realpath(__file__))
    # yaml文件的路径
    yamlpath = os.path.join('../../common/test_data.yaml')
    task_data = readyaml(yamlpath)['task_sex_data']
    @allure.story("新增任务,读取yaml")
    @pytest.mark.parametrize("test_input,expect", task_data)
    def test_2(self,delect_task,test_input,expect,):
        '''新增任务,读取yaml'''

        result = self.DF.add_task_yaml(test_input)
        assert result["message"]["content"] == expect["message"]["content"]

    @allure.story("任务列表")
    def test_3(self):
        '''任务列表'''
        result = self.DF.task_list()
        assert result["message"]["content"] == "查询成功"

    @allure.story("关闭任务")
    def test_4(self,update_spman_center_task):
        '''关闭任务'''
        status = "true"
        #查询已发布任务
        result = self.DF.task_list(status)
        #获取已发布任务id
        task_id = result["data"]["dataList"][0]["id"]
        #关闭此id的任务
        r_close = self.DF.close_task(task_id)
        assert r_close["message"]["content"] == "操作成功"




if __name__ == '__main__':
    # 使用python的方式去执行此命令，结果是与在终端中使用脚本执行的效果是一样的
    pytest.main(["-s","test_info_1.py","-m","drg_api_login"])

