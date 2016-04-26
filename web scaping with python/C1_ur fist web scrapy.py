#coding:utf-8

from urllib.request import urlopen
# urllib是python3中的模块，并且有urllib.request,urllib.parse,urllib.error好几个子模块,区别于py2.x中的urllib2，
html = urlopen("http://pythonscraping.com/pages/page1.html")
print(html.read())
# 会得到此网址的全部html代码,不同之处在于浏览器若遇到如图片的html时他还会回到服务器继续请求，但是python代码是不会的。


# BeautifulSoup来自爱丽丝梦游仙境中的一首诗，其可帮助复原bad html并且返回XML结构。
from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com/pages/page1.html")
** bsObj = BeautifulSoup(html.read()) **
** print(bsObj.h1) **         #注意此地！直接访问html标签了！！
# 输出：<h1>An Interesting Title</h1>
# 实际上，BS可以嵌套使用，甚至是跳跃的嵌套使用。下面的表达都和bsObj.h1等效:
# bsObj.html.body.h1
# bsObj.body.h1
# bsObj.html.h1


# 建立稳定的连接:
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
def getTitle(url):
    try:
        html = urlopen(url)     #有两种情况: 1：服务器不在了(xxx.com)，此时返回None
                                #           2：此路径不在(404,500...),此时抛出HttpError异常
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read())      #如果返回的html为None，那么bsObj就是None
        title = bsObj.body.h1                   #如果访问的标签没有，返回None；但是如果此时bsObj为None再如此访问就会抛出AttributeError
    except AttributeError as e:
        return None
    return title

title = getTitle("http://www.pythonscraping.com/pages/page1.html")
if title == None:
    print("Title could not be found")
else:
    print(title)