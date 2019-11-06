#!/usr/bin/env python
# coding: utf-8
from bs4 import BeautifulSoup
import urllib.request as RequestLib
from string import Template

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
wiki_url = 'https://en.wikipedia.org/wiki/Herbert_A._Simon'
base = 'https://en.wikipedia.org'
req = RequestLib.Request(wiki_url, headers=headers)
html = RequestLib.urlopen(req).read()
bsObj = BeautifulSoup(html, 'html.parser')

title = bsObj.select('h1.firstHeading')[0].text

vcard = bsObj.select('table.vcard')[0]
rows = vcard.select('tr')
biography = [['People_Name', title], ['Wikipedia_url', wiki_url]]

extract_method = {
    'Citizenship': 'text',
    'Children': 'text',
    'Alma\xa0mater': 'a-list',
    'Known\xa0for': 'a-list',
    'Fields': 'a-list',
    'Institutions': 'a-list',
    'Doctoral advisor': 'a-list',
    'Other\xa0academic advisors': 'a-list',
    'Doctoral students': 'a-list',
    'Influences': 'a-list',
    'Influenced': 'a-list'
}

for tr in rows:
    if tr.th and tr.th.attrs.get('scope'):
        td = tr.td
        key = tr.th.text.strip()
        method = extract_method.get(key)
        val = ""
        if method == 'a-list':
            val = []
            for a in td.select('a'):
                if a.text.find('[') != -1:
                    continue
                val.append({ 'title': a.text, 'url': base+a.attrs['href'] })
        elif method == 'text':
            val = td.text
        elif key == 'Born':
            val = {
                'date': td.span.span.text,
                'place': td.select('div.birthplace')[0].text
            }
        elif key == 'Died':
            val = {
                'date': td.span.text,
                'place': td.select('div.deathplace')[0].text
            }
        elif key == 'Spouse(s)':
            val = []
            for d in td.select('div'):
                val.append({ 'name': d.text })
        elif key == 'Awards':
            val = []
            for li in td.div.ul.select('li'):
                val.append({
                    "title": li.a.text,
                    "url": base+li.a.attrs['href'],
                    'year': li.small.text[1:-1]
                })
            

        biography.append([key.replace('\xa0', ' '), val])
        
for e in biography:
    print(e[0], e[1])

class MyTemplate(Template):
    idpattern = r'[_a-zA-Z][_:.a-zA-Z0-9]*'

template = MyTemplate("""
# ${People_Name}
维基百科地址：[${People_Name}](${Wikipedia_url})
## 时间
### 生卒年月
${Born.date} - ${Died.date}
### 求学经历
${Alma_mater}
## 空间
### 学术领域
${Fields}
### 获奖情况
${Awards}
### 所属机构
${Institutions}
## 变量
### 主要成就
${Known_for}
### 合作关系

### 师承关系
#### 老师
${Doctoral_advisor}
${Other_academic_advisors}
#### 学生
${Doctoral_students}
""")

data = {}

for e in biography:
    b = e[0].replace(' ', '_')
    if type(e[1]) is list:
        v = ""
        for a in e[1]:
            if a.get('title'):
                v = v + '* [%s](%s)\n' % (a['title'], a['url'])
        data[b] = v
    elif type(e[1]) is dict:
        for k in e[1]:
            data[b+'.'+k] = e[1][k]
    else:
        data[b] = e[1]

print(data)
print(template.safe_substitute(data))