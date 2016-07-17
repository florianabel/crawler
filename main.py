#!/usr/bin/python

import pymysql
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse


connection = pymysql.connect(host='XXX', port=1234, user='XXX', passwd='XXX', db='XXX')
cursor = connection.cursor()
for num in range(1,5):
    nextUrlQuery = "SELECT url FROM crawlList WHERE id = '%i'" %num
    cursor.execute(nextUrlQuery)
    data = cursor.fetchone()
    nextUrl = data[0]
    print (nextUrl)
    page = requests.get(nextUrl)
    content = BeautifulSoup(page.content, 'html.parser')
    urls = content.find_all('a')
    for url in urls:
        rawUrl = (url.get('href'))
        print (rawUrl)
        if "http" in rawUrl:
            stripUrl = urlparse(rawUrl)
            scheme = stripUrl.scheme
            netloc = stripUrl.netloc
            path = stripUrl.path
            basicUrl = scheme + "://" + netloc
            rawData = "INSERT INTO url(scheme, netloc, path) VALUES('%s','%s','%s')" % (scheme, netloc, path)
            cursor.execute(rawData)
            existQuery = "SELECT id FROM crawlList WHERE url = '%s'" % basicUrl
            cursor.execute(existQuery)
            id = cursor.fetchone()
            if id != None:
                increaseQuery = "UPDATE crawlList SET linkcount = linkcount + 1 WHERE id = '%s'" % id
                cursor.execute(increaseQuery)
            else:
                crawlList = "INSERT INTO crawlList(url) VALUES ('%s')" % basicUrl
                cursor.execute(crawlList)
        else:
            continue
cursor.execute("SELECT * FROM url")
connection.close()