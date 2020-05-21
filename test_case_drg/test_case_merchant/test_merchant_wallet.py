import allure
from common.common_func_merchant import Drg_merchant

@allure.feature("达人馆商户商户端资金模块")
class Test_wallet():

    @allure.story("资金账户")
    def test_1(self,merchant_login_fix):
        '''资金账户'''
        ms = merchant_login_fix
        DM = Drg_merchant(ms)
        result = DM.wallet_selectOne()
        assert result["data"]["name"] == "极限传媒"