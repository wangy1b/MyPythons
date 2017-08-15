#encoding=utf-8
import requests
from bs4 import BeautifulSoup
import re
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

def getPageNum():
    url='https://www.qiushibaike.com'
    myHeaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
    }

    html=requests.get(url,headers=myHeaders)
    soup=BeautifulSoup(html.content,'lxml')
    #pagelink=soup.find_all(class__='pagination')
    #print(soup)
    pagelink=soup.find_all('ul','pagination','li')
    # print(pagelink)
    pagelink = BeautifulSoup(str(pagelink),'lxml')
    #print(pagelink)
    lista=[]
    listb=[]
    for i in pagelink.find_all('a'):
        links=i.get('href').strip()
        nums=i.span.text.strip()
        if nums !='下一页':
            link=url+links
            num=nums
            #print(num+' '+link)
            lista.append(link)
            listb.append(int(num))
    #print(lista)
    #print(listb)
    dicts=dict(zip(listb, lista))
    pageMax=max(listb)
    linkMax=dicts.get(max(listb))
    #print(str(pageMax)+' '+linkMax)
    return pageMax,linkMax

def getContext(texturl):
    myHeaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
    }
    newresponse = requests.get(texturl,myHeaders)
    info = BeautifulSoup(newresponse.content, 'lxml')
    contentRaw = info.find(class_='content')
    # content = info.find(class_='content').text.strip()
    # print(contentRaw)
    contentRaw = str(contentRaw).replace('<br/>', '\n')
    contentRaw = str(contentRaw).replace('<br>', '\n')
    content = BeautifulSoup(contentRaw, 'lxml')
    content = content.text.strip()
    return content

def getOnePage(oneurl):
    myHeaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
    }
    #oneurl='https://www.qiushibaike.com/8hr/page/1/'
    r=requests.get(oneurl,headers=myHeaders)
    soup_page=BeautifulSoup(r.content,'lxml')
    #print(soup_page)
    stories=soup_page.find_all(class_=re.compile('^article block untagged mb15'))
    #print(stories)

    list=[]
    for story in stories:
        nums = story.ul.text.replace('\n', '')
        # print(nums)
        up = int(nums.split('-')[0])
        # print(up)
        down = int(nums.split('-')[-1])
        # print(down)
        dzs = up - down
        #print(dzs)

        if dzs>=2000 :
            k=BeautifulSoup(str(story),'lxml')
            isImg=k.find_all(class_='thumb')
            isAllMesage=k.find_all(class_='contentForAll')
            isContens = k.find_all(class_='content')
            #print(isAllMesage)
            article = k.find(class_='contentHerf')
            alink=article.get('href')
            #print(alink)
            newurl = 'https://www.qiushibaike.com' + alink
            if len(isImg):
                #print('有照片')
                pass
            else:
                user = story.h2.text.strip()
                content=getContext(newurl)

                # print('作者：%s      点赞数:%d     链接：%s'%(user,dzs,newurl))
                # print(content)
                list.append([user,dzs,content,newurl])
    #print(list)
    return list



def getAllPage():
    pageMax,linkMax=getPageNum()
    #print(str(pageMax) + ' ' + linkMax)
    pageinfo={}
    #links=['https://www.qiushibaike.com/8hr/page/','https://www.qiushibaike.com/hot/page/','https://www.qiushibaike.com/text/page/']
    # while pageMax>0:
    #     page=pageMax
    #     for link in links:
    #         setLink=link+str(page)+'/'
    #         # print(str(page)+'  '+link)
    #         print('page:%d  pagelik:%s'%(page,setLink))
    #         infos=getOnePage(setLink)
    #         pageinfo['pagelink '+setLink]=infos
    #     pageMax-=1
    #随机选三个模块中一个进行抓取，根据当前星期几
    today = datetime.date.today()
    isoweekday = datetime.date.isoweekday(today)
    i=isoweekday%3
    #print(i)
    links={0:'https://www.qiushibaike.com/8hr/page/',1:'https://www.qiushibaike.com/hot/page/',2:'https://www.qiushibaike.com/text/page/'}
    link=links.get(i)
    #print(link)
    while pageMax>0:
        page=pageMax
        setLink=link+str(page)+'/'
        # print(str(page)+'  '+link)
        print('page:%d  pagelik:%s'%(page,setLink))
        infos=getOnePage(setLink)
        time.sleep(2)
        pageinfo['pagelink '+setLink]=infos
        pageMax-=1
    return pageinfo

def saveStories(myDict):
    #myList=[['打不死的至尊宝', 13030, '大家的童年是不是这样的： 花一毛钱买一袋汽水，在袋角咬个小洞洞喝一下午，然后再往里面吹气，拧紧，再一脚踩爆', 'https://www.qiushibaike.com/article/119388480']]
    #myDict={'page1':myList}
    date=datetime.datetime.now().strftime('%Y%m%d')
    fileName='qsbk'+date+r'.txt'
    saveTextPath=r'F:\qsbk2MyEmail'+'\\'+fileName


    file=open(saveTextPath, 'w', encoding='utf8') #打开要保存文件
    print('进入排序，请等待....')
    #传入字典只取values
    dictValues = myDict.values()
    allList = []
    #将传入dict.values改为list
    for pageLists in dictValues:
        for textLists in pageLists:
            allList.append(textLists)

    #myDict.clear() #清除字典值
    #print(allList)

    #去重
    allListQC =[]
    for one in allList:
        if one not in allListQC:
            allListQC.append(one)
    #allList.clear()
    # 把list按照点赞数排降序
    allPageLists = sorted(allListQC, key=lambda x:x[1], reverse=True)
    #allListQC.clear()
    print('排序完成！')
    print('写入文件，请等待...')
    id=1
    for textList in allPageLists:
        #print(textList)
        firstLine='序号: '+str(id)+'      作者: '+textList[0]+'      点赞数: '+str(textList[1])+'      链接: '+textList[3]
        secondLine=str(textList[2])+'\n\n'
        allLine=firstLine+'\n'+secondLine
        # print(firstLine)
        # print(secondLine)
        #print(allLine)
        file.write(allLine)
        id+=1
    file.close()
    allPageLists.clear()
    print('文件写入完成！')
    return saveTextPath,fileName



def send_email(SMTP_host, from_addr, password, to_addrs, subject='', content=''):
    """
    发送邮件
    :param SMTP_host: smtp.163.com
    :param from_addr: 发送地址：xxx@163.com
    :param password: 密码: password
    :param to_addrs: 发送给谁的邮箱： xxx@qq.com
    :param subject:  邮件主题： test
    :param content:  邮件内容： test
    :return: None
    """
    msg = MIMEMultipart()
    msg['from'] = from_addr
    msg['to'] = to_addrs
    msg['subject'] = subject
    content = content
    txt = MIMEText(content)
    msg.attach(txt)

    #SMTP
    # smtp = smtplib.SMTP()
    # smtp.connect(SMTP_host, '25')

    #SMTP_SSL
    smtp = smtplib.SMTP_SSL(SMTP_host,'465')
    smtp.login(from_addr, password)
    smtp.sendmail(from_addr, to_addrs, str(msg))
    smtp.quit()


if __name__=='__main__':
    textPath, fileNM='',''
    try:
        infomations=getAllPage()
        textPath,fileNM=saveStories(infomations)
        # textPath, fileNM = r'F:\qsbk2MyEmail\qsbk20170811.txt', 'qsbk20170811.txt'
        mySmtp_host = 'smtp.qq.com'
        myFrom_addr = 'xxx@qq.com' 
        myPassword = 'xxxx' #客户端密码
        ###########163信箱老是报smtplib.SMTPHeloError: (500, b'Error: bad syntax') ，故选择qq邮箱发给自己
        # mySmtp_host = 'smtp.163.com'
        # myFrom_addr = 'xxxxx@163.com'
        # myPassword = 'xxxxx'  #客户端密码
        myTo_addrs='xxxx@qq.com'#接受邮箱
        mySubject = fileNM
        file = open(textPath, 'r', encoding='utf-8')
        myContent = file.read()
        file.close()
        send_email(mySmtp_host, myFrom_addr, myPassword, myTo_addrs, mySubject, myContent)
        print('邮件已成功发送了!')
        logfile=open(textPath.strip(fileNM)+'logfile.txt','a',encoding='utf-8')
        logfile.write(fileNM+' : 邮件已成功发送了!\n')
        logfile.close()

    except smtplib.SMTPException as emailErr:
        print(emailErr)
        logfile=open(textPath.strip(fileNM)+'logfile.txt','a',encoding='utf-8')
        logfile.write(fileNM+' : '+str(emailErr)+'\n')
        logfile.close()