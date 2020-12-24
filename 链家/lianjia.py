import os
import re
import time
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


city2abbr = {"北京": "bj", "上海": "sh", "广州": "gz", "深圳": "sz",
             "杭州": "hz", "重庆": "cq", "天津": "tj", "南京": "nj", "成都": "cd"}  # 城市名-缩写

city = "南京"  # !!选择你要爬取的城市!!

main_url = "https://%s.lianjia.com" % city2abbr[city]  # 链家xx市主页
cj_url = "https://%s.lianjia.com/chengjiao" % city2abbr[city]  # 链家xx市已成交房源主页

path = "链家2/"  # 存放excel的文件夹
headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'}  # 百度UA
columns = ["名称", "成交日期", "成交价格（万）",
           "挂牌价格（万）", "成交周期（天）", "调价（次）",
           "带看（次）", "关注（人）", "浏览（次）", "房屋户型", "所在楼层",
           "建筑面积", "户型结构", "套内面积", "建筑类型", "房屋朝向",
           "建成年代", "装修情况", "建筑结构", "供暖方式",
           "梯户比例", "配备电梯", "链家编号", "交易权属",
           "房屋用途", "房屋年限", "房权所属", "城市", "区/县",
           "镇/街道", "小区", "小区编号", "经度", "纬度"]  # 指定pandas导出excel时列名顺序


def get_areas():
    """获取城市各区对应的镇/街道 和 每个镇/街道对应的url字典
    rdic:{"西城":{"西单":"/chengjiao/xidan/","新街口":"/chengjiao/新街口2/"}}
    """
    rdic = {}
    r = requests.get(cj_url, headers=headers)
    soup = bs(r.text, 'html.parser')
    # 区域div中的每一个a标签对应一个区
    tag_a = soup.find('div', attrs={'data-role': "ershoufang"}).find_all('a')
    for a in tag_a:
        district = a.text  # 区名称
        rdic[district] = {}
        dis_href = a.get("href")  # 每个区对应的url后缀,例如:"/chengjiao/gulou/"
        dis_url = main_url+dis_href  # 每个区成交记录的url
        r = requests.get(dis_url, headers=headers)
        soup = bs(r.text, 'html.parser')
        tag_a2 = soup.find('div', attrs={'data-role': "ershoufang"}).find_all('div')[
            1].find_all('a')  # 镇/街道div中的每一个a标签对应一个镇/街道
        for a2 in tag_a2:
            town = a2.text  # 镇/街道名称
            # 每个镇/街道对应的url后缀,例如:"/chengjiao/fujianlu/"
            town_href = a2.get("href")
            town_url = main_url+town_href
            print(town_url)
            rdic[district][town] = town_url
        time.sleep(0.5)
    return rdic


def get_town_houses_url_list(town_url, town):
    """获取每一个镇/街道的已成交的房源详细信息url链接
    """
    rlst = []
    try:
        r = requests.get(town_url, headers=headers)
    except:
        return rlst
    soup = bs(r.text, 'html.parser')
    span = soup.find('div', attrs={"class": "total fl"}).find('span')
    total_count = int(span.text)
    print(town, "街道房源总数："+str(total_count))
    total_page = int(total_count/30+1)
    for i in range(1, total_page+1):
        pg_url = town_url+'pg'+str(i)
        try:
            r = requests.get(pg_url, headers=headers)
        except:
            continue
        soup = bs(r.text, 'html.parser')
        ul = soup.find('ul', attrs={"class": "listContent"})
        house_li = ul.find_all("li")
        for li in house_li:
            div = li.find('div')
            a = div.find('a')
            href = a.get("href")
            # print(href)
            rlst.append(href)
    return rlst


def get_house_info(house_url, district, town, data_district, data):
    """获取每一个已售房源的具体信息并存入datafram
    """
    try:
        r = requests.get(house_url, headers=headers)
    except:
        return
    soup = bs(r.text, 'html.parser')

    resblock_id = soup.find(
        "div", attrs={"class": "house-title"}).get("data-lj_action_housedel_id")  # 小区id

    div = soup.find("div", attrs={"class": "wrapper"})
    name = div.find("h1").text  # 名称
    resblock = name.split(" ")[0]  # 小区名
    deal_date = div.find("span").text.split(" ")[0].replace(".", "-")  # 成交日期

    div = soup.find("div", attrs={"class": "price"})
    deal_price = div.find("span").find("i").text  # 成交价格
    # price_per_square = div.find("b").text  # 每平米单价

    spans = soup.find("div", attrs={"class": "msg"}).find_all("span")
    listing_price = spans[0].find("label").text  # 挂牌价格
    trans_cycle = spans[1].find("label").text  # 成交周期
    price_change = spans[2].find("label").text  # 调价
    take_look = spans[3].find("label").text  # 带看
    follow = spans[4].find("label").text  # 关注
    browse = spans[5].find("label").text  # 浏览

    li = soup.find_all("div", attrs={"class": "content"})[
        0].find("ul").find_all("li")
    layout = li[0].text[4:].strip()  # 房屋户型 ·一室一厅
    floor = li[1].text[4:].strip()  # 所在楼层 ·低楼层（共17层）
    area = li[2].text[4:].strip()[0:-1]  # 建筑面积 ·42m²
    layout_structure = li[3].text[4:].strip()  # 户型结构 ·平层
    area_inside = li[4].text[4:].strip()  # 套内面积
    building_type = li[5].text[4:].strip()  # 建筑类型 ·塔楼
    direction = li[6].text[4:].strip()  # 房屋朝向 ·西
    age = li[7].text[4:].strip()  # 建成年代 ·2010
    decoration = li[8].text[4:].strip()  # 装修情况 ·精装
    building_structure = li[9].text[4:].strip()  # 建筑结构 ·钢混结构
    heating = li[10].text[4:].strip()  # 供暖方式 ·集体供暖
    ratio_of_elevator = li[11].text[4:].strip()  # 梯户比例 .一梯两户
    elevator = li[12].text[4:].strip()  # 配备电梯 ·有
    # property_right_age_limit = li[12].text[4:].strip()[0:-1]  # 产权年限 ·65年

    li = soup.find_all("div", attrs={"class": "content"})[
        1].find("ul").find_all("li")
    house_id = li[0].text[4:].strip()  # 链家编号
    trading_right = li[1].text[4:].strip()  # 交易权属 ·商品房
    housing_use = li[3].text[4:].strip()  # 房屋用途 ·普通住宅
    house_age_limit = li[4].text[4:].strip()  # 房屋年限
    house_ownership = li[5].text[4:].strip()  # 房权所属

    pattern = re.compile(r'resblockPosition:.+\'')
    text = pattern.findall(r.text)[0]
    lng_lat = text.split("'")[1]
    longitude = lng_lat.split(",")[0]  # 经度
    latitude = lng_lat.split(",")[1]  # 纬度

    d = {"名称": name, "成交日期": deal_date, "成交价格（万）": deal_price,
         "挂牌价格（万）": listing_price, "成交周期（天）": trans_cycle, "调价（次）": price_change,
         "带看（次）": take_look, "关注（人）": follow, "浏览（次）": browse, "房屋户型": layout, "所在楼层": floor,
         "建筑面积": area, "户型结构": layout_structure, "套内面积": area_inside, "建筑类型": building_type, "房屋朝向": direction,
         "建成年代": age, "装修情况": decoration, "建筑结构": building_structure, "供暖方式": heating,
         "梯户比例": ratio_of_elevator, "配备电梯": elevator,  "链家编号": house_id, "交易权属": trading_right,
         "房屋用途": housing_use, "房屋年限": house_age_limit, "房权所属": house_ownership, "城市": city, "区/县": district,
         "镇/街道": town, "小区": resblock, "小区编号": resblock_id, "经度": longitude, "纬度": latitude}
    print(d)
    data = data.append(d, ignore_index=True)  # 总的datafram增加一行记录
    data_district = data_district.append(
        d, ignore_index=True)  # 当前区datafram增加一行记录
    return data, data_district


def main():
    """主函数 依次爬取所有区对应的所有镇/街道的房源
    """
    print('你要爬取的城市为：', city)
    data = pd.DataFrame()
    if not os.path.exists(path):
        os.makedirs(path)

    area_dic = get_areas()  # 当前市各区域字典
    print(area_dic)

    # 依次爬每一个区
    for district in area_dic:
        data_district = pd.DataFrame()  # 每爬完一个区重新初始化一个新的dataframe
        # 依次爬每一个镇/街道
        for town in area_dic[district]:
            # town_url="https://bj.lianjia.com/chengjiao/xidan/"
            town_url = area_dic[district][town]
            house_url_list = get_town_houses_url_list(town_url, town)

            # 爬每一个房源详细信息
            for house_url in house_url_list:
                try:
                    data, data_district = get_house_info(
                        house_url, district, town, data_district, data)
                except:
                    print('error')

        data_district.to_excel(path+"链家_"+city+"_"+district+"区.xlsx",
                               columns=columns)  # 每爬完一个区导出该区excel
    data.to_excel(path+"lianjia.xlsx", columns=columns)  # 爬完所有区导出总excel


main()
