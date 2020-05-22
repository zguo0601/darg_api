

def aa():
    data = {
        "学校":"清华大学",
        "个人信息":"[{'姓名':'张三','年龄':'18',}]",
    }
    print(data)
    data1 = {
        "学校": "清华大学",
        "个人信息": "[{'姓名':'','年龄':'',}]",
    }
    print(data1)


name = "aa"
age = "18"
r = aa(name,age)
print(r)


