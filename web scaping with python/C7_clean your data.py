from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
"""
    -----------------------------------------------Cleaning in Code-----------------------------------------------------
"""

def ngrams(input, n):
    input = input.split(' ')
    output = []
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])
    return output

html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html,'html.parser')
content = bsObj.find("div", {"id":"mw-content-text"}).get_text()
# print(content.encode('utf-8'))
ngrams = ngrams(content, 2)
for i in ngrams:
    print(i)
print("2-grams count is: "+str(len(ngrams)))

# Using some regular expressions to remove escape characters (such as \n) and filtering
# to remove any Unicode characters, we can clean up the output somewhat:
def ngrams(input, n):

    input = input.split(' ')
    output = []
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])
    return output

html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html,'html.parser')
content = bsObj.find("div", {"id":"mw-content-text"}).get_text()    #此地的content为str，既是py2中把unicode以'utf-8'编码后的东东

#***************************************************************************************************
content = re.sub('\n+', " ", content)       #替换连续换行符为空格
content = re.sub(' +', " ", content)        #替换连续空格为空格
content = bytes(content, "UTF-8")           #以utf-8 encode str从而转化为bytes，同样可以写成：content = content.encode('utf-8'),str encode变成bytes，bytes decode变成str
content = content.decode("ascii", "ignore") #将bytes以ascii解码转化为str，若遇到不能解码的自动删除（此时若有中文就被删除了）
# 参考文献：
# http://www.ituring.com.cn/article/1115
# http://www.ituring.com.cn/article/1116

ngrams = ngrams(content, 2)
for i in ngrams:
    print(i)
print("2-grams count is: "+str(len(ngrams)))




"""
    ---------------------------------------------使用第三方工具清理数据--------------------------------------------------
    OpenRefine
"""