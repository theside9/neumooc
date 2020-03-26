import urllib
import urllib.request
from urllib import request,parse
import requests
import re
import os
import sys
import time
import getpass
import _thread
#--------------------------------------

#通过python3实现

#作者：satiya

#--------------------------------------

#固定区
sdmax=8
xcmax=8
statunum=-1
last=False
def init():
    i=0
    while i<1:
        courseId="Undefined"#替换为对应课程的courseid
        if courseId=="Undefined":
            courseId=input("请先输入courseId:")
        referer="http://www.neumooc.com/course/play/init?courseId="+courseId
        session=requests.session()
        res=session.get("http://www.neumooc.com/login/login")
        cookies=requests.utils.dict_from_cookiejar(res.cookies)#获取登录所需cookies
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
        print("登录：")
        yanzhengurl="http://www.neumooc.com/captcha-image?75"
        session.headers=headers
        html = session.get(yanzhengurl)
        #with open('out.jpg', 'wb') as file:
        #    file.write(html.content)
        #img=Image.open('out.jpg')
        username=input("请输入你的学号：")
        psword=getpass.getpass("请输入你的密码（不会显示，正常输入后回车即可）：")
        #img.show()
        #yz=input("请输入验证码：")
        yz=""

#模拟人工输入验证码过程
        try:
            #body="captchaCode="+yz
            #body=bytes(body,encoding="utf-8")
            #url="http://www.neumooc.com/login/captchaCodeCheck"
            #res=session.post(url,body)

            body="userRequestUrl=&userName="+username+"&password="+psword+"&captchaCode="+yz
            body=bytes(body,encoding="utf-8")
            url="http://www.neumooc.com/login/checkLogin"
            res=session.post(url,body)
            cookies=requests.utils.dict_from_cookiejar(res.cookies)#登录后刷新cookies
            headers["Cookie"]="JSESSIONID="+cookies["JSESSIONID"]+";uid="+cookies["uid"]+";"
            i=1
            os.system("cls")
        except:
            print("用户名、密码错误，请重试")
            time.sleep(2)
            os.system("cls")
    linsten_init(session,courseId)
#登录完成

def linsten_init(session,courseId):
    url="http://www.neumooc.com/course/play/init?courseId="+courseId
    course=re.compile('class="childLi outl_(.*?)"')
    test=re.compile('showTest\(this, ., \'(.*?)\'\)')
    title=re.compile('none;">(.*?)</span>')
    testqueslistfind=re.compile('{"resInfo":{"testQuesList":\[]')
    resId_grup=()
    i=0
    while i<1:
        try:
            response=session.get(url)
            res = response.text.encode(response.encoding).decode()#获取到网页正文（乱码转换成二进制码再解码成字符串形式）
            response.close()
            i=1
        except:
            print(tittle[e+1],"初始化异常，正在重启程序！")
            return

    tittle=title.findall(res)#索引记录
    outlineId_grup=course.findall(res)#找出outlineID
    i=1
    while i<1:
        url="http://www.neumooc.com/course/play/init?courseId="+courseId+"&outlineId="+str(outlineId_grup[len(outlineId_grup)-1])
        try:
            response=session.get(url)
            res = response.text.encode(response.encoding).decode()
            response.close()
        except:
            print(tittle[e+1],"索引异常，请重启程序！")
    res=res.replace("\n","").replace("\t","").replace("\r","")
    t=re.compile('href=\"/course/play/init\?courseId='+courseId+'&outlineId=.*?\">.*?<font style=\"color:.*?;\">(.*?)</font>')
    #print(t.findall(res))
    statut=t.findall(res)#所有视频的状态
    global   statunum
    e=0
    while e < len(outlineId_grup):
        if xcmax>0:
            try:
                _thread.start_new_thread( linsten, (session,outlineId_grup,tittle,e,courseId,statut) )
                e+=1
            except:
                print(tittle[e+1],"多线程异常，正在尝试重试……")
        time.sleep(0.3)
    end=False
    while end is False:
        if xcmax ==8 :
            print("所有课程已经听完！强烈建议去个人中心检查进度。")
            end=True
    #for e in range(0,len(outlineId_grup)):
     #   linsten(session,outlineId_grup,tittle,e,courseId)



def linsten(session,outlineId_grup,tittle,e,courseId,statut):
    global xcmax,statunum,last
    xcmax-=1
    outlineId=outlineId_grup[e]
    url="http://www.neumooc.com/course/play/init?courseId="+courseId+"&outlineId="+str(outlineId)
    i=0
    while i<1:
        try:
            response=session.get(url)
            res = response.text.encode(response.encoding).decode()
            response.close()
            i=1
        except:
            print(tittle[e+1],"听课异常1，即将重试")
            time.sleep(3)
    test=re.compile('showVideo\(this, ., \'(.*?)\',\'(.*?)\'\)')#视频按钮的resid获取
    resid=test.findall(res)#获取resid
    temp=test.findall(res)
    if len(temp) is 0:
        print(tittle[e+1],"该专题没有视频")
        xcmax+=1
        return
    statunum+=1
    if statut[statunum]=="完成":
        print(tittle[e+1],"该章节已完成")
        xcmax+=1
        return

    dict="resId="+str(resid[0][0])+"&resType=1&outlineId="+outlineId+"&courseId="+courseId+"&entityId="+str(resid[0][1])
    data = bytes(dict,encoding="utf-8")
    url="http://www.neumooc.com/course/play/getOutlineResInfo"
    i=0
    while i<1:
        try:
            response=session.post(url,data)
            res = response.text.encode(response.encoding).decode()
            response.close()
            i=1
        except:
            print(tittle[e+1],"听课异常2，即将重试")
    videoidfind=re.compile("\"videoId\":\"(.*?)\",")
    videoid=videoidfind.findall(res)
    videoSecond=re.findall('\"videoSecond\":\"(.*?)\"',res)
    videoSecond=int(videoSecond[0])
    #获取到了视频时间总长
    #addplayinfo
    dict="videoId="+str(videoid[0])+"&startSecond=0&courseId="+courseId+"&outlineId="+outlineId
    data = bytes(dict,encoding="utf-8")
    url="http://www.neumooc.com/course/play/addPlayInfo"
    response=session.post(url,data)
    res = response.text.encode(response.encoding).decode()
    uvid=re.findall('\"uvId\":\"(.*?)\"',res)
    uvid=uvid[0]
    #获取到了uvid

    #通过M3u8文件计算视频所需时间
    #alltime=m3u8cal(resid,outlineId,courseId,videoid)
    #开始模拟上传听课记录
    temp=videoSecond%30
    for timed in range(0,videoSecond,30):
        url="http://www.neumooc.com/course/play/updatePlayInfo"
        dict="uvId="+uvid+"&videoId="+videoid[0]+"&endSecond="+str(timed)+"&completeFlag="
        data = bytes(dict,encoding="utf-8")
        session.post(url,data)
        print(tittle[e+1]+"——当前观看到的时长"+str(timed)+"     总时长："+str(videoSecond)+"\n\n")
        time.sleep(30)
    time.sleep(temp)
    url="http://www.neumooc.com/course/play/updatePlayInfo"
    dict="uvId="+uvid+"&videoId="+videoid[0]+"&endSecond="+str(videoSecond)+"&completeFlag=complete"
    data = bytes(dict,encoding="utf-8")
    session.post(url,data)
    xcmax+=1

def main():
    init()
    time.sleep(5000)



if __name__ == '__main__':
    main()