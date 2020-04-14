import time
import pytest
import allure
from common.common_func import DRG_func
from common.SJ import SF


@allure.feature("达人馆用户管理模块")
class Test_drgapi_user():

    # @classmethod
    # def setup_class(cls):
    #     #前置条件，打开浏览器
    #     cls.s = requests.session()
    #     # 操作步骤：1.实例化DRG_func(s)
    #     cls.DF = DRG_func(cls.s)
    #     code = time.strftime("%Y%m%d%H%M%S")
    #     smscode = code[2:8]
    #     # 2.获取验证码+获取登录成功
    #     cls.DF.login_sucess(smscode)
    #
    # @classmethod
    # def teardown_class(cls):
    #     cls.s = requests.session()
    #     cls.s.close()

    @allure.story("获取承揽方信息")
    # 标记测试用例，加个标签
    @pytest.mark.drg_api_login
    def test_1(self,login_fix):
        '''获取承揽方信息'''
        s = login_fix
        DF = DRG_func(s)
        u_list = DF.get_user_list()
        #3.断言
        assert u_list["data"]["pageSize"] == 20

    @allure.story("获取发包方信息")
    def test_2(self,login_fix):
        '''获取发包方信息'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.get_merchant_list()
        assert result["message"]["content"] == "查询成功"

    @allure.story("发包方详情")
    def test_3(self,login_fix):
        '''发包方详情'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.merchant_detail()
        assert result["message"]["content"] == "查询成功"

    @allure.story("新增发包方")
    def test_4(self,login_fix):
        '''新增发包方'''
        s = login_fix
        sj = SF()
        shorrtname = sj.name()
        accountName = sj.name()
        contactMail = sj.get_email()
        contactName = sj.name()
        managerMobile = sj.phone()
        licenceSerialNumber = time.strftime("%Y%m%d%H%M%S")
        DF = DRG_func(s)
        result = DF.add_merchant(shorrtname,accountName,contactMail,contactName,managerMobile,licenceSerialNumber)
        assert result["message"]["content"] == "新增成功"

    @allure.story("归属用户信息")
    def test_5(self,login_fix):
        '''归属用户信息'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.user_Merchant()
        assert result["message"]["content"] == "查询成功"

    @allure.story("承揽方详情")
    def test_6(self,login_fix):
        '''承揽方详情'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.get_user_detail()
        assert result["message"]["content"] == "查询成功"

    @allure.story("子公司列表")
    def test_7(self,login_fix):
        '''子公司列表'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.sub_list()
        assert result["message"]["content"] == "查询成功"


    @allure.story("新增子公司")
    def test_8(self,login_fix):
        '''新增子公司'''
        #获取子公司列表，判断，如果有子公司的话，获取子公司id，删除之后再新增。
        # 没有的话新增子公司
        s = login_fix
        DF = DRG_func(s)
        sl = DF.sub_list()
        d_l = sl["data"]["total"]
        if d_l == 0:
            result = DF.add_sub()
            assert result["message"]["content"] == "新增成功"
        else:
            mid = sl["data"]["dataList"][0]["merchantRelationId"]
            DF.del_sub(mid,)
            result = DF.add_sub()
            assert result["message"]["content"] == "新增成功"


if __name__ == '__main__':
    # 使用python的方式去执行此命令，结果是与在终端中使用脚本执行的效果是一样的
    pytest.main(["-s","test_info_1.py","-m","drg_api_login"])

