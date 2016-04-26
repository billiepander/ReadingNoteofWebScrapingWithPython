#coding:utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup

"""
    -------------------------------------------------媒体文件------------------------------------------------------------
两种方法保存媒体文件：
    1：保存其url
    2：下载下来

In Python 3.x, urllib.request.urlretrieve can be used to download files from any remote URL:
"""

** from urllib.request import urlretrieve **

html = urlopen("http://www.pythonscraping.com")
bsObj = BeautifulSoup(html)
imageLocation = bsObj.find("a", {"id": "logo"}).find("img")["src"]      #此地访问属性不太对吧？？不应该是.find('img').attrs['src']
** urlretrieve (imageLocation, "logo.jpg") **
# This downloads the logo from http://pythonscraping.com and stores it as logo.jpg in the same directory.


# 上面的方法只适用于下载单个已知文件类型的文件，下面是爬取页面内所有tag 的src属性的文件：

import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

downloadDirectory = "downloaded"
baseUrl = "http://pythonscraping.com"
def getAbsoluteURL(baseUrl, source):
    if source.startswith("http://www."):
        url = "http://"+source[11:]
    elif source.startswith("http://"):
        url = source
    elif source.startswith("www."):
        url = source[4:]
        url = "http://"+source
    else:
        url = baseUrl+"/"+source
    if baseUrl not in url:
        return None
    return url

def getDownloadPath(baseUrl, absoluteUrl, downloadDirectory):       # cleans and normalizes the URLs to get an absolute path for each download
    path = absoluteUrl.replace("www.", "")
    path = path.replace(baseUrl, "")
    path = downloadDirectory+path
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    return path

html = urlopen("http://www.pythonscraping.com")
bsObj = BeautifulSoup(html)
downloadList = bsObj.findAll(src=True)         # lambda to select all tags on the front page that have the src attribute

for download in downloadList:
    fileUrl = getAbsoluteURL(baseUrl, download["src"])
    if fileUrl is not None:
        print(fileUrl)

urlretrieve(fileUrl, getDownloadPath(baseUrl, fileUrl, downloadDirectory))

# 注，以上代码很危险，不要这样随意的下载文件，极有可能出现恶意文件破坏电脑


"""
    -------------------------------------------保存到MySQL--------------------------------------------------------------
    MySQL (officially pronounced “My es-kew-el,” although many say, “My Sequel”)

    Mysql默认不支持unicode，但是可以开启支持，不过会增加数据库大小：
        ALTER DATABASE scraping CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
        ALTER TABLE pages CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        ALTER TABLE pages CHANGE title title VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        ALTER TABLE pages CHANGE content content VARCHAR(10000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    These four lines change the following: the default character set for the database, for the table,
    and for both of the two columns, from utf8mb4 (still technically Unicode,
    but with notoriously terrible support for most Unicode characters) to utf8mb4_unicode_ci.

"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import pymysql
conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock',
                       user='root', passwd=None, db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE scraping")
random.seed(datetime.datetime.now())

def store(title, content):
    cur.execute("INSERT INTO pages (title, content) VALUES (\"%s\",\"%s\")", (title, content))
    cur.connection.commit()

def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html)
    title = bsObj.find("h1").find("span").get_text()
    content = bsObj.find("div", {"id":"mw-content-text"}).find("p").get_text()
    store(title, content)
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$"))

links = getLinks("/wiki/Kevin_Bacon")
try:
    while len(links) > 0:
        newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
        print(newArticle)
        links = getLinks(newArticle)
finally:
    cur.close()
    conn.close()


#
# 纪录six degrees of wikipedia的link过程
# 先建两张表：
# CREATE TABLE `wikipedia`.`pages` (
#     `id` INT NOT NULL AUTO_INCREMENT,
#     `url` VARCHAR(255) NOT NULL,
#     `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY (`id`));
#
# CREATE TABLE `wikipedia`.`links` (
#     `id` INT NOT NULL AUTO_INCREMENT,
#     `fromPageId` INT NULL,
#     `toPageId` INT NULL,
#     `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY (`id`));

# The following will store all pages on Wikipedia that have a “Bacon number” (the
# number of links between it and the page for Kevin Bacon, inclusive) of 6 or less
conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd=None, db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE wikipedia")
def insertPageIfNotExists(url):
    cur.execute("SELECT * FROM pages WHERE url = %s", (url))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO pages (url) VALUES (%s)", (url))
        conn.commit()
        return cur.lastrowid
    else:
        return cur.fetchone()[0]

def insertLink(fromPageId, toPageId):
    cur.execute("SELECT * FROM links WHERE fromPageId = %s AND toPageId = %s",(int(fromPageId), int(toPageId)))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO links (fromPageId, toPageId) VALUES (%s, %s)",(int(fromPageId), int(toPageId)))
        conn.commit()

pages = set()
def getLinks(pageUrl, recursionLevel):
    global pages
    if recursionLevel > 4:
        return;
    pageId = insertPageIfNotExists(pageUrl)
    html = urlopen("http://en.wikipedia.org"+pageUrl)
    bsObj = BeautifulSoup(html)
    for link in bsObj.findAll("a",href=re.compile("^(/wiki/)((?!:).)*$")):
        insertLink(pageId,insertPageIfNotExists(link.attrs['href']))
        if link.attrs['href'] not in pages:
            #We have encountered a new page, add it and search it for links
            newPage = link.attrs['href']
            pages.add(newPage)
            getLinks(newPage, recursionLevel+1)

getLinks("/wiki/Kevin_Bacon", 0)
cur.close()
conn.close()


"""
    -------------------------------------------------Email--------------------------------------------------------------

"""
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
def sendMail(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "christmas_alerts@pythonscraping.com"
    msg['To'] = "ryan@pythonscraping.com"
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

bsObj = BeautifulSoup(urlopen("https://isitchristmas.com/"))
while(bsObj.find("a", {"id":"answer"}).attrs['title'] == "NO"):
    print("It is not Christmas yet.")
    time.sleep(3600)

bsObj = BeautifulSoup(urlopen("https://isitchristmas.com/"))
sendMail("It's Christmas!","According to http://itischristmas.com, it is Christmas!")