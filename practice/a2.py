import time
from PIL import Image
import pytesseract
from selenium import webdriver


# url='https://spman.shb02.net/admin/login'
# driver = webdriver.Chrome()
# driver.maximize_window()  #将浏览器最大化
# driver.get(url)
# driver.find_element_by_id("login_name").send_keys("spman_admin")
# driver.find_element_by_id("password").send_keys("111111")
# driver.find_element_by_id("mobile_btn").click()
# driver.find_element_by_id("vercode").send_keys("200426")
# driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div/form/div[6]").click()
# time.sleep(3)
# driver.find_element_by_xpath('//*[@id="menu"]/li[9]/div/span').click()
# time.sleep(2)
# driver.find_element_by_xpath('//*[@id="menu"]/li[9]/ul/li[2]').click()
# driver.find_element_by_xpath('//*[@id="app"]/section/div[2]/section/div[1]/table/tr[2]/td[2]/button/span').click()

# driver.save_screenshot('f://aa.png')  #截取当前网页，该网页有我们需要的验证码
# imgelement = driver.find_element_by_xpath('//*[@id="phone_img"]')  #定位验证码
# location = imgelement.location  #获取验证码x,y轴坐标
# print(location)
# size=imgelement.size  #获取验证码的长宽 321*285
# #验证码图片坐标
# rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height']))
# print(rangle)
# #写成我们需要截取的位置坐标
# i=Image.open("f://aa.png") #打开截图
# frame4=i.crop(1000,361,1097,721)  #使用Image的crop函数，从截图中再次截取我们需要的区域
# frame4.save('f://frame4.jpg')
qq=Image.open('f://bb.jpg')
print(type(qq))
# L = qq.convert('1')
# L.show()
# Img = qq.convert('RGB')
# Img.show()
# text=pytesseract.image_to_string(L).strip() #使用image_to_string识别验证码
# text1=pytesseract.image_to_string(Img).strip() #使用image_to_string识别验证码
# print(text)
# print(text1)




