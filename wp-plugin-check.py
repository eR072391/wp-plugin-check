import requests
from bs4 import BeautifulSoup
import re

url = input("Word Press URL: ")

if url[-1] != '/':
    url = url + '/'

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100'}

#headers={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1'}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

elems = soup.find_all('script')

target = 'wp-content/plugins'

path = ""
for i in elems:
    data = str(i)
    if target in data:
        hit = re.findall(url+r'(.+?)'+target,data)
        if 0 == len(hit):
            break
        path = hit[0]

target = 'wp-content/plugins/'
plugin_list = []

for i in elems:
    if not i.get('src') is None:
        if url+path+target in i.get('src'):
            idx = i.get('src').find(target)
            data = i.get('src')[idx+len(target):]
            idx = data.find('/')
            data = data[:idx]
            plugin_list.append(data)

elems = soup.find_all("link")

for i in elems:
    if url+path+target in i.get('href'):
        idx = i.get('href').find(target)
        data = i.get('href')[idx+len(target):]
        idx = data.find('/')
        data = data[:idx]
        plugin_list.append(data)



plugin_list = set(plugin_list)


print("*** Plugin List ***")
for plugin in plugin_list:
    print(plugin," ",end="")
    res = requests.get(url+path+target+plugin+'/readme.txt')
    if 200 != res.status_code:
        print("?")
    if 'Stable tag:' in res.text:
        idx = res.text.find('Stable tag:')
        data = res.text[idx+11:idx+18]
        print(data.replace('\n',''))
    else:
        print("?")
