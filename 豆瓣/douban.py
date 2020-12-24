import time
import requests
from bs4 import BeautifulSoup as bs


account = 'xxxx'  # your own account here
passwd = 'xxxx'  # your own account passwd
login_url = 'https://www.douban.com/accounts/login'
url = 'https://accounts.douban.com/login'
# your own cookie
headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'cookie': 'bid=bT-Ch6M3Bxo; ll="118159"; push_noty_num=0; push_doumail_num=0; __utmc=30149280; __utmv=30149280.22889; __utmz=30149280.1608786374.5.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=223695111.1608786401.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmc=223695111; __yadk_uid=r23dr0w0wLnnh5n4rTJKHYQhr2XgIyJr; _vwo_uuid_v2=D3355535C05CF1172DC358338004BD62E|ea377b25ba40fb65bb00dcbe60c43e66; ap_v=0,6.0; __utma=30149280.157976968.1608207711.1608797670.1608799731.7; __utma=223695111.2018317551.1608786401.1608797670.1608799731.3; __utmb=223695111.0.10.1608799731; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1608799731%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utmt=1; dbcl2="228891076:FnujCvxorTg"; ck=NmcO; douban-profile-remind=1; __utmb=30149280.9.10.1608799731; _pk_id.100001.4cf6=d65bc380ad65c561.1608786402.3.1608802624.1608797679.; __gads=ID=90f5a584f510d342-227a6b0f4ec500b9:T=1608802623:RT=1608802623:S=ALNI_Mbwtu0AVdq9tNclMoj6cMLTu_2XPQ'}
login_data = {
    'source': 'index_nav',
    'from_email': account,
    'form_password': passwd
}
data = {
    'source': 'index_nav',
    'redir': 'https//www.douban.com',
    'form_email': account,
    'form_password': passwd,
    'login': '登录'
}


def main():
    movie_lst = []
    session = requests.Session()
    # r=requests.post(login_url,data=login_data,headers=headers) # login
    for start in range(0, 250, 25):
        movie_url = 'https://movie.douban.com/top250?start={}'.format(
            str(start))
        r = session.get(movie_url, headers=headers)
        soup = bs(r.text, 'html.parser')
        ol = soup.find('ol', class_='grid_view')
        # for each movie
        for li in ol.find_all('li'):
            # get movie attrs
            rank = li.find('em').string
            href = li.find('a').get('href')
            name = li.find('span').string
            print(rank, name)
            try:
                quote = li.find('span', class_='inq').string
            except:
                quote = ''
            try:
                score = li.find('span', class_='rating_num').string
            except:
                score = '0.0'

            year = li.find('p').contents[2].strip().split('/')[0].strip()
            star = li.find('div', class_='star')
            spans = star.find_all('span')
            comment_num = spans[3].text[:-3]

            # get movie comments
            comment_href = href+'comments?status=P'
            r = requests.get(comment_href, headers=headers)
            soup = bs(r.text, 'html.parser')
            comment_lst = []
            div = soup.find('div', class_='mod-bd')
            com_div = div.find_all('div', class_='comment-item')
            for com in com_div:
                try:
                    comment = com.find('p').text.strip()
                except:
                    continue
                comment_lst.append(comment)

            movie = {}
            movie['rank'] = rank
            movie['name'] = name
            movie['score'] = score
            movie['year'] = year
            movie['comment_num'] = comment_num
            movie['quote'] = quote
            movie['href'] = href
            movie['comment'] = comment_lst
            movie_lst.append(movie)

    # write rank
    with open('豆瓣电影排名.txt', 'w', encoding='utf-8') as f:
        for moive in movie_lst:
            rank, name, year, score, comment_num, quote = moive['rank'], moive['name'], moive[
                'year'], moive['score'], moive['comment_num'], moive['quote']
            f.write('{} 《{}》 ({})  {}分  评价数:{}  短评:{}\n'.format(
                rank, name, year, score, comment_num, quote))

    # write comment
    with open('豆瓣电影评论.txt', 'w', encoding='utf-8') as f:
        for moive in movie_lst:
            rank, name, year, score, comment_lst = moive['rank'], moive['name'], moive[
                'year'], moive['score'], movie['comment']
            f.write('{}.《{}》 ({})  {}分\n'.format(rank, name, year, score))
            for comment in comment_lst:
                f.write(comment+'\n')
            f.write('\n\n')


main()
