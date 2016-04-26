#coding:utf-8

# 目前为止，我们都只是爬取并且储存心数据，这章我们要试着从英文语言学的角度来做一些分析
"""
    用二度词频分析法分析一篇英文演讲
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
import operator

def cleanInput(input):
    input = re.sub('\n+', " ", input).lower()
    input = re.sub('\[[0-9]*\]', "", input)
    input = re.sub(' +', " ", input)
    input = bytes(input, "UTF-8")
    input = input.decode("ascii", "ignore")
    input = input.split(' ')

    cleanInput = []
    for item in input:
        item = item.strip(string.punctuation)      #string.punctuation 包含所有标点
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput

def ngrams(input, n):
    input = cleanInput(input)
    output = {}
    for i in range(len(input)-n+1):
        ngramTemp = " ".join(input[i:i+n])
        if ngramTemp not in output:
            output[ngramTemp] = 0
            output[ngramTemp] += 1
    return output

content = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(),'utf-8')     #注意，此地读的是txt文件！！
ngrams = ngrams(content, 2)
sortedNGrams = sorted(ngrams.items(), key = operator.itemgetter(1), reverse=True)
print(sortedNGrams)

"""
    自然语言分析可用库：NLTK
    可用于分析词频，n-gram次数，
"""