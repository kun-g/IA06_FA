#!/usr/bin/env python
# coding: utf-8
# coding=utf-8

from bs4 import BeautifulSoup
from bs4 import NavigableString
import urllib.request as RequestLib
from string import Template
import re
import sys


def fetch(wiki_url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = RequestLib.Request(wiki_url, headers=headers)
    html = RequestLib.urlopen(req).read()
    return BeautifulSoup(html, 'html.parser')


def extract_birth(bsObj):
    bday = bsObj.select('span.bday')
    birthplace = bsObj.select('div.birthplace')
    if bday:
        bday = bday[0].text
    else:
        bday = bsObj.text
        
    if birthplace:
        birthplace = birthplace[0].text
    else:
        birthplace = None

    return {
        'day': bday,
        'place': birthplace
    }


def extract_death(bsObj):
    dday = bsObj.select('span')
    place = bsObj.select('div.deathplace')
    if dday:
        dday = dday[0].text
    else:
        bday = bsObj.text
        
    if place:
        place = place[0].text
    else:
        place = None

    return {
        'day': dday,
        'place': place
    }


def extract_awards(bsObj, base):
    val = []
    if bsObj.div:
        for li in bsObj.div.ul.select('li'):
            val.append({
                "title": li.a.text,
                "url": base+li.a.attrs['href'],
                'year': li.small.text[1:-1]
            })
    elif len(bsObj.text.split(',')) > 1:
        for e in bsObj.text.split(','):
            v = { 'title': e.strip() }
            year = re.search('\((\d{1,4})\)', e.strip())
            if year:
                v['year'] = year.groups()[0]
            val.append(v)
    else:
        v = ''
        year = None
        for e in bsObj.contents:
            if isinstance(e, NavigableString):
                year = re.search('\((\d{1,4})\)', e.strip())
                if year:
                    year = year.groups()[0]
            elif e.name == 'br':
                v = { 'title': v.strip() }
                if year:
                    v['year'] = year
                val.append(v)
                v = ''
            else:
                v += e.text

    return val

def parse_vcard(vcard):
    rows = vcard.select('tr')
    base = 'https://en.wikipedia.org'

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
    
    name = rows[0].select('div.fn')[0].text
    data = {'name': name}

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
                val = extract_birth(td)
            elif key == 'Died':
                val = extract_death(td)
            elif key == 'Spouse(s)':
                val = []
                for d in td.select('div'):
                    val.append({ 'name': d.text })
            elif key == 'Awards':
                val = extract_awards(td, base)
            else:
                val = td

            data[key.replace('\xa0', ' ')] = val

    return data


def get_people(wiki_url):
    bsObj = fetch(wiki_url)
    title = bsObj.select('h1.firstHeading')[0].text
    biography = [['People_Name', title], ['Wikipedia_url', wiki_url]]

    vcard = parse_vcard(bsObj.select('table.vcard')[0])
    vcard['wiki_url'] = wiki_url
    return vcard


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

def render_md(biography):
    data = {}

    for k in biography:
        e = biography[k]
        k = k.replace(' ', '_')
        
        if type(e) is list:
            v = ""
            for a in e:
                if a.get('title'):
                    v = v + '* [%s](%s)\n' % (a['title'], a['url'])
            data[k] = v
        elif type(e) is dict:
            for l in e:
                data[l+'.'+l] = e[l]
        else:
            data[k] = e
    return template.safe_substitute(data)


#simon = get_people('https://en.wikipedia.org/wiki/Herbert_A._Simon')
#burt = get_people('https://en.wikipedia.org/wiki/Ronald_Stuart_Burt')
#kaneman = get_people('https://en.wikipedia.org/wiki/Daniel_Kahneman')
#mccarth = get_people('https://en.wikipedia.org/wiki/John_McCarthy_(computer_scientist)')
#
#people = [simon, burt, kaneman, mccarth]
#ignore = ['Citizenship', 'Nationality', 'Born', 'Died', 'Institutions', 'Doctoral students', 'Fields', 'Known for', 
#          'wiki_url', 'Website',
#          'Doctoral advisor', 'name', 'Awards', 'Thesis',
#
#          'Alma mater', 'Education', 'Residence',
#          'Other academic advisors', 'Influenced', 'Influences', 
#
#          'Spouse(s)', 'Children']
#
#for main in people:
#    for k in main.keys():
#        if k in ignore:
#            continue
#        for p in people:
#            print(p['name'], k, p.get(k))

#if len(sys.argv) < 2:
#    print('usage: wikipedia.py [url]')
#    exit()
#wiki_url = sys.argv[1]
#print(wiki_url)
#data = get_people(wiki_url)
#print(render_md(data).encode('utf-8'))
