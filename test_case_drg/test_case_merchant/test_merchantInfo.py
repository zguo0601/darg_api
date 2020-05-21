import allure
from common.common_func_merchant import Drg_merchant


@allure.feature("达人馆商户端账户模块")
class Test_invoice_apply():

    @allure.story("商户信息")
    def test_1(self,merchant_login_fix):
        '''商户信息'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        result = DM.account_merchantInfo()
        assert result["message"]["content"] == "获取商户用户信息成功"
