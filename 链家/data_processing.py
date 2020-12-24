import os
import re
import json
import operator
import pandas as pd


path = "链家/"


def data_analyze():
    files = os.listdir(path)  # 遍历每一个文件

    date_dic = {}  # 日期
    district_dic = {}  # 区
    price_dic = {}  # 价格
    resblock_dic = {}  # 小区
    price_per_square_dis_dic = {}  # 区平均每平米单价

    # 初始化日期
    for i in range(1, 10):
        date_dic['0'+str(i)] = 0
    date_dic['10'] = 0
    date_dic['11'] = 0
    date_dic['12'] = 0

    # 初始化价格区间
    price_dic['0-50'] = 0
    price_dic['50-100'] = 0
    price_dic['100-150'] = 0
    price_dic['150-200'] = 0
    price_dic['200-250'] = 0
    price_dic['250-300'] = 0
    price_dic['300-350'] = 0
    price_dic['350-400'] = 0
    price_dic['400-450'] = 0
    price_dic['450-500'] = 0
    price_dic['>500'] = 0

    # 初始化建筑面积区间
    area_dic = {}
    area_dic['0-30'] = 0
    area_dic['30-50'] = 0
    area_dic['50-70'] = 0
    area_dic['70-90'] = 0
    area_dic['90-110'] = 0
    area_dic['110-130'] = 0
    area_dic['130-150'] = 0
    area_dic['>150'] = 0

    # 读文件
    for file_ in files:
        df = pd.read_excel(path+file_)

        # 统计面积区间
        area = df["建筑面积"].tolist()
        for a in area:
            a = int(a)
            if a < 30:
                area_dic['0-30'] = area_dic['0-30']+1
            elif a >= 30 and a < 50:
                area_dic['30-50'] = area_dic['30-50']+1
            elif a >= 50 and a < 70:
                area_dic['50-70'] = area_dic['50-70']+1
            elif a >= 70 and a < 90:
                area_dic['70-90'] = area_dic['70-90']+1
            elif a >= 90 and a < 110:
                area_dic['90-110'] = area_dic['90-110']+1
            elif a >= 110 and a < 130:
                area_dic['110-130'] = area_dic['110-130']+1
            elif a >= 130 and a < 150:
                area_dic['130-150'] = area_dic['130-150']+1
            elif a >= 150:
                area_dic['>150'] = area_dic['>150']+1

        # 统计日期区间
        date = df["成交日期"].tolist()
        for d in date:
            month = d.split("-")[1]
            date_dic[month] = date_dic[month]+1

        # 统计各区房源数量
        district = df["区/县"].tolist()
        for d in district:
            if d in district_dic:
                district_dic[d] = district_dic[d]+1
            else:
                district_dic[d] = 1

        # 统计成交价区间
        prices = df["成交价格（万）"].tolist()
        for price in prices:
            price = int(price)
            if price < 50:
                price_dic['0-50'] = price_dic['0-50']+1
            elif (price >= 50 and price < 100):
                price_dic['50-100'] = price_dic['50-100']+1
            elif (price >= 100 and price < 150):
                price_dic['100-150'] = price_dic['100-150']+1
            elif (price >= 150 and price < 200):
                price_dic['150-200'] = price_dic['150-200']+1
            elif (price >= 200 and price < 250):
                price_dic['200-250'] = price_dic['200-250']+1
            elif (price >= 250 and price < 300):
                price_dic['250-300'] = price_dic['250-300']+1
            elif (price >= 300 and price < 350):
                price_dic['300-350'] = price_dic['300-350']+1
            elif (price >= 350 and price < 400):
                price_dic['350-400'] = price_dic['350-400']+1
            elif (price >= 400 and price < 450):
                price_dic['400-450'] = price_dic['400-450']+1
            elif (price >= 450 and price < 500):
                price_dic['450-500'] = price_dic['450-500']+1
            elif price >= 500:
                price_dic['>500'] = price_dic['>500']+1

        # 构造price_per_square_dis_dic字典
        for index, row in df.iterrows():
            # print(row['名称'])
            price_per_square = row['每平米单价（元）']
            district = row['区/县']
            year = row['成交日期'].split("-")[0]

            if district not in price_per_square_dis_dic:
                price_per_square_dis_dic[district] = {}
                price_per_square_dis_dic[district][year] = []
                price_per_square_dis_dic[district][year].append(
                    price_per_square)
            else:
                if year not in price_per_square_dis_dic[district]:
                    price_per_square_dis_dic[district][year] = []
                    price_per_square_dis_dic[district][year].append(
                        price_per_square)
                else:
                    price_per_square_dis_dic[district][year].append(
                        price_per_square)

        # 统计小区成交数量
        resblock = df['小区'].tolist()
        for r in resblock:
            if r not in resblock_dic:
                resblock_dic[r] = 1
            else:
                resblock_dic[r] = resblock_dic[r]+1

    # 统计每个区几年来成交价均价
    for dis in price_per_square_dis_dic:
        for year in price_per_square_dis_dic[dis]:
            sum_ = 0
            l = len(price_per_square_dis_dic[dis][year])
            for p in price_per_square_dis_dic[dis][year]:
                sum_ = sum_+int(p)
            price_per_square_dis_dic[dis][year] = int(sum_/l)

    # 小区按成交量从大到小排序
    resblock_lis = sorted(resblock_dic.items(),
                          key=operator.itemgetter(1), reverse=True)

    print(date_dic)
    print(district_dic)
    print(price_dic)
    print(price_per_square_dis_dic)
    print(area_dic)
    print(resblock_lis)

    rdic = {}
    rdic['date'] = date_dic
    rdic['district'] = district_dic
    rdic['price'] = price_dic
    rdic['price_per_square_dis'] = price_per_square_dis_dic
    rdic['area'] = area_dic
    rdic['resblock'] = resblock_lis[0:30]

    # 写入json文件
    with open('data.json', 'w') as f:
        json.dump(rdic, f)


data_analyze()
