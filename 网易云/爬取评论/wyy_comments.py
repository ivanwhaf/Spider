import requests
import time
import json
import os
#import sqlite3

# http://music.163.com/api/v1/resource/comments/R_SO_4_4153366?limit=100&offset=0
song_id = '4153366'
comment_url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' + \
    song_id+'?limit=100&offset='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.3'}
total_number = 200  # 要爬取的评论总数


def get_comments(comment_url, total_number):
    number = 0  # 已爬取的评论总数
    offset = 0  # 偏移量
    print('开始获取评论...')
    while offset < total_number:
        url = comment_url+str(offset)
        r = requests.get(url, headers=headers)
        try:
            j = json.loads(r.text)
        except:
            print('json loads error!')
            continue
        comments = j['comments']
        for comment in comments:
            user = comment['user']
            userId = user['userId']
            nickname = user['nickname']
            likedCount = comment['likedCount']
            content = comment['content']
            timeStamp = str(comment['time'])  # 整形转为字符串
            timeStamp = timeStamp[:10]  # 获取前10位时间戳
            timeArray = time.localtime(int(timeStamp))
            tIme = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            number = number+1
            print(str(number)+'. '+str(tIme)+' ' +
                  str(likedCount)+' '+content+str(number))
            if(number == total_number):
                break
        offset = offset+100
    print('评论获取完毕!')


def main():
    get_comments(comment_url, total_number)


if __name__ == '__main__':
    main()
