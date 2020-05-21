import allure
import pytest
from common.common_func_merchant import Drg_merchant
from common.SJ import SF

sj = SF()


@allure.feature("达人馆商户端用户模块")
class Test_User():

    @allure.story("用户列表")
    def test_1(self, merchant_login_fix):
        '''用户列表'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        result = DM.user_list()
        assert result["message"]["content"] == "查询成功"

    @allure.story("新增用户")
    def test_2(self,merchant_login_fix):
        '''新增用户'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        name = sj.name()
        idcard = sj.sf()
        mobile = sj.phone()
        #上传用户信息返回批次号
        response = DM.add_user(name, idcard, mobile)
        batchNo = response["data"]["batchNo"]
        #通过批次号注册用户信息
        result = DM.user_batchRegister(batchNo)
        assert result["message"]["content"] == "正在注册..."

    @allure.story("批量新增用户")
    def test_3(self,merchant_login_fix):
        '''批量新增用户'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        #批量新增用户
        response = DM.user_import()
        batchNo = response["data"]["batchNo"]
        # 通过批次号注册用户信息
        result = DM.user_batchRegister(batchNo)
        assert result["message"]["content"] == "正在注册..."



