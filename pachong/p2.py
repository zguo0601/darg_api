from bs4 import BeautifulSoup
import requests


r = requests.get("https://www.baidu.com")
r.encoding='utf-8'
demon = r.text
#html格式化
soup = BeautifulSoup(demon,"html.parser")
print(soup.prettify())
#获取title内容
t = soup.title
print(t)
#获取a标签内容
a = soup.a
print(a)
#获取a标签属性
ats = a.attrs
print(ats)
#获取a标签字符串内容
str = a.string
print(str)
#  .contents 和 .children 用于循环遍历儿子节点。.descendants,用于循环遍历，包含所有的子孙节点
a1 = soup.head.contents
print(len(a1))
print(a1)
#.parent节点的父亲标签 ， .parents循环遍历先辈节点
a2 = soup.title.parent
print(a2)
#.next_sibling平行标签遍历后续节点。.previous._sibling遍历前续节点
a4 = soup.a.next_sibling
print(a4)




