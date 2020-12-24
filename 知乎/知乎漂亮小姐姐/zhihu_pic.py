import requests
from bs4 import BeautifulSoup
import json
import os
import time
# url="https://www.zhihu.com/question/34243513/answers/created?page=1"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}
cookies = {
    'cookies': '_zap=621c86b9-c821-4717-9bb9-6f2b8ba24a86; q_c1=1ac94f4c1b9849be98be396777176709|1507043413000|1498537392000; d_c0="AJAspDMbFA2PTjRF4bDhv33jurIofXgrrCo=|1517467607"; __utmv=51854390.100--|2=registration_date=20170105=1^3=entry_date=20170105=1; __utma=51854390.340065372.1517470161.1517470161.1521730518.2; __utmz=51854390.1521730518.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; __DAYU_PP=RjBnZURAi3YI6iMBMeaj2db6b2ad7825; q_c1=1ac94f4c1b9849be98be396777176709|1522921198000|1498537392000; aliyungf_tc=AQAAAPr21GFksQwAZmpmtEHOw7BZ/Bdw; _xsrf=6dd2e0ad-1595-4382-9ef0-88a5eaac809a; capsion_ticket="2|1:0|10:1523359133|14:capsion_ticket|44:MjRkMTIzYmI5YmM5NDRlNzkwNWM1OGU3Y2QxZDUxODc=|aefc790647eec39248328c0251cc7589ec14092f052820d1b6c631681af66449"; z_c0="2|1:0|10:1523359153|4:z_c0|92:Mi4xXy1fa0F3QUFBQUFBa0N5a014c1VEU1lBQUFCZ0FsVk5zZXU1V3dCYl9HalFmalBEVTdMVTA1Z0Z6MlVpaERoYXp3|7e9b4ad1c4a208bb6a0549e16b32cc73e0a0ebef53cf87eda5c86158e58b815a"'}


questionId = '34243513'
answer_num = 6560
offset = 0
img_count = 1
question_id = '34243513'
img_path = './知乎'
length = ''


def download(img_url, fileType):
    global img_count
    global length
    img = requests.get(img_url, stream=True)
    try:
        length = img.headers['Content-Length']
    except:
        length = ''
    if length != '320':
        f = open(img_path+'/'+str(img_count)+fileType, 'wb')
        for chunk in img.iter_content(chunk_size=1024):
            if chunk:
                try:
                    f.write(chunk)
                except:
                    continue
        img_count = img_count+1


def main():
    global offset
    global img_count
    global length
    global answer_num
    if not os.path.exists(img_path):
        os.makedirs(img_path)

    while offset <= answer_num:
        url = 'https://www.zhihu.com/api/v4/questions/'+question_id + \
            '/answers?sort_by=created&include=data[*].is_normal,voteup_count,content&limit=20&offset='+str(
                offset)
        r = requests.get(url, headers=headers, cookies=cookies)
        dic = json.loads(r.text)
        for data in dic['data']:
            content = data['content']
            soup = BeautifulSoup(content, 'html.parser')
            figures = soup.find_all('figure')
            for figure in figures:
                img = figure.find('img')
                img_url = img.get('src')
                n, fileType = os.path.splitext(img_url)
                download(img_url, fileType)
                time.sleep(0.5)
                print(img_url+' '+length+'B  '+'offset:'+str(offset))
        offset = offset+20
    print('下载完成')
    input()
# https://www.zhihu.com/api/v4/questions/34243513/answers?sort_by=created&include=data[*].is_normal,voteup_count,content&limit=20&offset=6560


# https://pic4.zhimg.com/50/v2-c1c88ea1356b1548049cf584ec7d7445_hd.jpg1
# r=requests.get('https://pic3.zhimg.com/50/v2-31a7cc48c58431d80f20316e9a94ba2a_hd.jpg')
# print(r.headers)

def get():
    s = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(s.text, 'html.parser')
    answer_count = soup.find('meta', itemprop='answerCount').get('content')
    question_main = soup.find('div', class_='Question-main')
    question_list = question_main.find('div', class_='List')
    for list_item in question_list.find_all('div', class_='List-item'):
        span = list_item.find('span', itemprop='text')
        imgs = span.find_all('img')
        for img in imgs:
            img_url = img.get('src')
            # print(img_url)
    # print(question_list)


if __name__ == '__main__':
    main()
