# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

'''
1. install beautifulsoup4 and requests libraries
2. change data source url if needed
3. default output in desktop
'''

import requests
import csv
import os
import datetime

# data scource url
url = 'https://lab.isaaclin.cn/nCoV/api/area?latest=1'

# output file path
pre_filename = os.path.join(os.path.expanduser("~"), 'Desktop') + '/dxy_data_'

# get html content
r = requests.get(url)
response_dict = r.json()

overseas_dict = []
china_dict = []

for i in response_dict['results']:
    if i['countryName'] != '中国':
        overseas_dict.append(i)
    else:
        china_dict.append(i)

china_tags = ['locationId', 'continentName', 'continentEnglishName', 'countryName', 'countryEnglishName', 'provinceName', 'provinceShortName', 'provinceEnglishName', 'currentConfirmedCount', 'confirmedCount', 'suspectedCount', 'curedCount', 'deadCount', 'comment', 'updateTime']
city_tags = ['cityName', 'currentConfirmedCount', 'confirmedCount', 'suspectedCount', 'curedCount', 'deadCount', 'locationId', 'cityEnglishName']
overseas_tags = ['locationId', 'continentName', 'continentEnglishName', 'countryName', 'countryEnglishName', 'provinceName', 'provinceShortName', 'provinceEnglishName', 'currentConfirmedCount', 'confirmedCount', 'suspectedCount', 'curedCount', 'deadCount', 'updateTime']

# to china
with open(pre_filename + 'china_' + str(datetime.date.today()) + '.csv', 'w', encoding='utf_8_sig') as f:
    # load csv writer
    csv_writer = csv.writer(f)
    csv_writer.writerow(china_tags)

    for i in china_dict:
        record = []
        for t in china_tags:
            record.append(i[t])
        csv_writer.writerow(record)

# to cities
with open(pre_filename + 'cities_' + str(datetime.date.today()) + '.csv', 'w', encoding='utf_8_sig') as f:
    # load csv writer
    csv_writer = csv.writer(f)
    csv_writer.writerow(city_tags)

    for i in china_dict:
        # write province first
        record = []
        record.append(i['provinceName'])
        for k in city_tags[1:-1]:
            record.append(i[k])
        record.append(i['provinceEnglishName'])
        csv_writer.writerow(record)

        # write cities last
        for j in i['cities']:
            record = []
            if j['cityName'] == '境外输入人员':
                for t in city_tags[:-1]:
                    record.append(j[t])
                record.append('')
            else:
                for t in city_tags:
                    record.append(j[t])
            csv_writer.writerow(record)
        csv_writer.writerow([])

# to overseas
with open(pre_filename + 'overseas_' + str(datetime.date.today()) + '.csv', 'w', encoding='utf_8_sig') as f:
    # load csv writer
    csv_writer = csv.writer(f)
    csv_writer.writerow(overseas_tags)

    for i in overseas_dict:
        record = []
        for t in overseas_tags:
            record.append(i[t])
        csv_writer.writerow(record)

print('Done!')
