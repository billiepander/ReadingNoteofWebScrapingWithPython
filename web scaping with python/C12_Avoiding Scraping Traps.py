#coding:utf-8

# 出不来在浏览器中分明可见的东东;提交了一个本该成功的表单却被服务器拒绝了;自身IP被站点封锁，总的来说都是被认定为机器人的结果

"""
    --------------------------------------------------改变请求头--------------------------------------------------------

    使用urllib库时的请求头：
        Accept-Encoding:   identity
        User-Agent:        Python-urllib/3.4
"""

#使用request库武装请求头
import requests
from bs4 import BeautifulSoup
session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
url = "https://www.whatismybrowser.com/developers/what-http-headers-is-my-browser-sending"
req = session.get(url, headers=headers)
bsObj = BeautifulSoup(req.text)
print(bsObj.find("table",{"class":"table-striped"}).get_text)

#大多数的情况改变User-Agent就行了，但是有些多疑的网站甚至选择检查Accept-Language


"""
    ------------------------------------------------COOKIE--------------------------------------------------------------

"""

# 1:view cookies by visiting any site (http://pythonscraping.com, in this example) and calling get_cookies() on the webdriver
from selenium import webdriver
driver = webdriver.PhantomJS(executable_path=r'D:\program\phantomjs-2.1.1-windows\bin\phantomjs')
driver.get("http://pythonscraping.com")
driver.implicitly_wait(1)
print(driver.get_cookies())
# 输出：
# [{'value': '1', 'name': '_gat', 'expires': '周一, 25 4月 2016 04:44:56 GMT', 'path': '/', 'expiry': 1461559496, 'domain': '.pythonscraping.com', 'secure': False, 'httponly': False}, {'value': 'GA1.2.767566030.1461558896', 'name': '_ga', 'expires': '周三, 25 4月 2018 04:34:56 GMT', 'path': '/', 'expiry': 1524630896, 'domain': '.pythonscraping.com', 'secure': False, 'httponly': False}, {'name': 'has_js', 'value': '1', 'path': '/', 'domain': 'pythonscraping.com', 'secure': False, 'httponly': False}]



# 可以通过delete_cookie(), add_cookie(),delete_all_cookies() 函数操作cookie. In addition, you can save and store cookies for use
# in other web scrapers. Here’s an example to give you an idea how these functions work together:
from selenium import webdriver
driver = webdriver.Chrome()
# driver = webdriver.PhantomJS(executable_path=r'D:\program\phantomjs-2.1.1-windows\bin\phantomjs')
driver.get("http://pythonscraping.com")
driver.implicitly_wait(1)
print(driver.get_cookies())
savedCookies = driver.get_cookies()

driver2 = webdriver.Chrome()
# driver2 = webdriver.PhantomJS(executable_path=r'D:\program\phantomjs-2.1.1-windows\bin\phantomjs')
driver2.get("http://pythonscraping.com")
driver2.delete_all_cookies()
for cookie in savedCookies:
    driver2.add_cookie(cookie)      #注：此行报错，only can be used in one domain
# driver2.add_cookie(savedCookies)


driver2.get("http://pythonscraping.com")
driver.implicitly_wait(1)
print(driver2.get_cookies())


"""
    -----------------------------------------------time-----------------------------------------------------------------
    如果你在不同网页间跳转过快，此站点可能认为你是bot
"""

"""
    -----------------------------------------------web form-------------------------------------------------------------
    对于网络爬虫，爬取了许多文章以及内容可能并不特别严重，但是创建成千上万的账户就很严重了，
除了前面讲过的验证码，headers以及IP地址，下面将讲到其他几种保护措施:
    1:hidden input：
        1):除了常用的input显示外，还补充一些其他的隐藏input，每次自动生成其value，一起提交到server。处理这个的办法是先爬登录页得到那些隐藏input的值
        2):将某个常见的如email设置为隐藏，那么如果你的程序提交了此字段就被视为bots，相当于钓鱼执法【honey pot】

    2：honey pot with CSS:
        使用CSS将form或者link等等hidden，这样用户通过browser就没法看到但是爬虫能够看到，比如是一个link，一旦点击
      此link则服务器就发现此为爬虫从而采取应对。
        Fortunately, because Selenium actually renders the pages it visits, it is able to distinguish
      between elements that are visually present on the page and those that aren’t.
        Whether the element is present on the page can be determined by the is_displayed() function.
"""

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
driver = webdriver.PhantomJS(executable_path=r'D:\program\phantomjs-2.1.1-windows\bin\phantomjs')
driver.get("http://pythonscraping.com/pages/itsatrap.html")
links = driver.find_elements_by_tag_name("a")
for link in links:
    if not link.is_displayed():
        print("The link "+link.get_attribute("href")+" is a trap")

fields = driver.find_elements_by_tag_name("input")
for field in fields:
    if not field.is_displayed():
        print("Do not change value of "+field.get_attribute("name"))

# 输出：
# The link http://pythonscraping.com/dontgohere is a trap
# Do not change value of phone
# Do not change value of email
# phone字段：<input type="hidden" name="phone" value="valueShouldNotBeModified"/><p/>
# email字段：<input type="text" name="email" class="customHidden" value="intentionallyBlank"/><p/>
#             <style>
    #             body {overflow-x:hidden;}
    #             .customHidden {
    #                     position:absolute;
    #                     right:50000px;
    #             }
#             </style>



"""
    =================================================总结================================================================
    如果你的爬虫搁浅了，可能是下面的问题：
        1：如果得到的html与browser看到的不一样可能是JS造成的，看第10章
        2：对于post提交form，使用chrome networkinspector来查看实际提交的
        3：如果是站点爬虫出现了异常，检查cookie的设置以及确保每个request都带有cookie
        4：如果得到HTTP error，特别是403错误，极有可能是IP被认定为bot，一些不好设计：
            1:站点跳转太快
            2:未设置header的User-Agent
            3:“点击"了honey-pot
            4:如果实在无法进入，试着联系管理员来获得允许。【Try emailing webmaster@<domain name> or admin@<domain name>】

"""

