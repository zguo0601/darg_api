from common.common_func import DRG_func
from common.common_func_merchant import Drg_merchant
import requests
from aip import AipOcr
import datetime
import time









""" 你的 APPID AK SK """
APP_ID = '19611635'
API_KEY = '5kn9XvSsF19BPNuTtYeuPghP'
SECRET_KEY = 'oRAxD3tm0ducNoF3dbzaVfBh9EQHiP6W'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)



s = requests.session()
#DF = DRG_func(s)
DM = Drg_merchant(s)
DM.merchant_login(username='M002137',password='111111')

#获取图片验证码,毫秒级时间戳
t = int(time.time() * 1000)
smscode = 'https://spman.shb02.net/common/jcaptcha/create?%s'%t
respnose = s.get(smscode)

#图片验证码存储路径
path = 'F:\\dx.jpg'
with open(path, 'wb') as f:
    f.write(respnose.content)
    f.close()

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


image = get_file_content('F:\\dx.jpg')
""" 调用通用文字识别, 图片参数为本地图片 """
text = client.basicGeneral(image)
scood = (text["words_result"][0]["words"])
print(scood)
print(type(scood))


#输入图片验证码
sms_url = 'https://spman.shb02.net/system/user/sendSms'
data = {
    "smsType":"MODIFY_PAYMENT_PASSWORD",
    "captchaCode":scood,
    "mobile":"18526999857",
}
r = s.post(sms_url,data)
print(r.json())



url1 = 'https://spman.shb02.net/merchant/account/modifyTradePassword'
data1 = {
    "smsCode":"200428",
    "newTradePasswordd":"111111",
}
r1 = s.post(url1,data1)
print(r1.json())







