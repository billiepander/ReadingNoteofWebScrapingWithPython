#coding:utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup
# 从一个wiki页面开始探寻所有的与之相关的页面


# 1：访问一个页面并得到相关页面的信息
html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html)
for link in bsObj.findAll("a"):
    if 'href' in link.attrs:
        print(link.attrs['href'])

# 经分析，发现并不是所有的结果都是相关页面的link，还有用于方便跳转的本页面不同位置的link
# 经过分析，发现相关页面link有以下相同点：
# • They reside within the div with the id set to bodyContent
# • The URLs do not contain semicolons
# • The URLs begin with /wiki/
import re
html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html)
for link in bsObj.find("div", {"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$")):
    if 'href' in link.attrs:
        print(link.attrs['href'])


# 运行一个完全的不停歇地挨个爬取相关页面的爬虫[注意，应该添加异常处理]
import random,datetime
random.seed(datetime.datetime.now())

def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html)
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$"))

links = getLinks("/wiki/Kevin_Bacon")
while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
    print(newArticle)
    links = getLinks(newArticle)


"""
    递归整站爬虫：每页有重复的页面，应当查重并且检验是否爬过
"""
pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen("http://en.wikipedia.org"+pageUrl)
    bsObj = BeautifulSoup(html)
    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                #We have encountered a new page
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)          #set的add方法
                getLinks(newPage)

getLinks("")


# 仅仅是跳来跳去并没有意义，尝试收集一些数据：
# • 所有的title都在h1->span标签下，并且此h1标签是唯一的
# • 所有正文在id为bodyContent的div标签下，如果仅仅想获得第一段，那用
#   div#mw-content-text →p 即可. 除了file page(如https://en.wikipedia.org/wiki/File:Orbit_of_274301_Wikipedia.svg),
#   他们并没有正文，以上都有效
# • Edit links 仅仅在文章页，如果他们生效，可在li#ca-edit tag, under li#ca-edit → span → a 中找到

pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen("http://en.wikipedia.org"+pageUrl)
    bsObj = BeautifulSoup(html)
    try:
        print(bsObj.h1.get_text())
        print(bsObj.find(id ="mw-content-text").findAll("p")[0])
        print(bsObj.find(id="ca-edit").find("span").find("a").attrs['href'])
    except AttributeError:
        print("This page is missing something! No worries though!")
    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                #We have encountered a new page
                newPage = link.attrs['href']
                print("----------------\n"+newPage)
                pages.add(newPage)
                getLinks(newPage)

getLinks("")







"""
    在不同网站之间爬
"""
pages = set()
random.seed(datetime.datetime.now())
#Retrieves a list of all Internal links found on a page
def getInternalLinks(bsObj, includeUrl):
    internalLinks = []
    #Finds all links that begin with a "/"
    for link in bsObj.findAll("a", href=re.compile("^(/|.*"+includeUrl+")")):
        if link.attrs['href'] is not None:
        if link.attrs['href'] not in internalLinks:
            internalLinks.append(link.attrs['href'])
    return internalLinks

#Retrieves a list of all external links found on a page
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    #Finds all links that start with "http" or "www" that do not contain the current URL
    for link in bsObj.findAll("a",href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def splitAddress(address):
    addressParts = address.replace("http://", "").split("/")
    return addressParts

def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html)
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    if len(externalLinks) == 0:
        internalLinks = getInternalLinks(startingPage)
        return getNextExternalLink(internalLinks[random.randint(0,len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]

def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink("http://oreilly.com")
    print("Random external link is: "+externalLink)
    followExternalOnly(externalLink)

followExternalOnly("http://oreilly.com")

# 从http://oreilly.com开始，随机跳后到达外部网络，输出：
# Random external link is: http://igniteshow.com/
# Random external link is: http://feeds.feedburner.com/oreilly/news
# Random external link is: http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=q319
# Random external link is: http://makerfaire.com/



# The nice thing about breaking up tasks into simple functions such as “find all external
# links on this page” is that the code can later be easily refactored to perform a different
# crawling task. For example, if our goal is to crawl an entire site for external links,




