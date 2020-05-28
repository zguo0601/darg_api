import allure
from common.common_func_operation import DRG_func

@allure.feature("达人馆平台付款管理模块")
class Test_drg_apply():

    @allure.story("上传完税证明")
    def test_1(self,login_fix):
        '''上传完税证明'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.update_apply()
        assert result["message"]["content"] == "上传成功"

    @allure.story("重传结算单")
    def test_2(self,login_fix):
        '''重传结算单'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.upload_Attachment()
        assert result["message"]["content"] == "上传成功"

    @allure.story("付款记录")
    def test_3(self,login_fix):
        '''付款记录'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.issu_list()
        assert result["message"]["content"] == "查询成功"

    @allure.story("放款详情")
    def test_4(self,login_fix):
        '''放款详情'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.issu_detail()
        assert result["data"]["systemOrderNumber"] == "20200410114901016767001236"

    @allure.story("批量放款记录")
    def test_5(self,login_fix):
        '''批量放款记录'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.issuBatchApply_detail()
        assert result["data"]["total"] > 0

    @allure.story("批次放款记录")
    def test_6(self, login_fix):
        '''批量放款记录'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.batch_issu_detail()
        assert result["data"]["dataList"][0]["batchNumber"] == "BATCH00001080"



if __name__ == '__main__':
    pass




