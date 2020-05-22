import allure
from common.common_func_operation import DRG_func


@allure.feature("达人馆账户管理模块")
class Test_invoice():

    @allure.story("员工管理-员工列表页面")
    #@pytest.mark.skip
    def test_1(self,login_fix):
        '''员工管理-员工列表页面'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.staff_management()
        assert result["data"]["dataList"][3]["userName"] == "刘主任"

    @allure.story("员工管理-员工角色页面")
    def test_2(self, login_fix):
        '''员工管理-员工角色页面'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.the_role()
        assert result["data"]["dataList"][0]["roleName"] == "固定角色"

    @allure.story("员工管理-员工角色页面-新增角色")
    def test_3(self,login_fix):
        '''员工管理-员工角色页面-新增角色'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.add_role()
        assert result["message"]["content"] == "操作成功"

    @allure.story("员工管理-员工角色页面-删除员工")
    def test_4(self,login_fix):
        '''员工管理-员工角色页面-删除员工'''
        s = login_fix
        DF = DRG_func(s)
        result_id = DF.add_account()#新增用户，返回用户id
        id = result_id["data"]["id"]
        result = DF.delete_account(id)#删除用户
        assert result["message"]["content"] == "操作成功"

    @allure.story("员工修改密码")
    def test_5(self,login_fix):
        '''员工修改密码'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.modify_pwd()
        assert result["message"]["content"] == "操作成功"

    @allure.story("编辑员工信息")
    def test_6(self,login_fix):
        '''编辑员工信息'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.modify_account()
        assert result["message"]["content"] == "成功"






