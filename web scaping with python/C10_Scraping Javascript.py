#coding:utf-8

from bs4 import BeautifulSoup
from urllib.request import urlopen

# =========爬取一个200s后用Ajax改变内容的页面

# 一:用原始的方法
html = urlopen('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
bsobj = BeautifulSoup(html,"html.parser")
print(bsobj.find('div').get_text)
# <bound method Tag.get_text of <div id="content">
# This is some content that will appear on the page while it's loading. You don't care about scraping this.
# </div>>


# 二：用selenium
from selenium import webdriver
import time
driver = webdriver.PhantomJS(executable_path=r'D:\program\phantomjs-2.1.1-windows\bin\phantomjs')
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
time.sleep(3)
print(driver.find_element_by_id("content").text)
driver.close()
# Here is some important text you want to retrieve!
# A button to click!

# 注，如果依然想使用BS，在time.sleep(3)后改为：
# pageSource = driver.page_source
# bsObj = BeautifulSoup(pageSource)
# print(bsObj.find(id="content").get_text())

# 三：上述方法并不有效，实际中并不知道什么时候我们想要的内容能够准备完全，一个解决办法是：
#     不断检查某个标志，出现后就认为是好了。
# This code uses the presence of the button with id loadedButton to declare that the page has been fully loaded:
# 注:具体分析标志时用F12，其总是能够显示当前页面所有的HTML（包括JS执行后的），但是网页源码查看只能够看到第一次的
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.PhantomJS(executable_path=r'D:\program\phantomjs-2.1.1-windows\bin\phantomjs')
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
try:
    # <button id="loadedButton">A button to click!</button>
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "loadedButton")))
finally:
    print(driver.find_element_by_id("content").text)
    driver.close()

# Here is some important text you want to retrieve!
# A button to click!

# Expected conditions can be many things in the Selenium library, among them:
# • An alert box pops up
# • An element (such as a text box) is put into a “selected” state
# • The page’s title changes, or some text is now displayed on the page or in a specific element
# • An element is now visible to the DOM, or an element disappears from the DOM

# The following locator selection strategies can used with the By object:
# ID
#     Used in the example; finds elements by their HTML id attribute.
# CLASS_NAME
#     Used to find elements by their HTML class attribute. Why is this function
#     CLASS_NAME and not simply CLASS? Using the form object.CLASS would create
#     problems for Selenium’s Java library, where .class is a reserved method. In order
#     to keep the Selenium syntax consistent between different languages, CLASS_NAME was used instead.
# CSS_SELECTOR
#     Find elements by their class, id, or tag name, using the #idName, .className,tagName convention.
# LINK_TEXT
#     Finds HTML <a> tags by the text they contain. For example, a link that says “Next” can be selected using (By.LINK_TEXT, "Next").
# PARTIAL_LINK_TEXT
#     Similar to LINK_TEXT, but matches on a partial string.
# NAME
#     Finds HTML tags by their name attribute. This is handy for HTML forms.
# TAG_NAME
#     Finds HTML tags by their tag name.
# XPATH
#     Uses an XPath expression (the syntax of which is described in the upcoming sidebar) to select matching elements.


"""
    ------------------------------------------Handling Redirects--------------------------------------------------------
    redirects有两种：
        一,服务器端跳转这样的不用selenium而用urllib模块能够自动捕捉
        二,客户端跳转：需要用Selenium执行JS才能够跳转
"""

# <script>
#     setTimeout(function() {
#         window.location.href = "redirectDemo2.html";
#         }, 2000);
# </script>

from selenium import webdriver
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("html")     #注意！用的是==,既是与初始的比较，若不同，抛出StaleElementReferenceException，此时网页表明已经跳转了
        except StaleElementReferenceException:
            return

driver = webdriver.PhantomJS(executable_path=r'D:\program\phantomjs-2.1.1-windows\bin\phantomjs')
driver.get("http://pythonscraping.com/pages/javascript/redirectDemo1.html")
waitForLoad(driver)
print(driver.page_source)

# 输出：
# Timing out after 10 seconds and returning
# <html><head>
# <title>The Destination Page!</title>
#
# </head>
# <body>
# This is the page you are looking for!
#
# </body></html>


# 注：selenium报错：
#   PermissionError: [WinError 32] 另一个程序正在使用此文件，进程无法访问。: 'C:\\Users\\ADMINI~1\\AppData\\Local\\Temp\\tmp
# 解决方法：
#     http://www.tuicool.com/articles/RnuQZ3I
