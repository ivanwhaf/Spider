import requests
import json

url = 'http://dsfc.njupt.edu.cn/dsgl/nocontrol/college/dsfc.htm?pageAction=queryDsxm'
url2 = 'http://dsfc.njupt.edu.cn/dsgl/nocontrol/college/dsfcxq.htm'
params = {'dssx': 3}

r = requests.post(url, params)
lst = json.loads(r.text)
dzxx = lst[2]
# print(dzxx)s
dsfcEjxkDtos = dzxx['dsfcEjxkDtos']
yxDto = dsfcEjxkDtos[0]['yxDto']
dsDto = []
for xy in yxDto:
    if xy['yxMc'] == '计算机学院':
        dsDto = xy['dsDto']
        # print(xy['dsDto'])
        break

fail = []
for ds in dsDto:
    dsgh = ds['dsgh']
    dsxm = ds['dsxm']
    dsxm = dsxm.replace('*', '')
    try:
        r = requests.post(url2, {'zgh': int(dsgh)}, timeout=4)
    except:
        fail.append(dsxm)
        continue

    with open('f:/ds/'+dsxm+'.html', 'w', encoding='utf-8') as f:
        f.write(r.text)
        print(dsxm)

print(fail)
