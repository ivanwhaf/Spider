import requests
import json
import os

playlist_id = '870048000'  # 歌单id
playlist_url = 'http://music.163.com/api/playlist/detail?id='+playlist_id  # 歌单api
music_url = 'http://music.163.com/song/media/outer/url?id='  # 歌曲api
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
path = '网易云'  # 音乐下载目录


def download_music(paht, song_url, song_name, singer_name, count):
    song_full_name = song_name+' - '+singer_name+'.mp3'
    try:
        r = requests.get(song_url, headers=headers, stream=True)
    except:
        print(song_full_name+' 下载失败!')
        return
    try:
        with open(path+'/'+song_full_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=32):
                f.write(chunk)
    except:
        print(song_full_name+' 下载失败!')
        return
    count = count+1
    print(str(count)+'. '+song_full_name+' 下载完成')
    return count


def load_playlist(playlist_url):
    print('正在加载歌单列表...')
    r = requests.get(playlist_url, headers=headers)
    result = {}
    result = json.loads(r.text)['result']
    tracks = []
    tracks = result['tracks']  # tracks列表
    count = 0
    for music in tracks:
        song_name = music['name']
        singer_name = music['artists'][0]['name']
        count = count+1
        song_full_name = song_name+' - '+singer_name
        print(str(count)+'.'+song_full_name)
    print('歌单加载完成!')
    return tracks


def download_all_music(path, tracks, music_url):
    if(not os.path.exists(path)):
        os.makedirs(path)
    print('开始下载歌曲...')
    count = 0
    for music in tracks:
        song_name = music['name']
        song_id = music['id']
        singer_name = music['artists'][0]['name']
        song_url = music_url+str(song_id)+'.mp3'
        count = download_music(path, song_url, song_name,
                               singer_name, count)  # 下载歌曲
    print('歌曲全部下载完成')


def main():
    tracks = load_playlist(playlist_url)
    download_all_music(path, tracks, music_url)


if __name__ == '__main__':
    main()
