import xlrd

wb = xlrd.open_workbook('dyc.xls')
sheet = wb.sheet_by_name('第一次创建sheet')

l = []
d = {}

#查询表格所有的行数
all_rows = sheet.nrows
#---------------------------------------------------------------------
#查询出第一行的内容,格式为list，[text:'id', text:'name', text:'age']
row_titile = sheet.row(0)
print(row_titile)
#表头的值
print(row_titile[0].value) #id
print(row_titile[1].value) #name
print(row_titile[2].value) #age
#---------------------------------------------------------------------
#[text:'1', text:'zs1', number:18.0]
row1 = sheet.row(1)
print(row1)
#数据信息
print(row1[0].value) #1
print(row1[1].value) #zs1
print(row1[2].value) #18.0
#----------字典的格式储存-----------------------------------------------------------
#[row_titile[0].value] = row1[0].value
#    等于字典的key         等于字典里的值
d[row_titile[0].value] = row1[0].value
d[row_titile[1].value] = row1[1].value
d[row_titile[2].value] = row1[2].value
#------字典数据，添加到列表里面---------------------------------------------------------------
l.append(d)
print(l)


row2 = sheet.row(2)
row3 = sheet.row(3)


list = []
#读取数据部分 sheet.nrows查询出 i=5，for i in range(1,5)
for i in range(1,sheet.nrows):#循环读取第i行之后的数据
    row = sheet.row(i)
    dic = {}
    for j in range(len(row)):
        dic[row_titile[j].value] = row[j].value
    list.append(dic)#字典添加到list

print(list)
