#coding:utf-8
"""
    ------------------------------使用API（application programming interface）--------------------------------------
    需要区别的是API指的是程序接口，但是在这里我们主要讨论网络应用接口，也就是直接通过其来访问服务器并且做相应操作(返回数据，或者对数据库进行操作).

    来看一下除了GET与POST外两个常用的HTTP请求方式：
        PUT：常用于更新数据，比如通过post创建了一个user后，通过put请求改变某个用户的邮箱。
        DELETE：用于删除东西，但是基本都是内部API而不作为Public API。
                如http://myapi.com/user/23表明删除ID为23的用户

    下面将讲三个网站提供的API
"""
# -----------------------------------Echo Nest----------------------------------------------------
# The Echo Nest relies on automated intelligence and information scraped from blogs and news articles
# in order to categorize musical artists, songs, and albums.and its total free.

获取艺人monty python的ID
http://developer.echonest.com/api/v4/artist/search?api_key=<your apikey>&name=monty%20python
# 返回：
# {"response": {"status": {"version": "4.2", "code": 0, "message": "Success"},
#               "artists": [{"id": "AR5HF791187B9ABAF4", "name": "Monty Python"},
#                           {"id": "ARWCIDE13925F19A33", "name": "Monty Python's SPAMALOT"},
#                           {"id": "ARVPRCC12FE0862033", "name": "Monty Python's Graham Chapman"}]
#               }
#  }

使用艺人ID获取其歌曲:
http://developer.echonest.com/api/v4/artist/songs?api_key=<your api key>&id=AR5HF791187B9ABAF4&format=json&start=0&results=10
# 返回：
# {"response": {"status": {"version": "4.2", "code": 0, "message": "Success"},
# "start": 0, "total": 476, "songs": [{"id": "SORDAUE12AF72AC547", "title":"Neville Shunt"},
#                                     {"id": "SORBMPW13129A9174D", "title": "Classic (Silbury Hill)(Part 2)"},
#                                     {"id": "SOQXAYQ1316771628E", "title": "Famous Person Quiz (The Final Rip Off Remix)"},
#                                     {"id": "SOUMAYZ133EB4E17E8", "title": "Always Look OnThe Bright Side Of Life - Monty Python"}, ...]
#               }
# }



"""
--------------------------------------------------Twitter--------------------------------------------------------
使用Twiter API首先你需要注册Twitter并且开通开发者部分，此时会有个只读的KEY
在py2中有多余py3的用于Twitter的模块，但是还好最常用的twitter模块py3有
twitter模块的文档：https://github.com/sixohsix/twitter/tree/master
"""
from twitter import Twitter

#搜索并以Json格式打印有关python的tweets.(记得把OAuth那行换成你的证书)：
t = Twitter(auth=OAuth(<Access Token>,<Access Token Secret>,<Consumer Key>,<Consumer Secret>))
pythonTweets = t.search.tweets(q = "#python")
print(pythonTweets)

# 发推
from twitter import *
t = Twitter(auth=OAuth(<Access Token>, <Access Token Secret>,<Consumer Key>, <Consumer Secret>))
statusUpdate = t.statuses.update(status='Hello, world!')    #更新状态
print(statusUpdate)

# 获取最近5条@了montypython的tweets
pythonStatuses = t.statuses.user_timeline(screen_name="montypython", count=5)
print(pythonStatuses)


"""
    ------------------------------------Google-----------------------------------------------------
    google API是最完备易用的，其包含各方面以及其软件(youtube，gmail，bloger)的API，并且通过认证可以将访问限制降低
    使用API：https://console.developers.google.com/project
    API库:https://developers.google.com/products/
    API的开启/关闭：https://code.google.com/apis/console/
    更多信息：https://developers.google.com/places/webservice/usage
"""

# 返回the Boston Museum of Science的经纬度
https://maps.googleapis.com/maps/api/geocode/json?address=1+Science+Park+Boston+MA+02114&key=<your API key>
# 返回：
# [ { "address_components" : [ { "long_name" : "Museum Of Science Driveway", "short_name" : "Museum Of Science Driveway", "types" : [ "route" ] },
#                              { "long_name" : "Boston", "short_name" : "Boston", "types" : [ "locality", "political" ] },
#                              { "long_name" : "Massachusetts", "short_name" : "MA", "types" : [ "administrative_area_level_1", "political" ] },
#                              { "long_name" : "United States", "short_name" : "US", "types" : [ "country", "political" ] },
#                              { "long_name" : "02114", "short_name" : "02114", "types" : [ "postal_code" ] } ],
#     "formatted_address": "Museum Of Science Driveway, Boston, MA 02114, USA", "geometry" :
#         { "bounds" :{ "northeast" : { "lat" : 42.368454, "lng" : -71.06961339999999 },
#                       "southwest" :{ "lat" : 42.3672568, "lng" : -71.0719624 } },
#           "location" : { "lat" : 42.3677994, "lng" : -71.0708078 },
#           "location_type" : "GEOMETRIC_CENTER", "viewport" : { "northeast" : { "lat" : 42.3692043802915, "lng" : -71.06943891970849 },
#                                                                "southwest" : { "lat" : 42.3665064197085, "lng" : -71.0721368802915 } } },
#     "types" : [ "route" ] }
# ],
# "status" : "OK" }
#注意：可以模糊输入，Google being Google，会返回best guess
# I have used the Geocode API on several occasions, not only to format user-entered addresses on a website,
# but to crawl the Web looking for things that look like addresses,
# and using the API to reformat them into something easier to store and search


# 获取海拔：
https://maps.googleapis.com/maps/api/elevation/json?locations=42.3677994,-71.0708078&key=<your API key>
# 返回:
# { "results" : [ { "elevation" : 5.127755641937256,
#                   "location" : { "lat" : 42.3677994, "lng" : -71.0708078 },
#                   "resolution" : 9.543951988220215 } ],
#   "status" : "OK"
# }



"""
    ------------------------------------上面的返回哦都市JSON，下面看看如何解析JSON----------------------------------------
    python自带json模块，可用于json object与python object之间的转化

    Python uses a more flexible approach and turns：
        JSON objects into dictionaries；
        JSON arrays into lists；
        JSON strings into strings。
"""
# 将JSON转化为python内建数据结构
import json
from urllib.request import urlopen
def getCountry(ipAddress):
    response = urlopen("http://freegeoip.net/json/"+ipAddress).read().decode('utf-8')
    ** responseJson = json.loads(response) **       #转化为对应的python数据结构
    return responseJson.get("country_code")

print(getCountry("50.78.253.58"))



jsonString = '{"arrayOfNums":[{"number":0},{"number":1},{"number":2}],' \
             ' "arrayOfFruits":[{"fruit":"apple"},' \
             ' {"fruit":"banana"},' \
             ' {"fruit":"pear"}]' \
             '}'
jsonObj = json.loads(jsonString)
print(jsonObj.get("arrayOfNums"))
print(jsonObj.get("arrayOfNums")[1])
print(jsonObj.get("arrayOfNums")[1].get("number")+jsonObj.get("arrayOfNums")[2].get("number"))
print(jsonObj.get("arrayOfFruits")[2].get("fruit"))

# 返回:
# [{'number': 0}, {'number': 1}, {'number': 2}]
# {'number': 1}
# 3
# pear






"""
    -------------------------------------------爬取wikipedia修改历史页面-------------------------------------------------

    如果你修改了wikipedia，那么如果你登陆了，将会记录你的用户名，否则纪录你的IP

    作者曾经爬取了这一信息并且利用Google Geochart Library(https://developers.google.com/chart/interactive/docs/gallery/geochart)
做了可视化的各修改人员地区分布图。(http://www.pythonscraping.com/pages/wikipedia.html)
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime,random,re
random.seed(datetime.datetime.now())

def getLinks(articleUrl):               #找到新页面的links
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html)
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$"))

def getHistoryIPs(pageUrl):             #获取修改页面中的IP信息
    #Format of revision history pages is:
    #           http://en.wikipedia.org/w/index.php?title=Title_in_URL&action=history
    pageUrl = pageUrl.replace("/wiki/", "")
    historyUrl = "http://en.wikipedia.org/w/index.php?title="+pageUrl+"&action=history"
    print("history url is: "+historyUrl)
    html = urlopen(historyUrl)
    bsObj = BeautifulSoup(html)

    #finds only the links with class "mw-anonuserlink" which has IP addresses instead of usernames
    ipAddresses = bsObj.findAll("a", {"class":"mw-anonuserlink"})
    addressList = set()
    for ipAddress in ipAddresses:
        addressList.add(ipAddress.get_text())
    return addressList

links = getLinks("/wiki/Python_(programming_language)")
while(len(links) > 0):
    for link in links:
        print("-------------------")
        historyIPs = getHistoryIPs(link.attrs["href"])
        for historyIP in historyIPs:
            print(historyIP)

    newLink = links[random.randint(0, len(links)-1)].attrs["href"]
    links = getLinks(newLink)



# 添加识别ip所在国家的功能：
def getCountry(ipAddress):
    try:
        response = urlopen("http://freegeoip.net/json/"+ipAddress).read().decode('utf-8')
    except HTTPError:
        return None
    responseJson = json.loads(response)
    return responseJson.get("country_code")

links = getLinks("/wiki/Python_(programming_language)")
while(len(links) > 0):
    for link in links:
        print("-------------------")
        historyIPs = getHistoryIPs(link.attrs["href"])
        for historyIP in historyIPs:
            country = getCountry(historyIP)
            if country is not None:
                print(historyIP+" is from "+country)

    newLink = links[random.randint(0, len(links)-1)].attrs["href"]
    links = getLinks(newLink)

# Here’s a sample output:
# -------------------
# history url is: http://en.wikipedia.org/w/index.php?title=Programming_paradigm&action=history
# 68.183.108.13 is from US
# 86.155.0.186 is from GB
# 188.55.200.254 is from SA
# 108.221.18.208 is from US
# 141.117.232.168 is from CA
# 76.105.209.39 is from US
# 182.184.123.106 is from PK
# 212.219.47.52 is from GB
# 72.27.184.57 is from JM
# 49.147.183.43 is from PH
# 209.197.41.132 is from US
# 174.66.150.151 is from US


"""
    推荐：
    Leonard Richardson, Mike Amundsen, and Sam Ruby’s 《RESTful Web APIs》 provides a strong overview of the theory and practice of using APIs on the Web.
        http://bit.ly/RESTful-Web-APIs
    Mike Amundsen has a fascinating video series, 《Designing APIs for the Web》, that teaches you how to create your own APIs,
        http://oreil.ly/1GOXNhE
"""