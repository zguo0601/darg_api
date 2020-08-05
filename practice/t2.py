
from practice import a1
from practice import a2


def get(ip):
    return a1.ipurl(ip)



if __name__ == '__main__':
    ip = '192.168.1.100:5000'
    a1ip = a2.setA(ip)
    print(get(a1ip))
