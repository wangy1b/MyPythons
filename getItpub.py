#enconding=utf-8

import re
import requests
from bs4 import BeautifulSoup
import time

# 1.解析每一天的题目和答案
# 2.保存成markdown格式
# 3.格式化成自己要的格式

myHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
}

def getAllPage(url):
    allPage = requests.get(url, headers=myHeaders)
    soup=BeautifulSoup(allPage.content,'lxml')
    pages=soup.find(class_ ='pg')
    lastPageLink=pages.find(class_ ='last').get('href')
    lastPageNum=re.sub('\D','',pages.find(class_ ='last').text) #取字符串（...55）中数字(55)
    # print(lastPageLink+'  '+lastPageNum)
    # print('*'*50)
    pageDict={}
    i=1
    while i<=int(lastPageNum):
        pageLink='http://www.itpub.net/'+lastPageLink[:-2]+str(i)
        pageNum=i
        # print(pageLink+'  '+str(pageNum))
        pageDict[pageNum]=pageLink
        i+=1
    return pageDict

def getOnePage(pageUrl):
    onePage = requests.get(pageUrl, headers=myHeaders)
    soup=BeautifulSoup(onePage.content,'lxml')
    oneTexts=soup.find_all(id=re.compile('^normalthread_'))
    onePage=[]
    for oneText in  oneTexts:
        textContent = oneText.tr.th.find(class_='s xst')
        textTitle=textContent.text
        textLinkRaw=textContent.get('href')
        textLink='http://www.itpub.net/'+textLinkRaw
        # print(textTitle+'  '+textLink)
        onePage.append([textTitle,textLink])
    return onePage

def getOneText(titile,link):
    titile=titile.replace('/','')
    if '：' in titile:
         newTitle=titile[titile.index('：') + 1:] #获取'PL/SQL Challenge 每日一题：2017-7-26　12c R2: 超长标识符名字'中'：'后的字符串
    else:
        newTitle = titile
    oneTextPage = requests.get(link, headers=myHeaders)
    oneTextSoup=BeautifulSoup(oneTextPage.content,'lxml')
    posts=oneTextSoup.find_all(id=re.compile('^post_[0-9]+')) #只查找了第一条
    postnum=1
    for post in posts:
        # print(post)
        # print('*'*30)
        postAuthor=post.table.tr.td.find(class_='authi').text.strip() #作者newkid
        # print(postAuthor)
        if postAuthor=='newkid':
            # print(postnum)
            if postnum==1:
                postcontentFirst = post.table.tr.find(class_='t_f')  # 题目
                #print(postcontentFirst.a)
                if   postcontentFirst.a is not None:# postcontentFirst.a 为None时，not  None为啥不是True？
                    beforeLink=postcontentFirst.a.get('href') #历史题目链接
                    textFirst = postcontentFirst.text
                    # print(str(postnum) + ' 题目')
                    # print(postAuthor)
                    testtextFirst=textFirst.replace('http://www.itpub.net/forum.php?m ... eid&typeid=1808',beforeLink)
                else:
                    textFirst = postcontentFirst.text
                    testtextFirst = textFirst
                # print(testtextFirst)
                file=open('PLSQLChallenge\\'+newTitle+'.txt','w',encoding='utf-8')
                file.write(testtextFirst.lstrip())
                file.close()
            else:
                postcontentMore=post.table.tr.find(class_='t_f') #答案
                textMore=postcontentMore.text
                first2text=textMore.strip()[:2]
                #print(first2text)
                if first2text=='答案':
                    # print(str(postnum)+' '+first2text)
                    # print(postAuthor)
                    # print(textMore)
                    file=open('PLSQLChallenge\\'+newTitle+'.txt','a',encoding='utf-8')
                    file.write('*'*80+textMore)
                    file.close()
        postnum+=1



if __name__=='__main__':
    url='http://www.itpub.net/forum.php?mod=forumdisplay&fid=3&filter=typeid&typeid=1808'
    test=getAllPage(url)  #获取所有页面的链接
    # print(test)
    for pageLK in test.values():
        # print(pageLK)
        testPage=getOnePage(pageLK) #获取每页
        #print(testPage)
        for testTitile,testLink in testPage:
            print(testTitile+'---'+testLink)
            getOneText(testTitile,testLink)
            time.sleep(5)
        time.sleep(5)
