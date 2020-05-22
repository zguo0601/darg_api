import time
from common.common_func_SJ import SF
from common.common_func_merchant_api import API_merchant
import allure



@allure.feature("API商户接口测试用例")
class Test_Api_Merchant():


    @allure.story("api商户新增用户")
    def test_1(self,api_merchant_login,api_get_merchantPriKey,api_get_systemPubKey):
        '''api商户新增用户'''
        s = api_merchant_login
        # 获取商户私钥
        merchantPriKey = api_get_merchantPriKey
        # 获取系统公钥
        systemPubKey = api_get_systemPubKey
        api = API_merchant(s)
        sj = SF()
        requesterUserIdentity = "jx" + sj.phone()
        idCard = sj.idcard()
        mobile = sj.phone()
        name = sj.name()
        # 获取api商户密码
        result1 = api.get_apimerchant_password(merchantPriKey, systemPubKey)
        password = result1["password"]
        # api商户新增用户
        result2 = api.add_api_merchant(merchantPriKey, systemPubKey, password, requesterUserIdentity, idCard, mobile,name)
        assert result2[0]["message"] == "处理中"


    @allure.story("查询用户详情")
    def test_2(self,api_merchant_login,api_get_merchantPriKey,api_get_systemPubKey):
        '''查询用户详情'''
        #前置条件登录
        s = api_merchant_login
        #获取商户私钥
        merchantPriKey = api_get_merchantPriKey
        #获取系统公钥
        systemPubKey = api_get_systemPubKey
        api = API_merchant(s)
        # 获取api商户密码
        result1 = api.get_apimerchant_password(merchantPriKey, systemPubKey)
        password = result1["password"]
        idcard = "110101198902226668"
        result = api.get_status(merchantPriKey,systemPubKey,password,idcard)
        assert result["message"] == "认证成功"

    @allure.story("单笔充值")
    def test_3(self,api_merchant_login,api_get_merchantPriKey,api_get_systemPubKey):
        '''单笔充值'''
        s = api_merchant_login
        merchantPriKey = api_get_merchantPriKey
        systemPubKey = api_get_systemPubKey
        api = API_merchant(s)
        result1 = api.get_apimerchant_password(merchantPriKey, systemPubKey)
        password = result1["password"]
        # 充值,金额100等于1块
        amount = "100"
        # 请求单号
        r_n = time.strftime("%Y%m%d%H%M%S")
        requesterOrderNumber = 'jxcz' + r_n
        result2 = api.recharge_single(merchantPriKey,systemPubKey,password,amount,requesterOrderNumber)
        assert result2["message"] == "等待确认"








