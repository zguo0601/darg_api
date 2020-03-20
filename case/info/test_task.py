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

    #绝对路径,先找出文件的上一层，在把文件加到上一层路径后面就等于文件的绝对路径
    #用例的路径
    curpath = os.path.dirname(os.path.realpath(__file__))
    #yaml文件的路径
    yamlpath = os.path.join('../../common/test_data.yaml')
    test_data = readyaml(yamlpath)['test_data']
    #print(test_data)
    # 暂时不执行该用用例@pytest.mark.skip("阻塞bug")，执行时会跳过这个测试用例，开发把这个问题解决了，就可以把这个skip注释掉
    # @pytest.mark.skip("阻塞bug")
    # 标记测试用例，可以区分之后想要执行按标记来执行测试用例,
    # 执行方法在终端中使用命令脚本命令去执行： pytest 文件名 -m 标记名称
    # （pytest test_b.py -m drgapi）,
    # 反选（pytest test_b.py -m not drgapi）
    @allure.story("新增任务")
    @pytest.mark.drg_api_task
    @pytest.mark.parametrize("test_input,expect",test_data)
    def test_1(self,login_fix,test_input,expect,delect_task):
        '''新增任务'''
        s = requests.session()
        DF = DRG_func(s)
        DF.login()
        result = DF.add_task(test_input,expect,delect_task)
        assert result["message"]["content"] == expect["message"]["content"]

if __name__ == '__main__':
    # 使用python的方式去执行此命令，结果是与在终端中使用脚本执行的效果是一样的
    pytest.main(["-s","test_info_1.py","-m","drg_api_login"])

