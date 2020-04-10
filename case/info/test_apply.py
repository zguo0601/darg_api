import allure
from common.common_func import DRG_func


class Test_drg_apply():

    @allure.story("上传完税证明")
    def test_1(self,login_fix):
        '''上传完税证明'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.update_apply()
        assert result["message"]["content"] == "上传成功"

    @allure.story("付款记录")
    def test_2(self,login_fix):
        '''付款记录'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.issu_list()
        assert result["message"]["content"] == "查询成功"









if __name__ == '__main__':
    pass




