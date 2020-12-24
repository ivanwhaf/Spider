import requests
import json
import time
import pymysql
import sys
import threading
sys.setrecursionlimit(100)
url_token_g = 'excited-vczh'
# url_token='edward-barnard'
'''https://www.zhihu.com/api/v4/members/wu-yu-fan-66-20/followers?include=data%5B*%5D.answer_count% \
2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'''

'''https://www.zhihu.com/api/v4/members/wu-yu-fan-66-20?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count\
%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2C\
following_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccolumns_count%2Ccommercial_question_count%2C\
favorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2C\
is_bind_phone%2Cis_force_renamed%2Cis_bind_sina%2Cis_privacy_protected%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2C\
is_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2C\
hosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'''

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
           'Accept-Language': 'zh-CN',
           'Upgrage-Insecure-Requests': '1',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'}
total_number = 0
user_list = []
proxies = {}


def get_detail_info(url_token):
    # start=time.clock()
    global total_number
    api_info = 'https://www.zhihu.com/api/v4/members/'+url_token+'?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count\
	%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2C\
	following_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccolumns_count%2Ccommercial_question_count%2C\
	favorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2C\
	is_bind_phone%2Cis_force_renamed%2Cis_bind_sina%2Cis_privacy_protected%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2C\
	is_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2C\
	hosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
    try:
        r = requests.get(api_info, headers=headers, proxies=proxies)
    except:
        print('get info error!')
        # time.sleep(60)
        return
    try:
        j = json.loads(r.text)
    except:
        print('json loads error!')
        return
    if 'error' in j:
        print(url_token+'账号已注销')
        return
    id = j['id']  # id
    name = j['name']  # 昵称
    url = j['url']  # 个人主页链接
    headline = j['headline']  # 一句话介绍
    description = j['description']  # 个人简介
    gender = j['gender']  # 性别男为1,整形
    follower_count = j['follower_count']  # 关注者人数
    following_count = j['following_count']  # 关注人数
    answer_count = j['answer_count']  # 回答数量
    question_count = j['question_count']  # 提问数量
    articles_count = j['articles_count']  # 文章数量
    columns_count = j['columns_count']  # 专栏数量
    favorite_count = j['favorite_count']  # 收藏夹数量
    favorited_count = j['favorited_count']  # 被收藏数量
    pins_count = j['pins_count']  # 想法数量
    logs_count = j['logs_count']  # 参与公共编辑数量
    voteup_count = j['voteup_count']  # 获得赞同(点赞)数量
    thanked_count = j['thanked_count']  # 获得感谢数量
    participated_live_count = j['participated_live_count']  # 赞助的live数量
    following_columns_count = j['following_columns_count']  # 关注的专栏数量
    following_topic_count = j['following_topic_count']  # 关注的话题数量
    following_question_count = j['following_question_count']  # 关注的问题数量
    following_favlists_count = j['following_favlists_count']  # 关注的收藏夹数量

    business = j['business']  # 所在行业,字典
    business_name = business['name']  # 所在行业名称

    locations = j['locations']  # 居住地,列表
    if locations:
        locations = locations[0]
        locations_name = locations['name']
    else:
        locations_name = ''

    employments = j['employments']  # 职业经历,列表
    if employments:
        employments = employments[0]
        if 'job' in employments:
            job = employments['job']
            job_name = job['name']  # 职位名称
        else:
            job_name = ''
        if 'company' in employments:
            company = employments['company']
            company_name = company['name']  # 公司名称
        else:
            company_name = ''
    else:
        job_name = ''
        company_name = ''

    educations = j['educations']  # 教育经历,列表
    if educations:
        educations = educations[0]
        if 'school' in educations:
            school = educations['school']
            school_name = school['name']  # 学校名称
        else:
            school_name = ''
        if 'major' in educations:
            major = educations['major']
            major_name = major['name']  # 专业方向名称
        else:
            major_name = ''
    else:
        school_name = ''
        major_name = ''

    is_bind_sina = j['is_bind_sina']  # 是否绑定微博
    if is_bind_sina:
        if 'sina_weibo_name' in j:
            sina_weibo_name = j['sina_weibo_name']  # 微博昵称
        else:
            sina_weibo_name = ''
        if 'sina_weibo_url' in j:
            sina_weibo_url = j['sina_weibo_url']  # 微博主页
        else:
            sina_weibo_url = ''
    else:
        sina_weibo_name = ''
        sina_weibo_url = ''

    total_number = total_number+1

    print(str(total_number)+'.'+name+' '+url_token+' '+str(gender)+' ' +
          headline+' '+description+' '+str(follower_count)+' '+str(following_count))

    # start=time.clock()
    conn = pymysql.connect('localhost', 'root', '111111', 'zhihu')
    cursor = conn.cursor()
    sql = "INSERT INTO zhihu_user(name,url_token,id,url,headline,description,gender,follower_count,following_count,answer_count,question_count,articles_count,\
	columns_count,favorite_count,favorited_count,pins_count,logs_count,voteup_count,thanked_count,participated_live_count,following_columns_count,following_topic_count,\
	following_question_count,following_favlists_count,locations_name,company_name,job_name,school_name,major_name,sina_weibo_name,sina_weibo_url)\
	VALUES('{}','{}','{}','{}','{}','{}',{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},'{}','{}','{}','{}','{}','{}','{}')".format(name, url_token, id, url, headline,
                                                                                                                                        description, gender, follower_count, following_count, answer_count, question_count, articles_count, columns_count, favorite_count, favorited_count, pins_count, logs_count, voteup_count,
                                                                                                                                        thanked_count, participated_live_count, following_columns_count, following_topic_count, following_question_count, following_favlists_count, locations_name, company_name, job_name,
                                                                                                                                        school_name, major_name, sina_weibo_name, sina_weibo_url)

    try:
        cursor.execute(sql)
        conn.commit()
    except:
        total_number = total_number-1
        print('execute sql error!')
        conn.rollback()
        cursor.close()
        conn.close()
        return

    cursor.close()
    conn.close()
    if total_number % 300 == 0:
        time.sleep(1)
    # end=time.clock()
    # print(end-start)


def craw(url_token):
    api_followers = 'https://www.zhihu.com/api/v4/members/'+url_token+'/followers?'
    try:
        r = requests.get(api_followers, headers=headers, proxies=proxies)
    except:
        print('get followers error!')
        # time.sleep(60)
        return
    try:
        j = json.loads(r.text)  # json字符串转换成字典
    except:
        print('follower json loads error!')
        return

    try:
        paging = j['paging']
    except:
        print('get paging error!')
        print(j)
        if 'error' in j:
            # time.sleep(60)
            pass
        return
    totals = paging['totals']

    if totals == 0:
        print(url_token+' no followers!')
        return

    print(url_token+' followers:'+str(totals))

    if totals % 20 == 0:
        page = int(totals/20)
    else:
        page = int(totals/20+1)

    for p in range(page):
        offset = p*20
        api_followers = api_followers+'&offset='+str(offset)+'&limit=20'
        try:
            r = requests.get(api_followers, headers=headers, proxies=proxies)
        except:
            print('get followers error!')
            # time.sleep(60)
            return
        try:
            j = json.loads(r.text)  # json字符串转换成字典
        except:
            print('follower json loads error!')
            print(j)
            return

        follower_url_token_list = []
        data = j['data']
        for follower in data:
            follower_url_token = follower['url_token']
            follower_url_token_list.append(follower_url_token)

        for i in range(len(follower_url_token_list)-1, -1, -1):
            t = follower_url_token_list[i]

            conn = pymysql.connect('localhost', 'root', '111111', 'zhihu')
            cursor = conn.cursor()
            sql = "SELECT 1 FROM zhihu_user where url_token='"+t+"'"
            cursor.execute(sql)
            f = cursor.fetchone()
            cursor.close()
            conn.close()
            if f == None:
                get_detail_info(t)

            else:
                print('repeat')
                follower_url_token_list.pop(i)

        for t in follower_url_token_list:
            craw(t)


def update_proxies():
    global proxies
    try:
        r = requests.get('http://120.79.180.139:88/proxy', timeout=2)
        j = json.loads(r.text)
    except:
        print('get proxy error!')
        proxies = {}
        update_proxies_thread = threading.Timer(10, update_proxies)
        update_proxies_thread.start()
        return
    print('get proxy-----------------------')
    print(j)
    proxies = j
    update_proxies_thread = threading.Timer(10, update_proxies)
    update_proxies_thread.start()


def main():
    update_proxies_thread = threading.Timer(10, update_proxies)
    update_proxies_thread.start()
    craw(url_token_g)


if __name__ == '__main__':
    main()
