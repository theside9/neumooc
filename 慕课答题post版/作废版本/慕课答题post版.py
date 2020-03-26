import urllib
import urllib.request
from urllib import request,parse
import requests
import re
import os
import sys
import time
from PIL import Image
import getpass
#7B6BF21D9FE045D191AD30C44BCDE4F8   
courseId="C67744D352EB42B199D5905E7167AB97"   
#社会主义
#courseId="7B6BF21D9FE045D191AD30C44BCDE4F8"
#java
print("正在初始化...")
session=requests.session()
res=session.get("http://www.neumooc.com/login/login")
cookies=requests.utils.dict_from_cookiejar(res.cookies)
referer="http://www.neumooc.com/course/play/init?courseId="+courseId
headers={
"Host": "www.neumooc.com",
"Connection": "keep-alive",
"Cache-Control": "max-age=0",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
"DNT": "1",
"Referer": referer,
"Accept-Language": "zh-CN,zh;q=0.9",
"Cookie": "JSESSIONID="+cookies["JSESSIONID"]
}
session.headers=headers
yanzhengurl="http://www.neumooc.com/captcha-image?75"
html = session.get(yanzhengurl)
username=input("请输入你的学号：")
psword=getpass.getpass("请输入你的密码（不会显示，正常输入后回车即可）：")
yz="22"

#模拟人工输入验证码过程
body="captchaCode="+yz
body=bytes(body,encoding="utf-8")
url="http://www.neumooc.com/login/captchaCodeCheck"
res=session.post(url,body)

body="userRequestUrl=&userName="+username+"&password="+psword+"&captchaCode="+yz
body=bytes(body,encoding="utf-8")
url="http://www.neumooc.com/login/checkLogin"
res=session.post(url,body)
cookies=requests.utils.dict_from_cookiejar(res.cookies)
os.system("cls")

#登录完成

print("欢迎"+"登录！如遇到问题请寻找开发者解决")
headers["Cookie"]="JSESSIONID="+cookies["JSESSIONID"]+";uid="+cookies["uid"]+";"
url="http://www.neumooc.com/course/play/init?courseId="+courseId
req=request.Request(url=url,headers=headers,method="GET")
try:
    response=request.urlopen(req)
    res=response.read().decode('utf-8')
    response.close()
except:
    print("无法初始化，请检查网络设置")
    response.close()
    time.sleep(20)
    close()

course=re.compile('class="childLi outl_(.*?)"')
test=re.compile('showTest\(this, ., \'(.*?)\'\)')
title=re.compile('none;">(.*?)</span>')
tittle=title.findall(res)#索引记录
outlineId_grup=course.findall(res)#找出outlineID
testqueslistfind=re.compile('{"resInfo":{"testQuesList":\[]')
resId_grup=()
response.close()
e=0
while e < len(outlineId_grup):
#初始化页面信息
    try:
        e+=1
        if(e==len(outlineId_grup)):
            break
        #courseId="C67744D352EB42B199D5905E7167AB97"
        outlineId=outlineId_grup[e]
        url="http://www.neumooc.com/course/play/init?courseId="+courseId+"&outlineId="+str(outlineId)
        req=request.Request(url=url,headers=headers,method="GET")
        try:
            response=request.urlopen(req)#获取页面信息
            res=response.read().decode('utf-8')#获取到源码
        except:
            print("初始化异常，即将重试该题")
            e-=1
            response.close()
            continue
        response.close()
    #    time.sleep(1)
        test=re.compile('showTest\(this, ., \'(.*?)\'\)')#考试按钮的resid获取
        resid=test.findall(res)#获取resid
        temp=test.findall(res)
        if len(temp) is 0:
            print(tittle[e+1],"该题无测试\n\n")
            resId_grup=resId_grup+tuple(' ')
            continue
    #resid，courseid，outlineid获取完成


    #检测是否100%正答率
    
        url="http://www.neumooc.com/course/play/test/stat/info"
        dict="outlineId="+outlineId
        data = bytes(dict,encoding="utf-8")
        req = request.Request(url=url,data=data,headers=headers,method="POST")
        try:
            response = request.urlopen(req)#开始获取题目及答案
            web=response.read().decode("utf-8")
        except:
            print("正答率加载失败，即将重试"+e)
            e-=1
            response.close()
            continue
        response.close()
        conunt=re.compile('\"testCount\":\"(.*?)\"')
        testCount=conunt.findall(web)
        maxCorrectRatefd=re.compile('\"maxCorrectRate\":\"(.*?)\"')
        maxCorrectRate=maxCorrectRatefd.findall(web)
        try:
            if testCount[0]!="0" and maxCorrectRate[0]=="100":
                print(tittle[e+1],"该题已经完美！")
                continue
        except:
            print(testCount,maxCorrectRate)
            time.sleep(99)
        url="http://www.neumooc.com/course/play/getOutlineResInfo"
        dict="resId="+str(resid[0])+"&resType=2&outlineId="+str(outlineId)+"&courseId="+str(courseId)#获取题目用的data
        data = bytes(dict,encoding="utf-8")
        req = request.Request(url=url,data=data,headers=headers,method="POST")
        try:
            response = request.urlopen(req)#开始获取题目及答案
            web=response.read().decode("utf-8")
        except:
            print("你个辣鸡网站！又出错！！！！"+e)
            e-=1
            response.close()
            continue
        testqueslistfind=re.compile('{"resInfo":{"testQuesList":\[]')
        response.close()
     #   time.sleep(1)
        while(len(testqueslistfind.findall(web))==1):#返回的包可能有空包，如果返回的testqueslist是空，则重新获取题库
             try:
                 response = request.urlopen(req)
                #print(response.read().decode("utf-8"))
                 web=response.read().decode("utf-8")
             except:
                print("重获取异常，即将重试该题",e)
                e-=1
                continue
             response.close()
      #       time.sleep(1)
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
        referer="http://www.neumooc.com/course/play/init?courseId="+courseId+"&outlineId="+str(outlineId)
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
    "Cookie": "JSESSIONID="+cookies["JSESSIONID"]+";uid="+cookies["uid"]+";"
        }
        for i in range(0,len(uqid)-1):#从0-n开始循环post
        #保存答案前post
            urlp="http://www.neumooc.com/course/play/testQues"
            dict="testId="+str(testid)+"&curOrNext=&nextId="
        
            data = bytes(dict,encoding="utf-8")
            req = request.Request(url=urlp,data=data,headers=headers,method="POST")
            try:
                response = request.urlopen(req)
            except:
                print("答题异常1，即将重试",e)
                response.close()
                i-=1
                continue
            response.close()
       #     time.sleep(1)
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
            try:
                response = request.urlopen(req)
            except:
                print("答题异常2，即将重试",e);
                response.close();
                i-=1
                continue
            response.close()
        #    time.sleep(1)
            if i==len(uqid)-1:#说明这题是最后一题，可以提交了
                break
        #下一题请求post
            urlp="http://www.neumooc.com/course/play/testQues"
            dict="testId="+str(testid)+"&curOrNext=&nextId="+str(uqid[i+1])
    
            data = bytes(dict,encoding="utf-8")
            req = request.Request(url=urlp,data=data,headers=headers,method="POST")
            try:
                response = request.urlopen(req)
            except:
                print("答题异常3，即将重试",e)
                i-=1
                response.close()
                continue
            response.close()
         #   time.sleep(1)

        urlp="http://www.neumooc.com/course/play/submitTest"
        dict="testId="+str(testid)+"&resourceId="+str(resourceId)+"&submitTestTag="

        data = bytes(dict,encoding="utf-8")
        req = request.Request(url=urlp,data=data,headers=headers,method="POST")
        try:
            response = request.urlopen(req)
            res=response.read().decode("utf-8")
            response.close()
        except:
            print("答题异常4",)
            e-=1
            response.close()
            continue
            #time.sleep(1)
        overfind=re.compile('"errorCount":(.*?),"RET_CODE":"(.*?)","noAnswer":(.*?)\}')
        over=overfind.findall(res)
        code=over[0][1]
        error=over[0][0]
        noans=over[0][2]
        print(tittle[e+1],"\n\n状态",code," 错误：",error," 正确：",len(uqid)-1-int(error)-int(noans)," 未答：",noans,"\n\n\n")
        code=0
        error=0
        noans=0
    except:
        e-=1
        print("异常重试")
print("已经全部答完")
time.sleep(999)
    #time.sleep(2)
