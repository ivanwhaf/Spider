import requests  # install
from bs4 import BeautifulSoup as bs  # install
from selenium import webdriver  # install
import time
import json
import pymysql  # install
from openpyxl import Workbook, load_workbook  # install

list_url = 'https://meishi.meituan.com/i/api/channel/deal/list'  # 查询list api
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'Host': 'meishi.meituan.com',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://meishi.meituan.com/i/?ci=55'
}

headers_poi = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'Host': 'meishi.meituan.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://meishi.meituan.com/i/?ci=55'
}

data = {
    'app': "",
    'areaId': 273,
    'cateId': 1,
    'deal_attr_23': "",
    'deal_attr_24': "",
    'deal_attr_25': "",
    'limit': 50,
    'lineId': 0,
    'offset': 0,
    'optimusCode': 10,
    'originUrl': "http://meishi.meituan.com/i/?ci=55",
    'partner': 126,
    'platform': 3,
    'poi_attr_20033': "",
    'poi_attr_20043': "",
    'riskLevel': 1,
    'sort': "default",
    'stationId': 0,
    'uuid': "3e248bc8-92ed-466e-9c31-767a2f6bb3ba",
    'version': "8.2.0"
}


data_dish_tag = {
    'app': "",
    'optimusCode': 10,
    'originUrl': "http://meishi.meituan.com/i/poi/64279557?ct_poi=264437932482467856512130747848741313150_a64279557_c1_e8325032252055707285_nareaid273",
    'partner': 126,
    'platform': 3,
    'poiId': 64279557,
    'riskLevel': 1,
    'uuid': "166640c9-cf6b-48c6-a5c2-6d29ebe67ed1",
    'version': "8.2.0"
}

c_g = {}


def get_cookies(ci):
    options = webdriver.ChromeOptions()
    # options.add_argument('--start-maximized')
    driver = webdriver.Chrome(
        executable_path='C:\\Users\\Ivan\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe', chrome_options=options)
    driver.get(url='https://meishi.meituan.com/i/?ci='+ci)
    time.sleep(1)
    driver.find_element_by_class_name("poi-info").click()
    time.sleep(2)
    cookies = driver.get_cookies()
    c = {}
    for line in cookies:
        c[line['name']] = line['value']
    return c


def get_dish(poiId, uuid):
    data_dish_tag['poiId'] = poiId
    data_dish_tag['uuid'] = uuid
    ret = ''
    r = requests.post('http://meishi.meituan.com/i/api/dish/poi',
                      data=data_dish_tag, headers=headers)
    try:
        j = json.loads(r.text)
    except:
        return ret
    try:
        for l in j['data']['list']:
            ret = ret+l['name']+' '
    except:
        return ret
    return ret


def get_tag(poiId, uuid):
    data_dish_tag['poiId'] = poiId
    data_dish_tag['uuid'] = uuid
    r = requests.post('http://meishi.meituan.com/i/api/comment/tag/poi',
                      data=data_dish_tag, headers=headers)
    ret = ''
    try:
        j = json.loads(r.text)
    except:
        return ret
    try:
        for l in j['data']['list']:
            ret = ret+l['tag']+' '
    except:
        return ret
    return ret


def get_smartTags(p):
    ret = ''
    try:
        smartTags = p['smartTags']
    except:
        return ret
    for st in smartTags:
        ret = ret+st['text']['content']+' '
    return ret


def get_extraService(p):
    ret = ''
    try:
        extraService = p['extraServiceTags']
    except:
        return ret
    for es in extraService:
        ret = ret+es['text']['content']+' '
    return ret


def get_preferentialInfo(p):
    ret = ''
    try:
        preferentialInfo = p['preferentialInfo']
    except:
        return ret
    entries = preferentialInfo['maidan']['entries']
    for e in entries:
        if e['discountColor'] == '#38c2aa':
            ret = ret+e['promotion']+e['content']+' '
        else:
            ret = ret+e['content']+' '
    return ret


def get_detail(poiid, ct_poi, c):
    '''options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver=webdriver.Chrome(executable_path='C:\\Users\\Ivan\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe',chrome_options=options)
    driver.get(url='https://meishi.meituan.com/i/poi/'+poiid+'?ct_poi='+ct_poi)
    cookies=driver.get_cookies()
    c={}
    for line in cookies:
            c[line['name']]=line['value']'''
    r = requests.get('https://meishi.meituan.com/i/poi/' +
                     poiid+'?ct_poi='+ct_poi, headers=headers_poi, cookies=c)
    soup = bs(r.text, 'html.parser')
    # print(soup)

    cr = soup.find_all('script', crossorigin='anonymous')[7].string
    # print(cr)
    cr = cr.split('=')[1:]
    cr = ''.join(cr)
    d = cr.split(' ')[1:]
    d = ''.join(d)
    d = d.split(';')[:-1]
    d = ''.join(d)

    j = json.loads(d)
    info = j['poiInfo']
    addr = info['addr']
    phone = info['phone']
    openInfo = info['openInfo'].replace('\n', ' ')
    # print(addr,phone,openInfo)
    return addr, phone, openInfo


def judge_exist_poi(poiid):
    conn = pymysql.connect('localhost', 'root', '111111', 'meituan')
    cursor = conn.cursor()
    sql = 'SELECT name FROM poi WHERE poiid="{}"'.format(poiid)
    cursor.execute(sql)
    row = cursor.fetchone()
    if row == None:
        return 0
    else:
        print(row[0]+'已存在！')
        return 1


def store_poi_data(name, cateName, areaName, avgScore, avgPrice, smartTags, extraService, preferentialInfo, dish, tag, addr, phone, openInfo, lat, lng, poiid, ctPoi):
    # if judge_exist_poi(poiid):
    # return
    conn = pymysql.connect('localhost', 'root', '111111', 'meituan')
    cursor = conn.cursor()
    sql = 'INSERT INTO poi(name,cateName,areaName,avgScore,avgPrice,smartTags,extraService,preferentialInfo,dish,tag,addr,phone,openInfo,lat,lng,poiid,ctPoi) \
	VALUES("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(name, cateName, areaName, avgScore, avgPrice, smartTags, extraService, preferentialInfo, dish, tag, addr, phone, openInfo, lat, lng, poiid, ctPoi)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def get_poi(ci, areaId, cateId, lineId):
    c_g = get_cookies(ci=ci)
    data['uuid'] = c_g['uuid']
    data['areaId'] = areaId  # 区域id
    data['cateId'] = cateId  # 类别id
    data['lineId'] = areaId  # 地铁线id
    offset = 0
    num = 1
    while(offset < 1000):
        data['offset'] = offset
        r = requests.post(url=list_url, data=data,
                          headers=headers, cookies=c_g)
        j = json.loads(r.text)
        try:
            totalCount = j['data']['poiList']['totalCount']
        except:
            break
        poiInfos = j['data']['poiList']['poiInfos']
        for p in poiInfos:
            name = p['name']
            cateName = p['cateName']
            areaName = p['areaName']
            avgScore = p['avgScore']
            avgPrice = p['avgPrice']
            poiid = p['poiid']
            lat = p['lat']
            lng = p['lng']
            ctPoi = p['ctPoi']
            if judge_exist_poi(poiid):
                continue

            smartTags = get_smartTags(p)
            extraService = get_extraService(p)
            preferentialInfo = get_preferentialInfo(p)
            dish = get_dish(poiid, c_g['uuid'])
            tag = get_tag(poiid, c_g['uuid'])
            addr, phone, openInfo = '', '', ''
            '''try:
				addr,phone,openInfo=get_detail(poiid,ctPoi,c_g)
			except:
				c_g=get_cookies(ci='55')
				data['uuid']=c_g['uuid']
				continue'''
            print(str(num), name, cateName, avgPrice, avgScore, smartTags)
            try:
                store_poi_data(name, cateName, areaName, avgScore, avgPrice, smartTags, extraService,
                               preferentialInfo, dish, tag, addr, phone, openInfo, lat, lng, poiid, ctPoi)
            except:
                continue
            num = num+1
        offset = offset+50
        time.sleep(2)


def get_areaList(ci):
    r = requests.get('https://meishi.meituan.com/i/?ci='+ci, headers=headers)
    soup = bs(r.text, 'html.parser')
    cr = soup.find_all('script', crossorigin='anonymous')[7].string
    cr = cr.split('=')[1:]
    cr = ''.join(cr)
    d = cr.split(' ')[1:]
    d = ''.join(d)
    d = d.split(';')[:-1]
    d = ''.join(d)
    j = json.loads(d)
    areaList = j['navBarData']['areaList']
    return areaList


def get_areaObj(ci):
    r = requests.get('https://meishi.meituan.com/i/?ci='+ci, headers=headers)
    soup = bs(r.text, 'html.parser')
    # print(soup)
    cr = soup.find_all('script', crossorigin='anonymous')[7].string
    cr = cr.split('=')[1:]
    cr = ''.join(cr)
    d = cr.split(' ')[1:]
    d = ''.join(d)
    d = d.split(';')[:-1]
    d = ''.join(d)
    j = json.loads(d)
    areaObj = j['navBarData']['areaObj']
    return areaObj


def get_lineObj(ci):
    r = requests.get('https://meishi.meituan.com/i/?ci='+ci, headers=headers)
    soup = bs(r.text, 'html.parser')
    # print(soup)
    cr = soup.find_all('script', crossorigin='anonymous')[7].string
    cr = cr.split('=')[1:]
    cr = ''.join(cr)
    d = cr.split(' ')[1:]
    d = ''.join(d)
    d = d.split(';')[:-1]
    d = ''.join(d)
    j = json.loads(d)
    lineObj = j['navBarData']['lineObj']
    return lineObj


def export_excel():
    a = ['name', 'cateName', 'areaName', 'avgScore', 'avgPrice', 'smartTags',
         'extraService', 'preferentialInfo', 'dish', 'tag', 'lat', 'lng', 'poiid', 'ctPoi']
    wb = Workbook()
    ws = wb.get_sheet_by_name('Sheet')
    ws.append(a)
    conn = pymysql.connect('localhost', 'root', '111111', 'meituan')
    cursor = conn.cursor()
    sql = 'SELECT name,cateName,areaName,avgScore,avgPrice,smartTags,extraService,preferentialInfo,dish,tag,lat,lng,poiid,ctPoi FROM poi'
    cursor.execute(sql)
    cursor.close()
    conn.close()
    for row in cursor.fetchall():
        try:
            ws.append(list(row))
        except:
            print('出错！')
    wb.save('meituan.xlsx')


def main():
    areaObj = get_areaObj(ci='55')
    lineObj = get_lineObj(ci='55')
    '''for key in areaObj:
		for a in areaObj[key]:
			id=a['id']
			count=a['count']
			name=a['name']
			if count!="" and count!=0:
				print('-----------------------id-----------------------'+str(id)+'-----------------name----------------'+str(name))
				get_poi(ci='55',areaId=id,cateId=1,lineId=0)'''

    for key in lineObj:
        for a in lineObj[key]:
            id = a['id']
            count = a['count']
            name = a['name']
            if count != "" and count != 0:
                print('-----------------------id-----------------------' +
                      str(id)+'-----------------name----------------'+str(name))
                get_poi(ci='55', areaId=0, cateId=1, lineId=id)


if __name__ == '__main__':
    main()
    # export_excel()
