#coding:utf-8

# On a fundamental level, all documents are encoded in 0s and 1s. On top of that,
# there are encoding algorithms that define things such as
# “how many bits per character” or “how many bits represent the color for each pixel”.
# The only difference between a text file, a video file, and an image file is how their 0s and 1s are interpreted


# 1: TXT
# The problem is that Python is attempting to read the document as an ASCII document,
# whereas the browser is attempting to read it as an ISO-8859-1 encoded document.
# Neither one, of course, realizes it’s a UTF-8 document.
# We can explicitly define the string to be UTF-8, which correctly formats the output into Cyrillic characters:
from urllib.request import urlopen
textPage = urlopen("http://www.pythonscraping.com/pages/warandpeace/chapter1.txt")      #是个西里尔文文件
print(textPage.read(),'utf-8')    #即是encode('utf-8')

# 在BS中关于encode的使用：
html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html)
content = bsObj.find("div", {"id":"mw-content-text"}).get_text()
** content = bytes(content, "UTF-8") **
** content = content.decode("UTF-8") **
# 关于bytes与encode
# http://www.ituring.com.cn/article/1115
# http://www.ituring.com.cn/article/1116

# 或许你希望全部都encode为utf-8，毕竟其能够很好支持ASCII，但实际上如果使用的是ISO encoding的话将无法具体确定其encoding格式，
# 不过有时可以通过meta标签中的charset属性值看出




# 2：CSV
#     留待





#3:PDF
py2中有不少PDF相关模块没有移植到py3，
py3中相对好用的是pdfminer模块，他可以读取任意的PDF为String
from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO


def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdfFile)
    device.close()
    content = retstr.getvalue()
    retstr.close()
    return content

pdfFile = urlopen("http://pythonscraping.com/pages/warandpeace/chapter1.pdf")
outputString = readPDF(pdfFile)
print(outputString)
pdfFile.close()

# The nice thing about this function is that if you’re working with files locally, you can
# simply substitute a regular Python file object for the one returned by urlopen, and use the line:
from io import open
pdfFile = open("../pages/warandpeace/chapter1.pdf", 'rb')








#4：Microsoft Word and .docx

import win32com
from win32com.client import Dispatch, constants
w = win32com.client.Dispatch('Word.Application')
# 或者使用下面的方法，使用启动独立的进程：
# w = win32com.client.DispatchEx('Word.Application')
# 后台运行，不显示，不警告
w.Visible = 0
w.DisplayAlerts = 0
# 打开新的文件
doc = w.Documents.Open( FileName = filenamein )
# worddoc = w.Documents.Add() # 创建新的文档
# 插入文字
myRange = doc.Range(0,0)
myRange.InsertBefore('Hello from Python!')
# 使用样式
wordSel = myRange.Select()
wordSel.Style = constants.wdStyleHeading1
# 正文文字替换
w.Selection.Find.ClearFormatting()
w.Selection.Find.Replacement.ClearFormatting()
w.Selection.Find.Execute(OldStr,False,False,False,False,False,True,1,True,NewStr,2)
# 页眉文字替换
w.ActiveDocument.Sections[0].Headers[0].Range.Find.ClearFormatting()
w.ActiveDocument.Sections[0].Headers[0].Range.Find.Replacement.ClearFormatting()
w.ActiveDocument.Sections[0].Headers[0].Range.Find.Execute(OldStr,False,False,False,False,False,True,1,False,NewStr,2)
# 表格操作
doc.Tables[0].Rows[0].Cells[0].Range.Text ='123123'
worddoc.Tables[0].Rows.Add() # 增加一行
# 转换为html
wc = win32com.client.constants
w.ActiveDocument.WebOptions.RelyOnCSS = 1
w.ActiveDocument.WebOptions.OptimizeForBrowser = 1
w.ActiveDocument.WebOptions.BrowserLevel = 0 # constants.wdBrowserLevelV4
w.ActiveDocument.WebOptions.OrganizeInFolder = 0
w.ActiveDocument.WebOptions.UseLongFileNames = 1
w.ActiveDocument.WebOptions.RelyOnVML = 0
w.ActiveDocument.WebOptions.AllowPNG = 1
w.ActiveDocument.SaveAs( FileName = filenameout, FileFormat = wc.wdFormatHTML )
# 打印，注：此打印能够跳出选择保存为的格式，并且默认为PDF
doc.PrintOut()
# 关闭
# doc.Close()
w.Documents.Close(wc.wdDoNotSaveChanges)
w.Quit()



