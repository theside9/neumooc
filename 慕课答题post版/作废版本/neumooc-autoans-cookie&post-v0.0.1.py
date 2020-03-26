import urllib
import urllib.request
from urllib import request,parse
import re
import sys
import time
referer="http://www.neumooc.com/course/play/init?courseId=13208EC1356C46BB91168D4C51A99B52"
headers={
"Host": "www.neumooc.com",
"Connection": "keep-alive",
"Cache-Control": "max-age=0",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"DNT": "1",
"Referer": referer,
"Accept-Language": "zh-CN,zh;q=0.9",
"Cookie": "uid=AIuX6m-c8gybKyt3GCpGSPDrJ788E_A2D1TyzoVsMXMjyijibrvNp5EkKDeI99D5x0skPw-CWPy3xxpirCCeRrTqHTQh7jckSY5Hk5bspV2NzPtiz8Vz52ZXNGGh-SDXya5E3MpFmQpNPKZiFxh2ZTzXxysBLXfogIkXJp1gMlA.; JSESSIONID=20209F0D5E012D53BA15441F95C204CC-n1"
    }

#初始化页面信息
print("start")
courseId="13208EC1356C46BB91168D4C51A99B52"
outlineId="433E90130BCE494B902D7113ED38F47F"
url="http://www.neumooc.com/course/play/init?courseId=13208EC1356C46BB91168D4C51A99B52&outlineId="+str(outlineId)
req=request.Request(url=url,headers=headers,method="GET")
response=request.urlopen(req)#获取页面信息
res=response.read().decode('utf-8')#获取到源码
test=re.compile('showTest\(this, ., \'(.*?)\'\)')#考试按钮的resid获取
resid=test.findall(res)#获取resid
#resid，courseid，outlineid获取完成
url="http://www.neumooc.com/course/play/getOutlineResInfo"
dict="resId="+str(resid[0])+"&resType=2&outlineId="+str(outlineId)+"&courseId="+str(courseId)#获取题目用的data
data = bytes(dict,encoding="utf-8")
req = request.Request(url=url,data=data,headers=headers,method="POST")
response = request.urlopen(req)#开始获取题目及答案
web=response.read().decode("utf-8")
testqueslistfind=re.compile('{"resInfo":{"testQuesList":\[]')
while(len(testqueslistfind.findall(web))==1):#返回的包可能有空包，如果返回的testqueslist是空，则重新获取题库
     response = request.urlopen(req)
    #print(response.read().decode("utf-8"))
     web=response.read().decode("utf-8")
#获取到答案页面
#开始从答案页面筛选testid，testQuesid（uqId）,resourceId
resourceIdfind=re.compile('"resourceId":"(.*?)"')#获取resourceId
resourceId=resourceIdfind.findall(web)
#print(resourceId)
#print(web)
testidfind=re.compile('"testId":"(.*?)"')
testid_grup=testidfind.findall(web)#获取到所有testid
testid=testid_grup[0]#只需要一个

uqid_find=re.compile('"uqId":"(.*?)"')
uqid=uqid_find.findall(web)#抓取到所有testQuesid

p=re.compile('"quesContent":".*?".*?"quesAnswer":"<as>(.*?)</as>',re.S)
a=p.findall(web)
p1=re.compile('<a>(.*?)</a>')
all=[]
for i in range(0,len(a)-1):
    a1=p1.findall(a[i])
    all.append(a1)
#print(all)
#所有答案获取完毕
referer="http://www.neumooc.com/course/play/init?courseId=13208EC1356C46BB91168D4C51A99B52&outlineId="+str(outlineId)
headers={
"Host": "www.neumooc.com",
"Connection": "keep-alive",
"Cache-Control": "max-age=0",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"DNT": "1",
"Referer": referer,
"Accept-Language": "zh-CN,zh;q=0.9",
"Cookie": "uid=AIuX6m-c8gybKyt3GCpGSPDrJ788E_A2D1TyzoVsMXMjyijibrvNp5EkKDeI99D5x0skPw-CWPy3xxpirCCeRrTqHTQh7jckSY5Hk5bspV2NzPtiz8Vz52ZXNGGh-SDXya5E3MpFmQpNPKZiFxh2ZTzXxysBLXfogIkXJp1gMlA.; JSESSIONID=20209F0D5E012D53BA15441F95C204CC-n1"
    }
for i in range(0,len(uqid)-1):#从0-n开始循环post
    #保存答案前post
    urlp="http://www.neumooc.com/course/play/testQues"
    dict="testId="+str(testid)+"&curOrNext=&nextId="
    
    data = bytes(dict,encoding="utf-8")
    req = request.Request(url=urlp,data=data,headers=headers,method="POST")
    response = request.urlopen(req)
    #保存答案post
    urlp="http://www.neumooc.com/course/play/updateTestQues"
    dict="testId="+str(testid)+"&testQuesId="+str(uqid[i])+"&seconds=1"
    dicttemp=""
    for q in range(0,len(all[i])):
        alltemp=urllib.parse.quote(all[i][q])
        dicttemp=str(dicttemp)+"&optionSelect="+str(alltemp)
    dict=str(dict)+str(dicttemp)

    data = bytes(dict,encoding="utf-8")
    req = request.Request(url=urlp,data=data,headers=headers,method="POST")
    response = request.urlopen(req)
    if i==len(uqid)-1:#说明这题是最后一题，可以提交了
        break
    #下一题请求post
    urlp="http://www.neumooc.com/course/play/testQues"
    dict="testId="+str(testid)+"&curOrNext=&nextId="+str(uqid[i+1])

    data = bytes(dict,encoding="utf-8")
    req = request.Request(url=urlp,data=data,headers=headers,method="POST")
    response = request.urlopen(req)

urlp="http://www.neumooc.com/course/play/submitTest"
dict="testId="+str(testid)+"&resourceId="+str(resourceId)+"&submitTestTag="

data = bytes(dict,encoding="utf-8")
req = request.Request(url=urlp,data=data,headers=headers,method="POST")
response = request.urlopen(req)
res=response.read().decode("utf-8")
overfind=re.compile('"errorCount":(.*?),"RET_CODE":"(.*?)","noAnswer":(.*?)\}')
over=overfind.findall(res)
code=over[0][1]
error=over[0][0]
noans=over[0][2]
print("状态",code," 错误：",error," 正确：",len(uqid)-1-int(error)-int(noans)," 未答：",noans)
