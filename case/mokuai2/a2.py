from appium import webdriver
import time


def start():
    desired_caps={
        'platformName':'Android',
        'deviceName':"emulator-5554",
        'platformVersion': "5.1.1",
        'appPackage':'tv.danmaku.bili',
        'appActivity':'.ui.splash.SplashActivity',
        'noReset':'true',
        'unicodeKeyboard': True,  # 此两行是为了解决字符输入不正确的问题
        'resetKeyboard': True,  # 运行完成后重置软键盘的状态
        'newCommandTimeout':600
     }

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return driver

def test():
    driver = start()

    driver.find_element_by_id("tv.danmaku.bili:id/expand_search").click()
    time.sleep(5)
    driver.find_element_by_id("tv.danmaku.bili:id/search_src_text").send_keys("appium")





if __name__ == '__main__':
    test()