import pytest
import allure


@pytest.fixture()
def demon_fix():
    print("测试之前的操作")
    #这里的hello就是  return hello
    yield "hello"
    print("测试用例结束之后的操作，数据清理")

@allure.step("我的步骤1，测试报告中展示")
def step1():
    print("我的步骤1")
@allure.step("我的步骤2，测试报告中展示")
def step2():
    print("我的步骤2")

@allure.feature("测试模块名称")
class Test_demon_1():

    @allure.story("测试用例1的标题")
    def test_1(self,demon_fix):
        '''用例1的描述，用例1的描述，用例1的描述，用例1的描述，用例1的描述，用例1的描述'''
        step1()
        step2()
        print("我是用例1")
        assert 1==1

    @allure.story("测试用例2的标题")
    def test_2(self):
        print("我是用例2")

    @allure.story("测试用例3的标题")
    def test_3(self):
        print("我是用例3")
