import re
import requests
from bs4 import BeautifulSoup as bs

# 视频链接
video_url = 'https://www.bilibili.com/video/{0}'
# 视频信息
video_url_2 = 'https://api.bilibili.com/x/player/pagelist?bvid={0}&jsonp=jsonp&aid={1}'

# 实时弹幕
comment_api = 'http://api.bilibili.com/x/v1/dm/list.so?oid={0}'
# 实时弹幕
comment_api_2 = 'http://comment.bilibili.com/{0}.xml'
# 历史弹幕
comment_api_3 = 'https://api.bilibili.com/x/v2/dm/history?type=1&oid={0}&date={1}'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}


def get_cid(video_num):
    # 根据视频号（av/BV）获取弹幕cid
    r = requests.get(video_url.format(video_num), headers=headers)
    pattern = 'cid=(.*?)&aid'
    cid = re.search(pattern, r.text).group().replace(
        'cid=', '').replace('&aid', '')
    print('cid:', cid)
    return cid


def get_danmu(cid):
    # 根据cid获取弹幕
    r = requests.get(comment_api.format(cid), headers=headers)
    r.encoding = 'utf-8'  # 设置编码防止乱码
    soup = bs(r.text, 'xml')
    danmu = []
    for i in soup.find_all('d'):
        danmu.append(i.text)
    print(danmu)
    return danmu


if __name__ == "__main__":
    cid = get_cid('BV1Ht4y197Xk')
    danmu = get_danmu(cid)
