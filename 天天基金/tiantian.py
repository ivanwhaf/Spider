import re
import os
import json
import random
import threading
import multiprocessing
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

# 获取所有基金信息接口
url_all_fund = 'http://fund.eastmoney.com/js/fundcode_search.js'

# 获取某一基金历史净值接口
api_lsjz = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={0}&page={1}&per=20'


def get_all_funds():
    """
    获取所有基金信息
    """
    r = requests.get(url_all_fund)
    content = re.findall(r'\[.*\]', r.text)[0]

    funds = json.loads(content)  # 转python列表

    print('基金信息抓取完毕，共：'+str(len(funds))+'个')

    return funds


def save_fund_info_to_excel(funds):
    """
    保存所有基金信息至excel
    """
    df = pd.DataFrame(funds, columns=['基金代码', '基金缩写', '基金名称', '基金类型', '基金拼音'])
    df.to_excel('所有基金信息.xlsx')  # 写入excel
    print(df.info())
    print('基金信息写入excel成功')


def save_fund_lsjz_to_excel(lsjz, code, name):
    """
    保存基金所有历史净值至excel
    """
    df = pd.DataFrame(
        lsjz[1:], columns=lsjz[0])
    df.to_excel('基金净值/'+name.replace('/', '') +
                str(code)+'_历史净值.xlsx')  # 写入excel
    # print(df.info())
    print(name+'净值信息写入excel成功')


def crawl_funds(funds):
    """
    爬取所有基金历史净值
    """
    for fund in funds:
        code = fund[0]  # 基金代码
        name = fund[2]  # 基金名称
        lsjz = crawl_fund(code, name)  # 爬单个基金净值
        if not lsjz:
            print('无基金净值数据！跳过')
            continue
        save_fund_lsjz_to_excel(lsjz, code, name)
        print('---------------------------------')

    print('所有基金历史净值爬取完成')


def crawl_fund(code, name):
    """
    爬取单个基金历史净值
    """
    print('开始爬取'+name+'基金净值：')
    r = requests.get(
        api_lsjz.format(code, '1'))

    # 获取该基金净值数据总页码
    try:
        pages = re.findall(r'pages:[0-9]*', r.text)[0]
        pages = int(pages.split(':')[1])
    except:
        pages = 0
    print('共'+str(pages)+'页基金净值数据 ')

    lsjz = []  # 历史净值信息数组
    for current_page in range(1, pages):
        r = requests.get(
            api_lsjz.format(code, str(current_page)))
        # content = re.findall(r'\{.*\}', r.text)[0]
        soup = bs(r.text, 'html.parser')
        trs = soup.find_all('tr')

        # 获取头部标题信息
        if current_page == 1:
            tr0 = trs[0]
            title = []
            for th in tr0.find_all('th'):
                title.append(th.text)
            lsjz.append(title)

        trs = trs[1:]  # 剔除第一行标题行

        for tr in trs:
            # 获取每一项净值信息
            tds = tr.find_all('td')
            lst = []
            for td in tds:
                lst.append(td.text)
                """
                jzrq = tds[0].text  # 净值日期
                dwjz = tds[1].text  # 单位净值
                ljjz = tds[2].text  # 累计净值
                rzzl = tds[3].text  # 日增长率
                sgzt = tds[4].text  # 申购状态
                shzt = tds[5].text  # 赎回状态
                fhsp = tds[6].text  # 分红送配
                """
            lsjz.append(lst)

        # print('第'+str(current_page)+'页净值抓取完成')
    print(name+'基金历史净值信息爬取完成')

    return lsjz


def split_funds(funds):
    """
    按步长拆分数据集，以便多线程并发爬取
    """
    step = 500
    n = len(funds)//step
    ret = []
    for i in range(n+1):
        ret.append(funds[i*step:(i+1)*step])
    print('共拆分成：'+str(len(ret)))
    return ret


def main():
    if not os.path.exists('基金净值'):
        os.makedirs('基金净值')

    funds = get_all_funds()  # 爬所有基金信息
    save_fund_info_to_excel(funds)  # 保存所有基金信息至excel

    # lsjz = crawl_fund('519674', '银河创新成长混合')  # 爬银河创新成长混合净值
    # save_fund_lsjz_to_excel(lsjz, '519674', '银河创新成长混合') # 保单个有基金净值至excel

    random.shuffle(funds)  # 随机打乱funds数组
    funds_ = split_funds(funds)  # 按步长拆分数据

    # 多线程爬取
    for funds in funds_:
        # thread = threading.Thread(
        # target=crawl_funds, args=(funds,), daemon=True)
        # thread.start()
        process = multiprocessing.Process(
            target=crawl_funds, args=(funds,), daemon=True)
        process.start()
        print('线程/进程开启成功')

    # crawl_funds(funds)  # 爬所有基金净值

    # 因为设置了线程为守护线程，所以防止线程退出加上死循环
    while True:
        pass


if __name__ == "__main__":
    main()
