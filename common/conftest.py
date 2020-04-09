import os
import requests
import pytest
from case.common_func import DRG_func
from common.connect_mysql import excute_sql, select_sql
import time

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
    '''
    设置的环境变量是：http://120.79.243.237:10021
    配置默认环境变量：https://spman.shb02.net/login，
    命令获取默认参数，赋值给环境变量，打印出来的是默认配置的环境'''
    os.environ["yy_host"] = request.config.getoption("--cmdhost")
    print("当前用例运行环境:%s"%os.environ["yy_host"])



'''
fixture的作用范围:
fixture里面有个scope参数可以控制fixture的作用范围：session>module>class>function
function：每一个函数或方法都会调用
class：每一个类调用一次，一个类中可以有多个方法
module：每一个.py文件调用一次，该文件内又有多个function和class
session：是多个文件调用一次，可以跨.py文件调用，每个.py文件就是module。
'''
@pytest.fixture(scope="class")
def login_fix(request):
    #相当于打开浏览器
    session = requests.session()
    code = time.strftime("%Y%m%d%H%M%S")
    smscode = code[2:8]
    print("登录成功")
    DF = DRG_func(session)
    DF.login_sucess(smscode)
    #这里yield s返回的是最新的cookie
    yield session
    #关闭session
    def close_s():
        session.close()
    request.addfinalizer(close_s)#终结'''自定义一个前置操作'''
    print("关闭请求")

@pytest.fixture(scope="class")
def lg():
    print("开始请求")
    s = requests.session()
    print("打开首页")
    url_merchant_list = "https://spman.shb02.net/admin/login"
    s.get(url=url_merchant_list)
    print("获取验证码")
    url = "https://spman.shb02.net/common/reset/getLoginSmsCode"
    data = {
        "loginPort": "OPERATION",
        "principal": "spman_admin",
    }
    res = s.post(url, data)
    print("登录成功")
    code = time.strftime("%Y%m%d%H%M%S")
    smscode = code[2:8]
    url_login = "https://spman.shb02.net/login"
    data = {
        "port_key": "OPERATION",
        "captcha_type": "LOGIN_CAPTCHA",
        "username": "spman_admin",
        "password": "111111",
        "mobile_key": smscode,
    }
    # verify=False（不做安全验证报错SSLerror时候）allow_redirects=False（禁止页面重定向，不禁用的话有可能会获取不到cookies）
    r = s.post(url_login, data, verify=False, allow_redirects=False)
    return s



@pytest.fixture(scope="function")
def unlogin_fix():
    '''自定义一个前置操作'''
    print("不登录操作")
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

@pytest.fixture()
def update_spman_center_task():
    #1任务开启，0任务关闭
    up_sql = 'UPDATE spman_center.task set STATUS=0 WHERE  id = "137";'
    sql1 = 'SELECT * FROM spman_center.task where id = "137";'
    select_sql(sql1)
    excute_sql(up_sql)
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
    r = login_fix()
    print(r)