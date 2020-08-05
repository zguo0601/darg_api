from  practice import a1 as a


def setA(ip):
    a.ip = ip
    return a.ip

if __name__ == '__main__':
    ip = '192.168.1.100:5000'
    a1ip = setA(ip)
    print(a1ip)






