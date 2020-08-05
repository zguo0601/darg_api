from aip import AipOcr
from PIL import Image
import pytesseract




#百度图片识别API接口
""" 你的 APPID AK SK """
APP_ID = '19611635'
API_KEY = '5kn9XvSsF19BPNuTtYeuPghP'
SECRET_KEY = 'oRAxD3tm0ducNoF3dbzaVfBh9EQHiP6W'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)



""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


image = get_file_content('E:\\gzyp_auto\\common\\1.gif')
""" 调用通用文字识别, 图片参数为本地图片 """
text = client.basicGeneral(image)
print(text)


