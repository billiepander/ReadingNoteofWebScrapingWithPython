#coding:utf-8
"""
    要用到的三个东东：
        1：图像处理的pillow库
        2：谷歌出的识别图像并转文字的Tesseract，注意，他并不是python库，用命令行启动并且使用
        3：Numpy库：a very powerful library used for linear algebra and other large-scale math applications.
                    NumPy works well with Tesseract because of
                    its ability to mathematically represent and manipulate images as large arrays of pixels.


    注：
        验证码：captcha
        Tesseract软件下载页：https://github.com/tesseract-ocr/tesseract/wiki

"""

# 一：识别testocr.jpg图像文件（图像可见templates文件夹）

# C:\Users\Administrator\Desktop>tesseract testocr.jpg textoutput
# 	Tesseract Open Source OCR Engine v3.05.00dev with Leptonica
# 	Warning in pixReadMemJpeg: work-around: writing to a temp file
# 即使在同一路径下分析了tesseract.jpg的文字并且将文字保存在textoutput.txt中(注意，默认就是.txt文件，不需要写上)
# 注：不知为何，在pycharm下的Terminal中运行会显示tesseract不是内部命令，待解决

# 二：看文件testocr_blur.jpg，若识别这个，黑色区域部分将丢失，方法是先对其做灰度处理而后再识别
#
from PIL import Image
import subprocess
# # This module allows you to spawn processes, connect to their input/output/error pipes, and obtain their return codes
# # 将templates下的testocr_blur.jpg做灰度处理后得到testocr_clean.jpg
# def cleanFile(filePath,newFilePath):
#     img = Image.open(filePath)
#     #Set a threshold value for the image, and save
#     img = img.point(lambda x: 0 if x<143 else 255)
#     img.save(newFilePath)
#
#     #call tesseract to do OCR on the newly created image
#     subprocess.call(["tesseract", newFilePath, r"templates\output"])
#
#     #Open and read the resulting data file
#     outputFile = open(r"templatse\output.txt", 'r')
#     print(outputFile.read())
#     outputFile.close()
#
# cleanFile(r"templates\testocr_blur.jpg", r"templates\testocr_clean.jpg")



"""
    ------------------------------------Scraping Text from Images on Websites-------------------------------------------
    亚马逊图书页面点击图书图片会通过Ajax出现书的previews.其有很多页，每页是一张图片，图片旁有下一页的按钮，最后一页没有此按钮
"""
import time
from urllib.request import urlretrieve
import subprocess
from selenium import webdriver
#Create Selenium driver
driver = webdriver.PhantomJS(executable_path=r'D:\program\phantomjs-2.1.1-windows\bin\phantomjs')
#Sometimes, I've found that PhantomJS has problems finding elements on this
#page that Firefox does not. If this is the case when you run this,
#try using a Firefox browser with Selenium by uncommenting this line:
# driver = webdriver.Chrome()
driver.get("http://www.amazon.com/War-Peace-Leo-Nikolayevich-Tolstoy/dp/1427030200")
time.sleep(2)
#Click on the book preview button
driver.find_element_by_id(u"sitbLogoImg").click()
imageList = set()
#Wait for the page to load
time.sleep(5)
#While the right arrow is available for clicking, turn through pages
while "pointer" in driver.find_element_by_id("sitbReaderRightPageTurner").get_attribute("style"):   #下一页的按钮，当没有pointer时代表到达最后一页了
    driver.find_element_by_id("sitbReaderRightPageTurner").click()       # 点击后翻到下一页
    time.sleep(1)
    #Get any new pages that have loaded (multiple pages can load at once,but duplicates will not be added to a set)
    pages = driver.find_elements_by_xpath("//div[@class='pageImage']/div/img")      #每次点击下一页时才生成下一页的HTML，有个小待考证是每个图片是此class,那么第二次定位时就都会定位到啊，后面同理
    #关于XPATH使用可以在F12中Copy项中直接Copy
    for page in pages:
        image = page.get_attribute("src")
        imageList.add(image)            #此地解决了上面的疑问，因为iamgeList为set数据类型，所以前面加入了的会去重

driver.quit()
#Start processing the images we've collected URLs for with Tesseract
for image in sorted(imageList):
    urlretrieve(image, "page.jpg")          #注意这里：下载文件用urlretrieve，图片也是文件啊，小伙
    p = subprocess.Popen(["tesseract", "page.jpg", "page"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    f = open("page.txt", "r")
    print(f.read())

# 注：报错信息：
# selenium.common.exceptions.NoSuchElementException: Message: {"errorMessage":"Unable to find element with id 'sitbLogoImg'","request":{"headers":{"Accept":"application/json","Accept-Encoding":"identity","Connection":"close","Content-Length":"92","Content-Type":"application/json;charset=UTF-8","Host":"127.0.0.1:53268","User-Agent":"Python-urllib/3.4"},"httpVersion":"1.1","method":"POST","post":"{\"sessionId\": \"c5e54430-0700-11e6-980b-79db5371e48a\", \"value\": \"sitbLogoImg\", \"using\": \"id\"}","url":"/element","urlParsed":{"anchor":"","query":"","file":"element","directory":"/","path":"/element","relative":"/element","port":"","host":"","password":"","user":"","userInfo":"","authority":"","protocol":"","source":"/element","queryKey":{},"chunks":["element"]},"urlOriginal":"/session/c5e54430-0700-11e6-980b-79db5371e48a/element"}}
# Screenshot: available via screen
# 实际不可能啊，我在源代码中都发现有啊，这代表初始化就有啊！



"""
    -------------------------------------Reading CAPTCHAs and Training Tesseract----------------------------------------
        ----------------------------------------读取验证码并且训练Tesseract-----------------------------------------
    首先对于一个相对算是很"好"的验证码进行了识别(见templates\capcha_C11.jpg)
        这个图片特点：
            1：相互之间没有交叉
            2：没有背景图片干扰
            3：颜色分明
            4：用了两种字体
        识别出来的结果：
            4N\,,,C<3
        所以，即使是如此"好"的一张图片都不能够识别出来，那么就需要对Tesseract进行训练

"""
def main(self):
    languageName = "eng"
    fontName = "captchaFont"
    directory = "<path to images>"
def runAll(self):
    self.createFontFile()
    self.cleanImages()
    self.renameFiles()
    self.extractUnicode()
    self.runShapeClustering()
    self.runMfTraining()
    self.runCnTraining()
    self.createTessData()

"""
createFontFile creates a required file, font_properties, that lets Tesseract know about the new font we are creating:
    captchaFont 0 0 0 0 0

This file consists the name of the font,followed by 1s and 0s indicating whether italic, bold, or other versions of the font should be considered.
(training fonts with these properties is an interesting exercise, but unfortunately outside the scope of this book).

cleanImages creates higher-contrast versions of all image files found, converts them
to grayscale, and performs other operations that make the image files easier to read
by OCR programs. If you are dealing with CAPTCHA images with visual garbage
that might be easy to filter out in post-processing, here would be the place to add that additional processing.

renameFiles renames all of your .box files and their corresponding image files with
the names required by Tesseract (the file numbers here are sequential digits to keep
multiple files separate):
• <languageName>.<fontName>.exp<fileNumber>.box
• <languageName>.<fontName>.exp<fileNumber>.tiff

extractUnicode looks at all of the created .box files and determines the total set of
characters available to be trained. The resulting Unicode file will tell you how many
different characters you’ve found, and could be a good way to quickly see if you’re missing anything.

The next three functions, runShapeClustering, runMfTraining, and runCtTraining,
create the files shapetable, pfftable, and normproto, respectively.
These all provide information about the geometry and shape of each character, as well as provide
statistical information that Tesseract uses to calculate the probability that a given character is one type or another.

Finally, Tesseract renames each of the compiled data folders to be prepended by the
required language name (e.g., shapetable is renamed to eng.shapetable) and compiles
all of those files into the final training data file eng.traineddata.

The only step you have to perform manually is move the created eng.traineddata file
to your tessdata root folder by using the following commands on Linux and Mac:
    $cp /path/to/data/eng.traineddata $TESSDATA_PREFIX/tessdata
"""



"""
    --------------------------------Retrieving CAPTCHAs and Submitting Solutions----------------------------------------

多数的验证码特性：
    1：他们是由服务器端自动生成的图片，不像传统图片的通过img标签的src属性来获得，但是依然是可以下载的
    2：对于图片的求解方法是存在服务器端数据库中的
    3：多数验证码有时间限制，获取时间与提交时间不能太久


"""
# http://pythonscraping.com/humans-only
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import subprocess
import requests
from PIL import Image
from PIL import ImageOps

def cleanImage(imagePath):
    image = Image.open(imagePath)
    image = image.point(lambda x: 0 if x<143 else 255)
    borderImage = ImageOps.expand(image,border=20,fill='white')
    borderImage.save(imagePath)

html = urlopen("http://www.pythonscraping.com/humans-only")
bsObj = BeautifulSoup(html)
#Gather prepopulated form values
imageLocation = bsObj.find("img", {"title": "Image CAPTCHA"})["src"]
formBuildId = bsObj.find("input", {"name":"form_build_id"})["value"]
captchaSid = bsObj.find("input", {"name":"captcha_sid"})["value"]
captchaToken = bsObj.find("input", {"name":"captcha_token"})["value"]
captchaUrl = "http://pythonscraping.com"+imageLocation
urlretrieve(captchaUrl, "captcha.jpg")
cleanImage("captcha.jpg")
p = subprocess.Popen(["tesseract", "captcha.jpg", "captcha"])
# p = subprocess.Popen(["tesseract", "captcha.jpg", "captcha"], stdout = subprocess.PIPE,stderr=subprocess.PIPE)
p.wait()
f = open("captcha.txt", "r")
#Clean any whitespace characters
captchaResponse = f.read().replace(" ", "").replace("\n", "")       #连用replace！！
print("Captcha solution attempt: "+captchaResponse)
if len(captchaResponse) == 5:
    params = {"captcha_token":captchaToken, "captcha_sid":captchaSid,
              "form_id":"comment_node_page_form", "form_build_id": formBuildId,
              "captcha_response":captchaResponse, "name":"Ryan Mitchell",
              "subject": "I come to seek the Grail",
              "comment_body[und][0][value]":"...and I am definitely not a bot"}
    """
        formData:
            name:
            subject:
            comment_body[und][0][value]:
            form_build_id:form-dtUyNtnIcnJKfMdexYK_sEO8z-4eDiuxfXK1N-ycADM
            form_id:comment_node_page_form
            captcha_sid:844
            captcha_token:2fbe6b0badd7590e9f3ce2d8fada0003
            captcha_response:
            op:Save
        注：其中很多值都是在html中作为某标签属性存在的
    """

    r = requests.post("http://www.pythonscraping.com/comment/reply/10",data=params)
    responseObj = BeautifulSoup(r.text)

    if responseObj.find("div", {"class":"messages"}) is not None:
        print(responseObj.find("div", {"class":"messages"}).get_text())
    else:
        print("There was a problem reading the CAPTCHA correctly!")


# 上面代码有两种可能失败：
# 	1：识别不正确，这有50%可能
# 	2：提交了表单但是服务器端处理不正确，这有20%可能
# 解决办法是多次提交验证码，因为一般来说对于验证码的提交次数是没有限制的。




























