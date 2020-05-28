from common.common_func_SJ import  SF
sj = SF()
import requests


s = requests.session()

def merchant_login(username, password):
    url = "https://spman.shb02.net/login"
    data = {
        "port_key": "MERCHANT",
        "captcha_type": "LOGIN_CAPTCHA",
        "username": username,
        "password": password,
    }
    rsp = s.post(url=url, data=data, verify=False, allow_redirects=False)
    return rsp

username = 'M002137'
password = '111111'
r = merchant_login(username,password)
print(r.headers)
print(r.cookies)

