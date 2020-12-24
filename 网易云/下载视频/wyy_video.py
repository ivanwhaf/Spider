import requests
import os

url="http://vodkgeyttp8.vod.126.net/cloudmusic/IiQwMDEwI2NiIDEzICZgIA==/mv/5402100/a2e1f273804487f86650f8d9ae4f57e4.mp4?wsSecret=eedd82630e61bc2b63888cd6be1bd193&wsTime=1539530261"
r=requests.get(url)

with open("1.mp4",'wb') as f:
	f.write(r.content)

