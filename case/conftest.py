import os
import requests
import pytest
from case.common_func import DRG_func
from common.connect_mysql import excute_sql


'''默认级别为scope="function"，只针对函数，每个用例都要调用一次。
 module针对的是模块，每个.py文件都会调用一次。
 class针对类里面需要调用的生效
 package针对的包下面都生效，
 session最高级别,针对整个项目生效
 '''

#配置默认地址
def pytest_addoption(parser):
    parser.addoption(
        "--cmdhost",
        action="store",
        default="https://spman.shb02.net/login",
        help="运营端测试环境地址"
    )
@pytest.fixture(scope="session",autouse=True)
def host(request):
    '''获取命令行参数，给到环境变量'''
    os.environ["yy_host"] = request.config.getoption("--cmdhost")
    print("当前用例运行环境:%s"%os.environ["yy_host"])


@pytest.fixture(scope="session")
def login_fix(request):
    '''自定义一个前置操作'''
    #相当于打开浏览器
    s = requests.session()
    print("登录获取cookie")
    DF = DRG_func(s)
    DF.login()
    #关闭session
    def close_s():
        s.close()
    request.addfinalizer(close_s)#终结
    # 这里s返回的是最新的cookie
    return s


@pytest.fixture(scope="function")
def unlogin_fix():
    '''自定义一个前置操作'''
    print("不登录")
    s = requests.session()
    return s


@pytest.fixture(scope="function")
def delect_task():
    #前置条件，先删除要新增的任务内容，保证用例可以循环执行
    del_sql = 'DELETE  FROM spman_center.task where  title = "哈哈哈哈1";'
    # 测试用例之前执行sql语句
    #excute_sql(del_sql)
    yield
    #测试用例之后执行sql语句
    excute_sql(del_sql)

@pytest.fixture(scope="function")
def delect_spman_center_merchant():
    #前置条件，先删除要新增的任务内容，保证用例可以循环执行
    del_sql = 'DELETE  FROM spman_center.merchant where short_name = "小可爱";'
    # 测试用例之前执行sql语句
    excute_sql(del_sql)
    yield
    #测试用例之后执行sql语句
    #excute_sql(del_sql)
@pytest.fixture(scope="function")
def delect_inside_user_center_user():
    #前置条件，先删除要新增的任务内容，保证用例可以循环执行
    del_sql = 'DELETE from inside_user_center.user where user_name = "小可爱";'
    # 测试用例之前执行sql语句
    excute_sql(del_sql)
    yield





#终端执行标记测试用例时报无法识别标签时添加此命令（单个标签）
# def pytest_configure(config):
#     config.addinivalue_line(
#     "markers", "drg_api_task" # drgapi 是标签名
# )
#终端执行:标记的测试用例时，报警无法识别标签时添加此命令（多个标签）
def pytest_configure(config):
    marker_list = ["drg_api_login","drg_api_task"]  # 标签名集合
    for markers in marker_list:
        config.addinivalue_line(
        "markers", markers
)


if __name__ == '__main__':
        pass