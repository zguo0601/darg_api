import time
import allure
import pytest
from common.common_func_operation import DRG_func
from common.common_func_merchant import Drg_merchant
from common.common_func_SJ import  SF


@allure.feature("达人馆财务管理模块")
class Test_invoice():

    @allure.story("销项发票管理查询")
    def test_1(self,login_fix):
        '''销项发票管理查询'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.invoice_list()
        assert result["data"]["resultList"]["pageSize"] == 20

    @allure.story("发票申请详情")
    def test_2(self,login_fix):
        '''发票申请详情'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.invoice_detail()
        assert result["data"]["resultList"]["dataList"][0]["batchNumber"] == "BATCH00000947"

    @allure.story("已开发票")
    def test_3(self, login_fix):
        '''已开发票'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.invoice_info_list()
        assert result["data"]["resultList"]["dataList"][0]["invoiceTypeStr"] == "增值税专用发票"

    @allure.story("已开发票详情")
    def test_4(self, login_fix):
        '''已开发票详情'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.invoice_info_detail()
        assert result["data"]["batchNumber"] == "BATCH00001517"

    @allure.story("确认待审核发票")
    @pytest.mark.drg_affirm_invoice
    #@pytest.mark.skip
    def test_5(self,login_fix,merchant_login_fix):
        '''开票申请'''
        s = login_fix
        ms = merchant_login_fix
        sj = SF()
        DF = DRG_func(s)
        DM = Drg_merchant(ms)
        #运营端开票时间
        invoiceDate = time.strftime("%Y" + "-" + "%m" + "-" + "%d" + " " + "%H" + ":" + "%M" + ":" + "%S")
        #发票代码
        invoiceCode = sj.phone()
        #发票号码
        invoiceNumber = sj.phone()
        #快递单号
        emsOrderNumber = sj.phone()
        #商户端充值通道单号（随机生成）
        channelOrderNumber = sj.channelOrderNumber()
        #商户端充值金额
        recharge_amount = sj.day()
        #---------运营端确认充值订单，查询放款单号-------------------------------------------------
        sysnumber1 = DF.wait_order()
        sysnumber = sysnumber1["data"]["resultList"]["dataList"][0]["systemOrderNumber"]
        # ----------商户端，查询出开票充值记录里面的充值金额和系统单号---------------------------------
        recharge_detail = DM.rechargeOrder_wait()
        m_totalAmount = recharge_detail["data"]["resultList"]["dataList"][0]["amountStr"]
        s_totalAmount = recharge_detail["data"]["resultList"]["dataList"][0]["amountStr"]#格式化输出，将字典里面的值参数化
        systemOrderNumbers = recharge_detail["data"]["resultList"]["dataList"][0]["systemOrderNumber"]
        #-------查询是否有待处理开票订单-------------------------------------------------------------------------------------
        applyStatus = 'WAIT'
        apply = DF.invoice_apply_list(applyStatus)
        apply_result = apply["data"]["count"]
        if apply_result == 0:
            #新增开票申请
            # ------查询是否有开票充值记录-----
            r = DM.rechargeOrder_wait()
            rechargeCount = r["data"]["rechargeCount"]
            # 判断充值记录为0的情况下
            if rechargeCount == 0:
                # 新增充值记录
                DM.merchant_recharge(recharge_amount, channelOrderNumber)
                # 运营端确认
                DF.sucess_order(invoiceDate, sysnumber)
                # 商户端提交开票申请
                DM.invoice_apply(m_totalAmount, systemOrderNumbers, s_totalAmount)
                # 运营端新增开票信息
                # --------运营端查询，返回税价合计金额、批次号、用户编号、根据税价合计计算出 金额和 税额-----------
                applyStatus = 'WAIT'
                r2 = DF.invoice_apply_list(applyStatus)
                totalAmount1 = r2["data"]["resultList"]["dataList"][0]["totalAmount"]  # 获取税价合计金额，类型为 str
                batchNumber = r2["data"]["resultList"]["dataList"][0]["batchNumber"]  # 获取批次号
                merchantNumber = r2["data"]["resultList"]["dataList"][0]["merchantNumber"]  # 获取用户编号
                f_totalAmount = float(totalAmount1)  # 类型为str的金额转化为 浮点型
                y_totalAmount = round(f_totalAmount, 2)  # 浮点型 税价合计金额 四舍五入
                f_amount = y_totalAmount / (1 + 0.1)  # 税率10%
                amount = round(f_amount, 2)  # 金额
                f_taxAmount = y_totalAmount - amount
                taxAmount = round(f_taxAmount, 2)  # 税额
                # 申请合并开票
                r3 = DF.invoice_merger(batchNumber, merchantNumber)
                # 查询开票中订单
                applyStatus = 'HANDLE'
                r4 = DF.invoice_apply_list(applyStatus)
                # 返回合并开票批次号 invoiceBatchNumber
                invoiceBatchNumber = r4["data"]["resultList"]["dataList"][0]["invoiceBatchNumber"]
                DF.invoice_add(invoiceCode, invoiceDate, invoiceNumber, taxAmount, y_totalAmount, amount,invoiceBatchNumber, merchantNumber)
                # 填写快递单号，确认开票申请
                result = DF.invoice_addEmsInfo(batchNumber, merchantNumber, invoiceBatchNumber, emsOrderNumber)
                assert result["message"]["content"] == "操作成功"
            else:
                # 商户端提交开票申请
                DM.invoice_apply(m_totalAmount, systemOrderNumbers, s_totalAmount)
                # 运营端新增开票信息
                # --------运营端查询，返回税价合计金额、批次号、用户编号、根据税价合计计算出 金额和 税额-----------
                applyStatus = 'WAIT'
                r2 = DF.invoice_apply_list(applyStatus)
                totalAmount1 = r2["data"]["resultList"]["dataList"][0]["totalAmount"]  # 获取税价合计金额，类型为 str
                batchNumber = r2["data"]["resultList"]["dataList"][0]["batchNumber"]  # 获取批次号
                merchantNumber = r2["data"]["resultList"]["dataList"][0]["merchantNumber"]  # 获取用户编号
                f_totalAmount = float(totalAmount1)  # 类型为str的金额转化为 浮点型
                y_totalAmount = round(f_totalAmount, 2)  # 浮点型 税价合计金额 四舍五入
                f_amount = y_totalAmount / (1 + 0.1)  # 税率10%
                amount = round(f_amount, 2)  # 金额
                f_taxAmount = y_totalAmount - amount
                taxAmount = round(f_taxAmount, 2)  # 税额
                # 申请合并开票
                r3 = DF.invoice_merger(batchNumber, merchantNumber)
                # 查询开票中订单
                applyStatus = 'HANDLE'
                r4 = DF.invoice_apply_list(applyStatus)
                # 返回合并开票批次号 invoiceBatchNumber
                invoiceBatchNumber = r4["data"]["resultList"]["dataList"][0]["invoiceBatchNumber"]
                DF.invoice_add(invoiceCode, invoiceDate, invoiceNumber, taxAmount, y_totalAmount, amount,invoiceBatchNumber, merchantNumber)
                # 填写快递单号，确认开票申请
                result = DF.invoice_addEmsInfo(batchNumber, merchantNumber, invoiceBatchNumber, emsOrderNumber)
                assert result["message"]["content"] == "操作成功"
        else:
            # 运营端新增开票信息
            # --------运营端查询，返回税价合计金额、批次号、用户编号、根据税价合计计算出 金额和 税额-----------
            applyStatus = 'WAIT'
            r2 = DF.invoice_apply_list(applyStatus)
            totalAmount1 = r2["data"]["resultList"]["dataList"][0]["totalAmount"]  # 获取税价合计金额，类型为 str
            batchNumber = r2["data"]["resultList"]["dataList"][0]["batchNumber"]  # 获取批次号
            merchantNumber = r2["data"]["resultList"]["dataList"][0]["merchantNumber"]  # 获取用户编号
            f_totalAmount = float(totalAmount1)  # 类型为str的金额转化为 浮点型
            y_totalAmount = round(f_totalAmount, 2)  # 浮点型 税价合计金额 四舍五入
            f_amount = y_totalAmount / (1 + 0.1)  # 税率10%
            amount = round(f_amount, 2)  # 金额
            f_taxAmount = y_totalAmount - amount
            taxAmount = round(f_taxAmount, 2)  # 税额
            # 申请合并开票
            r3 = DF.invoice_merger(batchNumber, merchantNumber)
            # 查询开票中订单
            applyStatus = 'HANDLE'
            r4 = DF.invoice_apply_list(applyStatus)
            # 返回合并开票批次号 invoiceBatchNumber
            invoiceBatchNumber = r4["data"]["resultList"]["dataList"][0]["invoiceBatchNumber"]
            DF.invoice_add(invoiceCode, invoiceDate, invoiceNumber, taxAmount, y_totalAmount, amount, invoiceBatchNumber,merchantNumber)
            # 填写快递单号，确认开票申请
            result = DF.invoice_addEmsInfo(batchNumber, merchantNumber, invoiceBatchNumber, emsOrderNumber)
            assert result["message"]["content"] == "操作成功"

    @allure.story("驳回开票申请")
    def test_6(self,login_fix,merchant_login_fix):
        '''驳回开票申请'''
        s = login_fix
        ms = merchant_login_fix
        sj = SF()
        DF = DRG_func(s)
        DM = Drg_merchant(ms)
        #--------------充值订单确认时间-------------------------------------------------------
        invoiceDate = time.strftime("%Y" + "-" + "%m" + "-" + "%d" + " " + "%H" + ":" + "%M" + ":" + "%S")
        # ---------运营端确认充值订单，查询放款单号-------------------------------------------------
        sysnumber1 = DF.wait_order()
        sysnumber = sysnumber1["data"]["resultList"]["dataList"][0]["systemOrderNumber"]
        # 商户端充值通道单号（随机生成）
        channelOrderNumber = sj.channelOrderNumber()
        # 商户端充值金额
        recharge_amount = sj.day()
        #------查询是否有待处理开票订单----------------
        applyStatus = 'WAIT'
        apply = DF.invoice_apply_list(applyStatus)
        apply_result = apply["data"]["count"]
        if apply_result == 0:
            # 新增开票申请
            # ------查询是否有开票充值记录-----
            r = DM.rechargeOrder_wait()
            rechargeCount = r["data"]["rechargeCount"]
            # 判断充值记录为0的情况下
            if rechargeCount == 0:
                # 新增充值记录
                DM.merchant_recharge(recharge_amount, channelOrderNumber)
                # 运营端确认
                DF.sucess_order(invoiceDate, sysnumber)
                # ----------商户端，查询出开票充值记录里面的充值金额和系统单号
                recharge_detail = DM.rechargeOrder_wait()
                m_totalAmount = recharge_detail["data"]["resultList"]["dataList"][0]["amountStr"]
                s_totalAmount = recharge_detail["data"]["resultList"]["dataList"][0]["amountStr"]  # 格式化输出，将字典里面的值参数化
                systemOrderNumbers = recharge_detail["data"]["resultList"]["dataList"][0]["systemOrderNumber"]
                # 商户端提交开票申请
                DM.invoice_apply(m_totalAmount, systemOrderNumbers, s_totalAmount)
                # --------查询待处理订单，返回批次号和用户编号---------------
                applyStatus = 'WAIT'
                result = DF.invoice_apply_list(applyStatus)
                merchantNumber = result["data"]["resultList"]["dataList"][0]["merchantNumber"]
                batchNumber = result["data"]["resultList"]["dataList"][0]["batchNumber"]
                # 驳回开票申请
                respnose = DF.unpass_invoice(batchNumber, merchantNumber)
                assert respnose["message"]["content"] == "操作成功"

            else:
                # ----------商户端，查询出开票充值记录里面的充值金额和系统单号
                recharge_detail = DM.rechargeOrder_wait()
                m_totalAmount = recharge_detail["data"]["resultList"]["dataList"][0]["amountStr"]
                s_totalAmount = recharge_detail["data"]["resultList"]["dataList"][0]["amountStr"]  # 格式化输出，将字典里面的值参数化
                systemOrderNumbers = recharge_detail["data"]["resultList"]["dataList"][0]["systemOrderNumber"]
                # 商户端提交开票申请
                DM.invoice_apply(m_totalAmount, systemOrderNumbers, s_totalAmount)
                # --------查询待处理订单，返回批次号和用户编号---------------
                applyStatus = 'WAIT'
                result = DF.invoice_apply_list(applyStatus)
                merchantNumber = result["data"]["resultList"]["dataList"][0]["merchantNumber"]
                batchNumber = result["data"]["resultList"]["dataList"][0]["batchNumber"]
                # 驳回开票申请
                respnose = DF.unpass_invoice(batchNumber, merchantNumber)
                assert respnose["message"]["content"] == "操作成功"

        else:
            # --------查询待处理订单，返回批次号和用户编号---------------
            applyStatus = 'WAIT'
            result = DF.invoice_apply_list(applyStatus)
            merchantNumber = result["data"]["resultList"]["dataList"][0]["merchantNumber"]
            batchNumber = result["data"]["resultList"]["dataList"][0]["batchNumber"]
            # 驳回开票申请
            respnose = DF.unpass_invoice(batchNumber,merchantNumber)
            assert respnose["message"]["content"] == "操作成功"

    @allure.story("发包方钱包查询")
    def test_7(self,login_fix):
        '''发包方钱包查询'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.merchantWallet_list()
        assert result["data"]["pageSize"] == 20

    @allure.story("发包方钱包详情")
    def test_8(self, login_fix):
        '''发包方钱包详情'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.merchantWallet_selectOne()
        assert result["data"]["name"] == "极限传媒"

    @allure.story("承揽方钱包")
    def test_9(self, login_fix):
        '''承揽方钱包'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.userWallet_list()
        assert result["data"]["total"] > 0

    @allure.story("承揽方钱包详情")
    def test_10(self, login_fix):
        '''承揽方钱包详情'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.userWallet_selectOne()
        assert result["data"]["name"] == "郑国"

    @allure.story("平台钱包")
    def test_11(self, login_fix):
        '''平台钱包'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.systemWallet_selectOne()
        assert result["data"]["name"] == "综合服务费钱包-系统"

    @allure.story("通道钱包")
    def test_12(self, login_fix):
        '''通道钱包'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.channelWallet_list()
        assert result["data"]["dataList"][0]["name"] == "第三方-日常测试"

    @allure.story("通道钱包详情")
    def test_13(self, login_fix):
        '''通道钱包详情'''
        s = login_fix
        DF = DRG_func(s)
        result = DF.channelWallet_selectOne()
        assert result["data"]["name"] == "民生银行-银企直联"



if __name__ == '__main__':
    pytest.main(["-s", "test_invoice.py"])