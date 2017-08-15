from bs4 import BeautifulSoup
import requests
import re
import os

url='http://www.biqukan.com/1_1094/'
def getOneChapter(url,name,spath,title):
    #判断文件路径
    if not os.path.exists(spath):
        os.mkdir(spath)
    #url = 'http://www.biqukan.com/1_1094/5403177.html'
    html = requests.get(url)
    # print(html.text)
    mytitle='        '+name
    logfile = open(spath+'/'+ r'logfile.txt', 'a')
    if html.status_code!=200:
        logfile.write(' 抓取失败 : '+url+'  '+name+'\n')
    else:
        # 创建Beautiful Soup对象
        soup = BeautifulSoup(html.content, 'lxml')
        #soup = soup.prettify()

        txt = soup.find_all(id='content')

        # soup_text = BeautifulSoup(str(txt), 'lxml')
        # info = soup_text.div.text.replace('\xa0', ' ')
        # #print(info)
        # #spath='/wyb/'
        # file = open(spath+'/'+name+r'.txt', 'w')
        # file.write(info)
        # file.close()

        info = str(txt).replace('<br>', '\n')
        info = str(txt).replace('<br/>', '\n')
        # print(info)
        text = BeautifulSoup(str(info), 'lxml')
        text = text.div.text
        #print(text)

        file = open(spath+'/'+title+'/'+name+r'.txt', 'w', encoding='utf8')
        # file.write(text+'\r\n')
        file.write(mytitle + '\n\n' + text)
        file.close()

        logfile.write(' 抓取成功 : '+url+'  '+name+'\n')

def getAllChapter(url):
    page=requests.get(url)
    pageinfo=BeautifulSoup(page.content,'lxml')
    txttitle=pageinfo.title.string
    savepath = r'C:/Users/Administrator/PycharmProjects/crawler/py3/BeautifulSoup'+'/'
    #print(savepath)
    infolist=pageinfo.find_all(class_='listmain')
    list=BeautifulSoup(str(infolist),'lxml')
    for i in list.find_all('a'):
        eurl='http://www.biqukan.com'+i.get('href').strip()
        ename=i.text
        print(eurl+' '+ename)
        print('当前正抓取%s'%ename)
        try:
            getOneChapter(eurl,ename,savepath,txttitle)
        except:
            pass
if __name__ == '__main__':
    getAllChapter(url)
