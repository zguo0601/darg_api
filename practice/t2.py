import requests


class Drg_merchant1():

    def __init__(self,s):
        #---类下实例化----
        self.s = s


    def merchant_login(self ,username ,password):
        url = "https://spman.shb02.net/login"
        data = {
            "port_key": "MERCHANT",
            "captcha_type": "LOGIN_CAPTCHA",
            "username": username,
            "password": password,
        }
        rsp = self.s.post(url=url, data=data, verify=False, allow_redirects=False)
        return rsp.text

    def rechargeOrder_wait(self):
        url_rechargeOrder_wait = "https://spman.shb02.net/operation/rechargeOrder/list"
        data = {
            "orderStatus": "SUCCESS",
            "invoiceStatus": "INVOICE_WAIT",
            "currentPage": "1",
            "pageSize": "100",
        }
        rsp = self.s.post(url=url_rechargeOrder_wait, data=data)
        return rsp.json()
if __name__ == '__main__':
    s = requests.session()
    DM = Drg_merchant1(s)
    DM.merchant_login(username="M002137",password="111111")
    r = DM.rechargeOrder_wait()
    print(r)
