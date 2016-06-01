#!/usr/bin/python

import pymysql
import requests
import json
from bs4 import BeautifulSoup

page = requests.get('https://news.ycombinator.com/')
content = BeautifulSoup(page.content, 'html.parser')
urls = content.find_all('a')
connection = pymysql.connect(host='florianabel.com', port=3306, user='d021ff24', passwd='crawler', db='d021ff24')
cursor = connection.cursor()
for url in urls:
    link = (url.get('href'))
    string = "INSERT INTO url(url) VALUES('%s')" % link
    print (string)
    cursor.execute(string)



cursor.execute("SELECT * FROM url")
connection.close()
