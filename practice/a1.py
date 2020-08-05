from practice import a2



def ipurl(ip):
    ip = ip
    url = ip + '/s_opt'
    return url

if __name__ == '__main__':
    ip = '192.168.1.100:5000'
    a1ip = a2.setA(ip)
    ipurl = ipurl(a1ip)
    print(ipurl)









