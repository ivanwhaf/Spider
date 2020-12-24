import requests
from bs4 import BeautifulSoup as bs
import os
import json

url = "https://nj.zu.anjuke.com/fangyuan"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
cookies = {'cookies': 'aQQ_ajkguid=263FB199-16A7-57BB-DA8B-E3643EFA96B1; lps=http%3A%2F%2Fwww.anjuke.com%2F%3Fpi%3DPZ-baidu-pc-all-biaoti%7Chttps%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3Dutf-8%26f%3D8%26rsv_bp%3D0%26rsv_idx%3D1%26tn%3Dbaidu%26wd%3D%25E5%25AE%2589%25E5%25B1%2585%25E5%25AE%25A2%26rsv_pq%3Da650a8660000086f%26rsv_t%3D0d30qH78ph38IB0ymmasOxoDhG1jE80iHblUAP%252BNPtjGHFsbfu8VeYwCUsM%26rqlang%3Dcn%26rsv_enter%3D1%26rsv_sug3%3D6%26rsv_sug1%3D5%26rsv_sug7%3D100; twe=2; sessid=F4EC0FE1-00E7-A40A-4E7B-BCC18533C842; _ga=GA1.2.1248194481.1527860349; _gid=GA1.2.1341196458.1527860349; 58tj_uuid=7aa876b5-e627-491c-9734-f527714c0aa6; init_refer=https%253A%252F%252Fwww.baidu.com%252Fs%253Fie%253Dutf-8%2526f%253D8%2526rsv_bp%253D0%2526rsv_idx%253D1%2526tn%253Dbaidu%2526wd%253D%2525E5%2525AE%252589%2525E5%2525B1%252585%2525E5%2525AE%2525A2%2526rsv_pq%253Da650a8660000086f%2526rsv_t%253D0d30qH78ph38IB0ymmasOxoDhG1jE80iHblUAP%25252BNPtjGHFsbfu8VeYwCUsM%2526rqlang%253Dcn%2526rsv_enter%253D1%2526rsv_sug3%253D6%2526rsv_sug1%253D5%2526rsv_sug7%253D100; new_uv=1; als=0; new_session=0; ctid=16; ajk_bfp=1; propertys=j7h1dt-p9neha_; __xsptplusUT_8=1; __xsptplus8=8.3.1527860384.1527862802.26%232%7Cwww.baidu.com%7C%7C%7C%25E5%25AE%2589%25E5%25B1%2585%25E5%25AE%25A2%7C%23%23WiKQKarmQ1TosOYklQc4ItgAhcgD5deM%23'}
cookies2 = {'cookies': 'aQQ_ajkguid=263FB199-16A7-57BB-DA8B-E3643EFA96B1; lps=http%3A%2F%2Fwww.anjuke.com%2F%3Fpi%3DPZ-baidu-pc-all-biaoti%7Chttps%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3Dutf-8%26f%3D8%26rsv_bp%3D0%26rsv_idx%3D1%26tn%3Dbaidu%26wd%3D%25E5%25AE%2589%25E5%25B1%2585%25E5%25AE%25A2%26rsv_pq%3Da650a8660000086f%26rsv_t%3D0d30qH78ph38IB0ymmasOxoDhG1jE80iHblUAP%252BNPtjGHFsbfu8VeYwCUsM%26rqlang%3Dcn%26rsv_enter%3D1%26rsv_sug3%3D6%26rsv_sug1%3D5%26rsv_sug7%3D100; twe=2; sessid=F4EC0FE1-00E7-A40A-4E7B-BCC18533C842; _ga=GA1.2.1248194481.1527860349; _gid=GA1.2.1341196458.1527860349; 58tj_uuid=7aa876b5-e627-491c-9734-f527714c0aa6; als=0; ctid=16; ajk_bfp=1; __xsptplusUT_8=1; init_refer=https%253A%252F%252Fnj.zu.anjuke.com%252Ffangyuan%252Fp2%252F; new_uv=2; propertys=j68ap8-p9ngn3_; __xsptplus8=8.4.1527865588.1527865603.2%232%7Cwww.baidu.com%7C%7C%7C%25E5%25AE%2589%25E5%25B1%2585%25E5%25AE%25A2%7C%23%23me5xdPubmY-r-F9cZvvJ5Sn8ab-msmnG%23; new_session=0'}
count = 1
lis = []
total_count = 100


def download(img_url, name):
    global count
    img = requests.get(img_url, stream=True)
    f = open('安居客/图片/'+name+'.jpg', 'wb')
    for chunk in img.iter_content(chunk_size=1024):
        if chunk:
            try:
                f.write(chunk)
            except:
                continue


def main():
    global lis
    global count
    global total_count
    global url
    page = 1
    if not os.path.exists('安居客'):
        os.makedirs('安居客')
        os.makedirs('安居客/图片')
    while total_count > count:
        r = requests.get(url, headers=headers, cookies=cookies)
        soup = bs(r.text, 'html.parser')
        zfs = soup.find_all('div', class_='zu-itemmod')
        for zf in zfs:
            href = zf.find('a').get('href')
            p = zf.find('p').strings
            l = []
            for s in p:
                l.append(s)
            Floor = l[4]
            r = requests.get(href, headers=headers, cookies=cookies2)
            soup = bs(r.text, 'html.parser')
            title = soup.find('h3').string
            img_count = 1
            imgs = soup.find('div', id='room_pic_wrap').find_all('img')
            for im in imgs:
                img = im.get('data-src')
                try:
                    download(img, str(count)+'('+str(img_count)+')')
                except:
                    print('编号'+str(count)+'('+str(img_count)+')'+'下载失败')
                    continue
                img_count = img_count+1
            infos = soup.find(
                'ul', class_='house-info-zufang cf').find_all('li')
            n = 1
            for info in infos:
                if n == 1:
                    Price = info.find('em').string
                elif n == 2:
                    HouseType = info.find('span', class_='info').string
                elif n == 3:
                    Area = info.find('span', class_='info').string
                elif n == 4:
                    Orientation = info.find('span', class_='info').string
                elif n == 6:
                    Decoration = info.find('span', class_='info').string
                elif n == 7:
                    Type = info.find('span', class_='info').string
                elif n == 8:
                    A = info.find_all('a')
                    i = 1
                    for a in A:
                        if i == 1:
                            Village = a.string
                        elif i == 2:
                            District = a.string
                        elif i == 3:
                            County = a.string
                        i = i+1
                n = n+1
            ps = soup.find('div', class_='auto-general').find_all('p')
            General = ''
            for p in ps:
                ss = p.strings
                for s in ss:
                    General = General+s
            General = ''.join(General.split())
            if General == '':
                General = '无房源概况'

            # print(General+'sssssssssssssssssssssssssss')
            dic = {}
            dic['id'] = str(count)  # 序号
            dic['title'] = title  # 名称
            dic['Price'] = Price  # 价格
            dic['HouseType'] = HouseType  # 户型
            dic['Area'] = Area  # 面积
            dic['Orientation'] = Orientation  # 朝向
            dic['Floor'] = Floor  # 楼层
            dic['Decoration'] = Decoration  # 装修
            dic['Type'] = Type  # 类型
            dic['Village'] = Village
            dic['District'] = District
            dic['County'] = County
            dic['General'] = General

            lis.append(dic)
            print(str(count)+'.'+str(title)+' '+str(Price)+' '+str(HouseType)+' '+Area+' ' +
                  Orientation+' '+Floor+' '+Decoration+' '+Type+' '+Village+' '+District+' '+County)
            if(count == total_count):
                break
            count = count+1
        page = page+1
        url = url+'fangyuan/p'+str(page)
    j = json.dumps(lis, ensure_ascii=False)
    print(j)
    f = open('安居客/房源信息.txt', 'w')
    f.write(j)
    f.close()


main()
