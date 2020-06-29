import xlwt
from common.common_func_SJ import  SF

sj = SF()
wb = xlwt.Workbook()
sheet = wb.add_sheet("批量新增用户")
''':type :xlwt.Worksheet'''

class User_sj():

    #批量新增
    def sj_user(self):
        list = []
        for i in range(0, 5):
            name = sj.name()
            id = sj.idcard()
            phone = sj.phone()
            user = {"name": name, "id": id, "phone": phone}
            list.append(user)

        title_row = 0
        for i in range(len(list)):
            dic = list[i]
            sheet.write(title_row + i, 0, dic['name'])  # 第0列放id的值
            sheet.write(title_row + i, 1, dic['id'])  # 第1列放name的值
            sheet.write(title_row + i, 2, dic['phone'])  # 第2列放age的值

        #wb.save('E:\\pytest_api\\data\\user_info.xls')
        #代码再docker里面运行，保存地址需要填写服务器上的地址，本地调试的时候，可以先注销
        #wb.save('/var/jenkins_home/workspace/darg_api/data/user_info.xls')
        #代码再服务器里用代理面运行，保存地址需要填写服务器上的地址，本地调试的时候，可以先注销
        wb.save('/home/jenkins/test1/workspace/darg_api/data/user_info.xls')


    #jmeter 新增用户（单个新增）参数化方法
    # def sj_single(self):
    #     with open('E:\pytest_api\data\\user_single.txt', 'w', encoding='utf-8') as f:
    #         for i in range(0, 1):
    #             name = sj.name()
    #             id = sj.idcard()
    #             phone = sj.phone()
    #             data1 = f.write(name + ',' + id + ',' + phone + '\n')
    #     f = open('E:\pytest_api\data\\user_single.txt', 'r', encoding='utf-8')
    #
    # # jmeter 新增用户（批量新增）参数化方法
    # def sj_batch(self):
    #     with open('E:\pytest_api\data\\user_batch.txt', 'w', encoding='utf-8') as f:
    #         for i in range(0, 500):
    #             name = sj.name()
    #             id = sj.idcard()
    #             phone = sj.phone()
    #             data1 = f.write(name + ',' + id + ',' + phone + '\n')
    #     f = open('E:\pytest_api\data\\user_batch.txt', 'r', encoding='utf-8')



if __name__ == '__main__':
    a = User_sj()
    a.sj_single()



#sheet.write(3,4,'你好')  #从0开始 在4行5列写入 你好

# list = [
#     {"id":"1","name":"zs1","age":18,},
#     {"id":"2","name":"zs2","age":19,},
#     {"id":"3","name":"zs3","age":20,},
#     {"id":"4","name":"zs4","age":21,},
# ]



# #先处理表头，计算所长度，循环输出
# titles = ["id","name","age"]
# for i in range(len(titles)):
#     sheet.write(0,i,titles[i])

#title占了一行，数据从第二行开始写入
# title_row = 1
# for i in range(len(list)):
#     dic = list[i]
#     sheet.write(title_row+i,0,dic['id'])#第0列放id的值
#     sheet.write(title_row+i,1,dic['name'])#第1列放name的值
#     sheet.write(title_row+i,2,dic['age'])#第2列放age的值



