import requests

def getHTMLTEXT(s,url):
    try:
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.66 Safari/537.36"}
        response = s.get(url,headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    except:
        print("产生异常")


if __name__ == '__main__':
    s = requests.session()
    url = " http://b.zqsign.com/#/"
    response = getHTMLTEXT(s,url)
    path = 'F:\\qqq.jpg'
    with open(path,'wb') as f:
        f.write(response.content)
        f.close()


