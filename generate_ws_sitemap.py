#!/usr/bin/env python
# coding: utf-8
import json
import csv

sitemap = 'sitemap.json'
url_csv = 'url.csv'


with open(sitemap, 'r') as site:
    data = json.load(site)

data['startUrl'] = []

with open(url_csv, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data['startUrl'].append(row[2])

print(json.dumps(data))
