import random
import time

class SF():
    def regiun(self):
        '''生成身份证前六位'''
        #列表里面的都是一些地区的前六位号码
        first_list = ['362402','362421','362422','362423','362424','362425','362426','362427','362428','362429','362430','362432','110100','110101','110102','110103','110104','110105','110106','110107','110108','110109','110111']
        first = random.choice(first_list)
        return first

    def year(self):
        '''生成年份'''
        now = time.strftime('%Y')
        #1948为第一代身份证执行年份,now-18直接过滤掉小于18岁出生的年份
        second = random.randint(1948,int(now)-18)
        age = int(now) - second
        return second


    def month(self):
        '''生成月份'''
        three = random.randint(1,12)
        #月份小于10以下，前面加上0填充
        if three < 10:
            three = '0' + str(three)
            return three
        else:
            return three


    def day(self):
        '''生成日期'''
        four = random.randint(1,31)
        # 日期小于10以下，前面加上0填充
        if four < 10:
            four = '0' + str(four)
            return four
        else:
            return four


    def randoms(self):
        '''生成身份证后四位'''
        # 后面序号低于相应位数，前面加上0填充
        five = random.randint(1,9999)
        if five < 10:
            five = '000' + str(five)
            return five
        elif 10 < five < 100:
            five = '00' + str(five)
            return five
        elif 100 < five < 1000:
            five = '0' + str(five)
            return five
        else:
            return five

    #随机身份证号码
    def idcard(self):
        first = self.regiun()
        second = self.year()
        three = self.month()
        four = self.day()
        last = self.randoms()
        IDcard = str(first)+str(second)+str(three)+str(four)+str(last)
        return IDcard
    #随机姓名
    def name(self):
        xing = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜则同一女子所生子嗣组成的亲族也可以称东周文献中有时是指姓族之名无锡市人民医院副院长陈静瑜'
        ming = '豫章故郡洪都新府星分翼轸地接衡庐襟三江而带五湖当时他的肺已经纤维化不可逆实行肺移植手术对患者和医疗团队都存在风静瑜团队做了非常详细的准备肺炎危重症患者的肺移植手术具有高选择性'
        X = random.choice(xing)#在xing中随机选择一个字符串
        M = ''.join(random.choice(ming) for i in range(2))#
        n = X+M
        return n
    #随机手机号码
    def phone(self):
        headList = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
                    "147", "150", "151", "152", "153", "155", "156", "157", "158", "159",
                    "186", "187", "188", "189"]
        return (random.choice(headList) + "".join(random.choice("0123456789") for i in range(8)))
    #随机银行卡
    def bankcard(self):
        card_id = '62'
        for i in range(17):
            ran = str(random.randint(0, 9))
            card_id += ran
        return card_id
    #随机电子邮箱
    def get_email(self):
        email_suf = random.choice(
            ['@163.com', '@qq.com', '@126.com', '@sina.com', '@sina.cn', '@soho.com', '@yeah.com'])
        phone = self.phone()
        email = phone + email_suf
        return email

    #生成商户新增充值的通道编号
    def channelOrderNumber(self):
        channelOrderNumber = random.randint(1,9999999999999999999)
        return channelOrderNumber

    def task_id(self):
        f_out = open('/data/num.txt', 'r+')
        a = f_out.read()
        a = int(a) + 1
        f_out.seek(0)
        f_out.truncate()
        f_out.write(str(a))
        f_out.close()
        return a




if __name__ == '__main__':
    a = SF()
    id = a.name()
    print(id)