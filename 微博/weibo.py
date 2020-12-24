import re
import json
import time
import requests  # install
from bs4 import BeautifulSoup as bs  # install
import jieba  # install
from wordcloud import WordCloud  # install
import matplotlib.pyplot as plt  # install


# weibo_url='https://m.weibo.cn/api/container/getIndex?type=uid&value=2714280233&containerid=1076032714280233&page=1'
# info_url='https://m.weibo.cn/api/container/getIndex?type=uid&value=2714280233&containerid=1076032714280233'
# detail_info_url='https://m.weibo.cn/api/container/getIndex?containerid=2302832714280233_-_INFO&title=%E5%9F%BA%E6%9C%AC%E8%B5%84%E6%96%99'
# followers_url='https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_2714280233&page=1'
# fans_url='https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_2714280233&page=1'

uid = 5745483847
baidu_ua = 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
headers = {'User-Agent': ua,
           'Cookie': '_T_WM=56586220990; ALF=1584071365; WEIBOCN_FROM=1110106030; SCF=ApCyY_SjxR35FsnN5jtX5lFyc964MW3RH6DUxngAK15NjPWo2SJDO9L9HDPWANATYbmynouamRoR1wfgkNZfRVI.; SUB=_2A25zR-XCDeRhGeRK6FoT8CfOyTiIHXVQy4uKrDV6PUJbktAKLXDmkW1NU2NrxjBVdhjhMT_P__oBNrrOSMDvhIUY; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5jJcKpJl.x8Qm_e0dQD1Fn5JpX5K-hUgL.FozXe0nEeh.EeoB2dJLoIX2LxK-L1K5L1h.LxK-LBo5L1KBLxK-LBo5LB.eLxKML1-2L1hBLxKMLBo2LBoeLxK-L1KeLBK.LxKML1hzL128kH7tt; SUHB=0pHwvs8sIfGRT5; SSOLoginState=1581487505; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D2302832438209225_-_INFO%26fid%3D2302832438209224_-_INFO%26uicode%3D10000011; XSRF-TOKEN=3ed46f'
           }
users = {}


def get_weibo_url(uid, page):
    # 获取个人微博url
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + \
        str(uid)+'&containerid=107603'+str(uid)+'&page='+str(page)
    return url


def get_user_info_url(uid):
    # 获取个人信息url
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + \
        str(uid)+'&containerid=100505'+str(uid)
    return url


def get_user_detail_info_url(uid):
    # 获取个人详细信息url
    url = 'https://m.weibo.cn/api/container/getIndex?containerid=230283' + \
        str(uid)+'_-_INFO&title=%E5%9F%BA%E6%9C%AC%E8%B5%84%E6%96%99'
    return url


def get_user_followers_url(uid, page):
    # 获取用户关注者信息url
    url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_' + \
        str(uid)+'&page='+str(page)
    return url


def get_weibo_text(uid):
    # 抓取用户所有微博内容，返回微博字符串
    page = 1  # 从第一页开始 第0页与第一页有重复博客
    num = 1
    weibo_text = ''
    while(True):
        url = get_weibo_url(uid, page)
        r = requests.get(url, headers=headers)
        time.sleep(1)
        j = json.loads(r.text)
        if j['ok'] != 1:
            break
        cards = j['data']['cards']

        for card in cards:
            if 'mblog' in card:
                mblog = card['mblog']
                text = mblog['text']
                weibo_text += text
                print(str(num)+'.'+text)
                num += 1
        page += 1
    return weibo_text


def weibo_text_handling(text):
    # 微博内容处理
    pattern = re.compile(r'<.*?>')
    text = re.sub(pattern, '', text)
    text = text.replace('转发微博', '')  # 替换掉转发微博
    text = text.replace('网页链接', '')  # 替换掉网页链接
    return text


def make_wordcloud(text):
    # 词云制作
    wordlist = jieba.cut(text)
    list_split = " ".join(wordlist)
    print('list_text:\n'+list_split)
    # pic=np.array(Image.open(image_path))
    wd = WordCloud(background_color='white', max_font_size=52, max_words=150,
                   font_path='./yy.TTF', random_state=150).generate(list_split)
    # image_colors = ImageColorGenerator(pic)
    # plt.imshow(wd.recolor(color_func=image_colors))
    plt.imshow(wd, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def get_user_info(uid):
    # 获取用户基本信息，包括粉丝数、关注数
    r = requests.get(get_user_info_url(uid), headers=headers)
    j = json.loads(r.text)
    info = j['data']['userInfo']
    return info


def get_user_detail_info(uid):
    # 获取用户详细信息，包括昵称、简介、注册时间、性别、生日、情感状况、所在地等
    r = requests.get(get_user_detail_info_url(uid), headers=headers)
    j = json.loads(r.text)
    if j['ok'] != 1:
        return {}
    cards = j['data']['cards'][0:2]
    user = {'昵称': '', 'uid': uid, '性别': '', '生日': '', '所在地': '',
            '注册时间': '', '简介': '', '大学': '', '电话': '', '邮箱': '', '公司': ''}
    info = ''
    for card in cards:
        for card_g in card['card_group']:
            if 'item_name' in card_g:
                info += card_g['item_content']+' '
                user[card_g['item_name']] = card_g['item_content']

    return user


def get_user_followers(uid):
    # 获取用户关注者信息，包括id
    global users
    page = 1
    num = 0
    while(True):
        r = requests.get(get_user_followers_url(uid, page), headers=headers)
        j = json.loads(r.text)
        if j['ok'] != 1:
            print('请求频繁 | 页面超出')
            break

        cards = j['data']['cards']
        followers = []
        for card in cards:
            if card['itemid'] != '':
                followers = card['card_group']
        for f in followers:
            user = f['user']
            uid = user['id']
            if uid in users:
                continue
            followers_count = user['followers_count']  # 粉丝数
            follow_count = user['follow_count']  # 关注数
            num += 1
            user = get_user_detail_info(uid)
            if not user:
                print('请求频繁')
                continue
            user['粉丝数'] = followers_count
            user['关注数'] = follow_count
            users[uid] = user
            print(user)
            get_user_followers(uid)
        page += 1


def main():
    # text=get_weibo_text(uid) # 用户微博
    # print('weibo_text:\n'+text)
    # text=weibo_text_handling(text)
    # print('handle_text:\n'+text)
    # make_wordcloud(text) # 词云

    # get_user_detail_info(uid) # 用户详细信息
    get_user_followers(uid)  # 用户关注者


if __name__ == "__main__":
    main()
