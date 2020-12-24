import requests
import os
import time
import json
import wx
import threading

# playlist_id='870048000' #歌单id
playlist_api = 'http://music.163.com/api/playlist/detail?id='
# playlist_url=playlist_api+playlist_id #歌单api

music_url = 'http://music.163.com/song/media/outer/url?id='  # 歌曲api
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
path = '网易云'  # 音乐下载目录

song_id = '4153366'
comment_api = 'http://music.163.com/api/v1/resource/comments/R_SO_4_'
comment_url = comment_api+song_id+'?limit=100&offset='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.3'}
# total_number=200 #要爬取的评论总数


class mainFrame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title,
                          pos=(500, 200), size=(830, 520))
        self.number = 200  # 要爬取的评论总数
        self.isLoading = False
        self.isDownloading = False
        self.isGetting = False
        self.statusbar = self.CreateStatusBar()
        self.playlist_id_label = wx.StaticText(self, pos=(
            5, 10), label='歌单id:', size=(50, 30), style=wx.ALIGN_CENTER)
        self.playlist_id_label = wx.StaticText(self, pos=(
            410, 10), label='歌曲id:', size=(50, 30), style=wx.ALIGN_CENTER)
        self.total_number_label = wx.StaticText(self, pos=(
            680, 10), label='数量:', size=(50, 30), style=wx.ALIGN_CENTER)

        self.song_id_text = wx.TextCtrl(self, pos=(460, 5), size=(150, 30))
        self.playlist_id_text = wx.TextCtrl(self, pos=(55, 5), size=(200, 30))
        self.playlist_text = wx.TextCtrl(self, pos=(
            5, 40), size=(400, 415), style=wx.TE_MULTILINE)

        self.comment_text = wx.TextCtrl(self, pos=(
            410, 40), size=(400, 415), style=wx.TE_MULTILINE)
        self.total_number_text = wx.TextCtrl(self, pos=(
            725, 5), size=(80, 30), value=str(self.number))

        load_playlist_button = wx.Button(
            self, label='加载歌单', pos=(268, 5), size=(60, 30))
        download_music_button = wx.Button(
            self, label='下载歌曲', pos=(343, 5), size=(60, 30))
        get_comment_button = wx.Button(
            self, label='获取评论', pos=(620, 5), size=(60, 30))

        load_playlist_button.Bind(wx.EVT_BUTTON, self.load)
        download_music_button.Bind(wx.EVT_BUTTON, self.download)
        get_comment_button.Bind(wx.EVT_BUTTON, self.get)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.timer = wx.Timer(self)  # 要加self
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)
        self.Show(True)

    def OnTimer(self, evt):  # 显示时间事件处理函数
        t = time.localtime(time.time())
        StrYMDt = time.strftime("%Y-%m-%d %H:%M:%S", t)
        self.statusbar.SetStatusText(StrYMDt)  # 显示年月

    def load_playlist_raw(self, playlist_url):
        r = requests.get(playlist_url, headers=headers)
        result = {}
        try:
            result = json.loads(r.text)['result']
            self.playlist_text.AppendText('正在加载歌单列表...\n')
        except:
            dlg = wx.MessageDialog(None, '歌单id无效!')
            dlg.ShowModal()
            dlg.Destroy()
            return
        tracks = []
        tracks = result['tracks']  # tracks列表
        self.playlist_text.Clear()
        if(len(tracks) == 0):
            self.playlist_text.AppendText('歌单为空!\n')
            return

        count = 0
        for music in tracks:
            song_name = music['name']
            singer_name = music['artists'][0]['name']
            count = count+1
            song_full_name = song_name+' - '+singer_name
            self.playlist_text.AppendText(str(count)+'.'+song_full_name+'\n')
        self.playlist_text.AppendText('歌单加载完成!\n')
        return tracks

    def load_playlist(self):
        self.playlist_id = self.playlist_id_text.GetValue()
        if self.playlist_id == '':
            dlg = wx.MessageDialog(None, '请输入歌单id!')
            dlg.ShowModal()
            dlg.Destroy()
            return
        playlist_url = playlist_api+self.playlist_id
        self.load_playlist_raw(playlist_url)
        self.isLoading = False

    def load(self, event):  # 按钮绑定函数
        if(self.isLoading == True or self.isDownloading == True):
            return
        self.isLoading = True
        load_thread = threading.Thread(target=self.load_playlist)
        load_thread.setDaemon(True)  # 设置为守护主线程
        load_thread.start()

    def download_music(self, path, song_url, song_name, singer_name, count):
        song_full_name = song_name+' - '+singer_name+'.mp3'
        try:
            r = requests.get(song_url, headers=headers, stream=True)
        except:
            self.playlist_text.AppendText(song_full_name+' 下载失败!\n')
            return count
        try:
            with open(path+'/'+song_full_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=32):
                    f.write(chunk)
        except:
            self.playlist_text.AppendText(song_full_name+' 下载失败!\n')
            return count
        count = count+1
        self.playlist_text.AppendText(str(count)+'. '+song_full_name+' 下载完成\n')
        return count

    def download_all_music(self, path=path, music_url=music_url):
        self.playlist_id = self.playlist_id_text.GetValue()
        if self.playlist_id == '':
            dlg = wx.MessageDialog(None, '请输入歌单id!')
            dlg.ShowModal()
            dlg.Destroy()
            self.isDownloading = False
            return
        playlist_url = playlist_api+self.playlist_id
        r = requests.get(playlist_url, headers=headers)
        result = {}
        try:
            result = json.loads(r.text)['result']
        except:
            dlg = wx.MessageDialog(None, '歌单id无效!')
            dlg.ShowModal()
            dlg.Destroy()
            self.isDownloading = False
            return
        tracks = []
        tracks = result['tracks']  # tracks列表

        path = path+'/'+self.playlist_id  # 网易云/id
        if(not os.path.exists(path)):
            os.makedirs(path)
        self.playlist_text.AppendText('开始下载歌曲...\n')
        count = 0
        for music in tracks:
            song_name = music['name']
            song_id = music['id']
            singer_name = music['artists'][0]['name']
            song_url = music_url+str(song_id)+'.mp3'
            count = self.download_music(
                path, song_url, song_name, singer_name, count)  # 下载歌曲
        self.playlist_text.AppendText('歌曲全部下载完成\n')
        self.isDownloading = False

    def download(self, event):  # 按钮绑定函数
        if(self.isLoading == True or self.isDownloading == True):
            return
        self.isDownloading = True
        download_thread = threading.Thread(target=self.download_all_music)
        download_thread.setDaemon(True)  # 设置为守护主线程
        download_thread.start()

    def get_comment(self, comment_url=comment_url):
        self.song_id = self.song_id_text.GetValue()
        if self.song_id == '':
            dlg = wx.MessageDialog(None, '请输入歌曲id!')
            dlg.ShowModal()
            dlg.Destroy()
            self.isGetting = False
            return
        self.total_number = self.total_number_text.GetValue()
        if self.total_number == '':
            self.total_number = self.number
        try:
            self.total_number = int(self.total_number)
        except:
            dlg = wx.MessageDialog(None, '请输入整数数量!')
            dlg.ShowModal()
            dlg.Destroy()

        comment_url = comment_api+self.song_id+'?limit=100&offset='

        number = 0  # 已爬取的评论总数
        offset = 0  # 偏移量
        self.comment_text.Clear()
        self.comment_text.AppendText('开始获取评论...\n')
        while offset < self.total_number:
            url = comment_url+str(offset)
            r = requests.get(url, headers=headers)
            try:
                j = json.loads(r.text)
            except:
                self.comment_text.AppendText('json loads error!+'+'\n')
                continue
            try:
                comments = j['comments']
            except:
                dlg = wx.MessageDialog(None, '歌曲id无效!')
                dlg.ShowModal()
                dlg.Destroy()
                self.isGetting = False
                return
            total = j['total']
            if total == 0:
                self.comment_text.AppendText('评论为空...\n')
                self.isGetting = False
                return
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
                self.comment_text.AppendText(
                    str(number)+'. '+str(tIme)+' '+str(likedCount)+' '+content+'\n')
                if(number == self.total_number):
                    break
            offset = offset+100
        self.comment_text.AppendText('评论获取完毕!'+'\n')
        self.isGetting = False

    def get(self, event):  # 按钮绑定函数
        if(self.isGetting == True):
            return
        self.isGetting = True
        get_thread = threading.Thread(target=self.get_comment)
        get_thread.setDaemon(True)  # 设置为守护主线程
        get_thread.start()

    def OnCloseWindow(self, evt):
        dlg = wx.MessageDialog(None, u'确定要关闭本程序？', u'操作提示',
                               wx.YES_NO | wx.ICON_QUESTION)
        if(dlg.ShowModal() == wx.ID_YES):
            self.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    frame = mainFrame('网易云')
    app.MainLoop()
