import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

s = requests.session()

def login():
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.66 Safari/537.36",
    }

    url = "https://spman.shb02.net/login"

    data = {
        "port_key": "MERCHANT",
        "captcha_type": "LOGIN_CAPTCHA",
        "username": "M002137",
        "password": "111111",
    }
    result = s.post(url=url,
                    data=data,
                    headers=headers,
                    allow_redirects=False,
                    verify=False)
    return result

def mer_list():
    url_mer_list = "https://spman.shb02.net/merchant/user/list"
    data = {
        "currentPage":"1",
        "pageSize":"20",
    }
    r = s.post(url=url_mer_list,data=data)
    return r.json()

login()
print(mer_list())