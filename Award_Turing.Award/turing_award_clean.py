#!/usr/bin/env python
# coding: utf-8
import csv
import json

url_csv = 'turing_award_page1.csv'

def process_bib(data):
    return data

def process_edu(data):
    return data

def process_exp(data):
    return data

def process_award(data):
    return data

def process_extra(data):
    return data

data = {}

with open(url_csv, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['name']
        if data.get(name) == None:
            bib = process_bib(row['bib'])
            left = process_exp(row['left'])
            data[row['name']] = {
                'name': name,
                'url': row['web-scraper-start-url'],
                'citation': row['citation'],
                'dl_link': row['dl_link-href'],
                'extra': process_extra(row['extra'])
            }
            if row.get('death'):
                data[name]['death'] = row['death']
        data[name]['extra'][row['title'].replace('\n','')] = row['title-href']
        print(data[row['name']])
        print(bib)
        print(left)
        break

#print(json.dumps(data))
#print(data.keys())
#print(len(data.keys()))
#print(data['Alan J Perlis'])
#print(json.dumps(data['Herbert ("Herb") Alexander Simon'], indent=4))
