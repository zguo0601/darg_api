from common.SJ import SF

class LL():


    def ll(self,requesterUserIdentity,idCard,mobile,name):
        data = {
            'content': '[{"industryId":"1","requesterUserIdentity":"%s","idCard":"%s","mobile":"%s","name":%s,"idCardBackFileUrl":"https://darenguan-static-file.oss-cn-shenzhen.aliyuncs.com/drg1587699987268.jpg","idCardFrontFileUrl":"https://darenguan-static-file.oss-cn-shenzhen.aliyuncs.com/drg1587699987268.jpg"}]',
        }

        print(data)

    def tt(self):
        data = {

            'content': '[{"industryId":"1","requesterUserIdentity":"jx7879187","idCard":"350181199906025489","mobile":"18759613658","name":"郭富城3","idCardBackFileUrl":"https://darenguan-static-file.oss-cn-shenzhen.aliyuncs.com/drg1587699987268.jpg","idCardFrontFileUrl":"https://darenguan-static-file.oss-cn-shenzhen.aliyuncs.com/drg1587699987268.jpg"}]',
        }
        print(data)

if __name__ == '__main__':
    a = LL()
    sj = SF()
    requesterUserIdentity = str("jx" + sj.phone())
    idCard = sj.sf()
    mobile = sj.phone()
    name = sj.name()


    a.ll(requesterUserIdentity,idCard,mobile,name)
    a.tt()
