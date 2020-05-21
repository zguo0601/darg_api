#coding = uft-8
# a = 0
# while a <= 2 :#循环输入9次
#     a += 1
#     for i in range ( 1,11):#输出数据1-9
#         with open("F:/1.txt","a",encoding='utf-8') as f:
#             f.write(str(i))


# with open("F:/1.txt","r",encoding='utf-8') as f:
#     str = f.read()
#     print(str)

# import  random
# random1=["霞","艾希","圣枪游侠","VN","凯特琳"]
# random1_num = len(random1)
# random2=["原计划皮肤","星之守护者皮肤","原图皮肤","限定皮肤"]
# random2_num = len(random2)
# random_int = 0
# while random_int < 10:
#     #random_nub = random.sample(range(1,10), 1)
#     renwu = random.sample(range(0,random1_num), 1)
#     renwu1 = renwu[0]
#     pifu = random.sample(range(0,random2_num), 1)
#     pifu1 = pifu[0]
#     a=("英雄"+str(renwu[0]+1)+":"+str(random1[renwu1])+",皮肤"+str(pifu[0]+1)+":"+str(random2[pifu1]))
#     print(a)
#     random_int += 1

from selenium import webdriver
from selenium.webdriver import ActionChains

driver = webdriver.Chrome()
url = "https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable"
driver.get(url)
driver.maximize_window()
driver.implicitly_wait(2)
# 切换到元素所在的frame
driver.switch_to.frame("iframeResult")
# 起点
start = driver.find_element_by_id("draggable")
# 终点
end = driver.find_element_by_id("droppable")


#ActionChains(driver).click_and_hold(start).perform()
#拖拽元素到指定的坐标位置，start是定位到的元素，x是元素要横向位移的像素，y是元素要纵向位移的像素
ActionChains(driver).drag_and_drop_by_offset(start, 200, 0).perform()

# actions = ActionChains(driver)
# actions.drag_and_drop(start, end)
# actions.perform()

