import json

#with open('./website/turing_award.json', 'r') as jsonFile:
with open('./website/website/turing_award.json', 'r') as jsonFile:
    data = json.load(jsonFile)

def get_by_year(year):
    for e in data:
        if data[e]['year'] == year:
            return formalize_keys(data[e])
    return None

def formalize_keys(data):
    res = {}
    for k in data:
        res[k.replace('-', '_')] = data[k]

    return res