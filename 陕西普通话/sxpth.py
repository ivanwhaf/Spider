import requests
from bs4 import BeautifulSoup as bs
import re


def get_content():
    while True:
        r = requests.get('http://sxpth.cn')
        if(r.status_code == requests.codes.ok):
            r.encoding = 'utf-8'
            return r.text


def get_info(name, id):
    # url='http://sxpth.cn/'+name+'查询结果.htm'
    url = 'http://sxpth-x-cn.img.abc188.com/'+name+'.jpg'
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        with open('f:/project/python/爬虫/sxpth/'+name+'-'+id+'.jpg', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(name+'下载完成')


def main():
    c = get_content()
    soup = bs(c, 'html.parser')
    script = soup.find('script').text
    # print(script)

    pattern = re.compile('\'.+==身份证号')
    r = pattern.findall(script)
    # print(r)
    for p in r:
        p = p.split('\'')
        print(p)
        name = p[1]
        id = p[3]
        get_info(name, id)


main()
