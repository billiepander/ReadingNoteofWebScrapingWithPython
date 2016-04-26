#coding:utf-8

"""
    ------------------------------------------------------提交登陆------------------------------------------------------
    有三种可能的登录：
    1：GET:  url中呗
    2：POST：两种查看方法，一种是查看源代码form中action属性，二是F12网络中错误提交登录信息后查看带有Form Data的
    3:Ajax：同上F12并且错误提交登录后Request Payload项就是（注意其content type，可以用其他编码，没用时写的text/plain）

    注意：使用的网址要是处理提交信息的网址，也就是上面2，3对应项中的Request URL

    注意：Request Payload 与 Form Data的别：http://www.w2bc.com/Article/78730
"""
import requests
params = {'firstname': 'Ryan', 'lastname': 'Mitchell'}
r = requests.post("http://pythonscraping.com/files/processing.php", data=params)
# print(r.text)

# import requests
# params = {'email_addr': 'ryan.e.mitchell@gmail.com'}
# r = requests.post("http://post.oreilly.com/client/o/oreilly/forms/quicksignup.cgi", data=params)
# print(r.text)


import requests

params = {'name':'930041940@qq.com','password':'punkisdead'}
r = requests.post("http://www.luoo.net/login/", data=params)
txt = bytes(r.text,'utf-8')
rxt = txt.decode('utf-8')
# print(txt)


"""
    --------------------------------------------------------提交文件----------------------------------------------------
    在爬虫几乎用不到
"""

# <form action="processing2.php" method="post" enctype="multipart/form-data">
#     Submit a jpg, png, or gif: <input type="file" name="image"><br>
#     <input type="submit" value="Upload File">
# </form>

# import requests
# files = {'uploadFile': open('../files/Python-logo.png', 'rb')}
# r = requests.post("http://pythonscraping.com/pages/processing2.php",files=files)
# print(r.text)


"""
    -----------------------------------------------使用COOKIE & SESSION-----------------------------------------------------------

"""
# ===========cookie
import requests
params = {'username': 'Ryan', 'password': 'password'}
r = requests.post("http://pythonscraping.com/pages/cookies/welcome.php", params)
print("Cookie is set to:")
print(r.cookies.get_dict())
print("-----------")
print("Going to profile page...")
r = requests.get("http://pythonscraping.com/pages/cookies/profile.php",cookies=r.cookies)
print(r.text)

# r既是返回头，其有许多属性：r.text为返回的html中的content
#                          r.cookies为获取的cookie


# ==========session：
import requests
session = requests.Session()
params = {'username': 'username', 'password': 'password'}
s = session.post("http://pythonscraping.com/pages/cookies/welcome.php", params)
print("Cookie is set to:")
print(s.cookies.get_dict())
print("-----------")
print("Going to profile page...")
s = session.get("http://pythonscraping.com/pages/cookies/profile.php")
print(s.text)

# In this case, the session object (retrieved by calling requests.Session()) keeps track
# of session information, such as cookies, headers, and even information about protocols
# you might be running on top of HTTP, such as HTTPAdapters


"""
11章涉及了验证码的识别
For help with CAPTCHAs, check out Chapter 11, which covers image processing and text recognition in Python.

12章：
If you encounter a mysterious error, or the server is rejecting your form submission for an unknown reason,
check out Chapter 12, which covers honey pots, hidden fields,
and other security measures that websites take to protect their forms.
"""













