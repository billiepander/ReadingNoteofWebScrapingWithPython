#coding:utf-8

# CSS是可通过id或者class来进行筛选，下面说明BS的对于那些标签的选择
# "<span class="red">Heavens! what a virulent attack!</span>" replied <span class="green">the prince</span>, not in the least disconcerted by this reception.
# 如上，有红色字有绿色

from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
bsObj = BeautifulSoup(html)
nameList = bsObj.findAll("span", {"class":"green"})     #返回class='green'的所有内容组成的的list ???
for name in nameList:
    print(name.get_text())      # prints name.get_text() in order to separate the content from the tags.
# .get_text()会去掉所有的标签。如果是一大段文字去掉标签后就没法再后期处理了，所以除非是只抽取出单独的一个单元文字，别的情况都不要去除标签


• html
    —body
        —div.wrapper
            — h1
        — div.content
            —table#giftList
                —tr
                    — th
                    — th
                    — th
                    — th
                —tr.gift#gift1
                    — td
                    —td
                        — span.excitingNote
                    — td
                    —td
                        — img
            — ...table rows continue...
        — div.footer

"""
The findAll & find function is responsible for finding tags based on their name and attribute:
    findAll(tag, attributes, recursive, text, limit, keywords)
    find(tag, attributes, recursive, text, keywords)
    参数讲解：
        .findAll({"h1","h2","h3","h4","h5","h6"})           #tag标签，可传入多个
        .findAll("span", {"class":"green", "class":"red"})  #attribute标签，以字典形式，可传入多个,其间的关系是 'or'
        text是不同的，它匹配的是内容而不是标签，比如，如果想知道'the prince'出现的次数：
            nameList = bsObj.findAll(text="the prince")
            print(len(nameList))
        The keywords argument allows you to select tags that contain a particular attribute.For example:
            allText = bsObj.findAll(id="text")
            print(allText[0].get_text())
            注1：以上等效于如下用attributes：
                bsObj.findAll("", {"id":"text"})
            注2：不能如下使用keywords：
                bsObj.findAll(class = "green")  #因为class为python保留字
                可改为：
                bsObj.findAll("", {"class":"green"})
                or
                bsObj.findAll(class_="green")
            注3：attributes里传入多个attribute的关系是or，keywords中可以设置为and
"""

"""
    不同于find函数通过标签及其属性的查找，对于基于位置的标签查找，我们就需要树形定位：
        bsObj.tag.subTag.anotherSubTag

    children:只相隔一代的子层
    descendant:比其低就行，无论低几层。BeautifulSoup默认的就是这个（第一章的bsObj.h1之间就差了好几代）

    需要注意的是，bsobj的无论children还是descendant也还是bsobj，故其仍能够使用find与findall方法以及继续向下定位：
        e.g1:
            bsObj.div.findAll("img")
        e.g2:If you want to find only descendants that are children, you can use the .children tag
            for child in bsObj.find("table",{"id":"giftList"}).children:    #find(all)函数返回的是不是bsobj？？？
                print(child)

    关于兄弟级（sibling）：
        for sibling in bsObj.find("table",{"id":"giftList"}).tr.next_siblings:
            print(sibling)
        # output is to print all rows of products from the product table, except for the first title row.
        同理还有：pre_siblings,  pre_sibling,next_sibling

    关于父级：
        print(bsObj.find("img",{"src":"../img/gifts/img1.jpg"}).parent.previous_sibling.get_text())
"""


"""
    ------------------------------------结合正则表达式使用BS--------------------------------------------------------
    A regular expression can be inserted as any argument in a BeautifulSoup expression, allowing you a great deal of flexibility in finding target elements.
"""
# 现代网站常有空或者隐藏图片用于布局，以及一些随机的图片标签，这种时候使用 .findAll("img")肯定是不够精确的
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html)
** images = bsObj.findAll("img", {"src":re.compile("\.\.\/img\/gifts/img.*\.jpg")}) **
for image in images:
    print(image["src"])

# ../img/gifts/img1.jpg
# ../img/gifts/img2.jpg
# ../img/gifts/img3.jpg
# ../img/gifts/img4.jpg
# ../img/gifts/img6.jpg

"""
    目前为止，都是讲的如何获取内容，但是对于有些时候我们想要获取标签的属性，如a中的链接以及img中的src

With tag objects, a Python list of attributes can be automatically accessed by calling:
    ** myTag.attrs **
Keep in mind that this literally returns a Python dictionary object, which makes
retrieval and manipulation of these attributes trivial. The source location for an
image, for example, can be found using the following line:
    ** myImgTag.attrs['src'] **
"""
bsObj = BeautifulSoup(html)
for link in bsObj.findAll("a"):
    if 'href' in link.attrs:
        print(link.attrs['href'])


"""
    使用lambda：
    For example, the following retrieves all tags that have exactly two attributes:
        ** soup.findAll(lambda tag: len(tag.attrs) == 2) **
    That is, it will find tags such as the following:
        <div class="body" id="content"></div>
        <span style="color:red" class="title"></span>
    使用lambda有时可以替代正则表达式
"""