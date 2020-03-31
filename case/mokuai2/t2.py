import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)





class new():

    def __init__(self,s):
        self.s = requests.session()

    def get_LoginSmsCode(self):

        url = "https://spman.shb02.net/common/reset/getLoginSmsCode"
        data = {
            "loginPort":"OPERATION",
            "principal":"spman_admin",
        }
        r = self.s.post(url=url,data=data)
        return r


    def login(self):

        url = "https://spman.shb02.net/login"

        data = {
            "port_key": "OPERATION",
            "captcha_type": "LOGIN_CAPTCHA",
            "username": "spman_admin",
            "password": "111111",
            "mobile_key": 200331,
        }
        result = self.s.get(url=url,params=data,allow_redirects=False,verify=False)
        return result

    def get_merchant_list(self):
        url_merchant_list = 'https://spman.shb02.net/login/operation/merchant/list'
        data = {
            "currentPage": "1",
            "pageSize": "20"
        }
        merchant_list = self.s.post(url=url_merchant_list, data=data)
        return merchant_list.json()

if __name__ == '__main__':
    s = requests.session()
    n = new(s)
    n.get_LoginSmsCode()
    n.login()
    print(n.get_merchant_list())

