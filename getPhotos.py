#python 3.5
#encoding=utf-8
import requests
import re
from bs4 import BeautifulSoup
import os

url = 'http://jandan.net/ooxx' #主网址

def GetHtml(url):
    html = requests.get(url).text
    re.findall(url,html)
    return html

def GetImg(html):
    r = BeautifulSoup(html, 'html.parser')
    imglist = []
    for photourl in r.find_all('img'):
        if not photourl.get('src').startswith(('http:','https:')):#没有http：加上
            purl='http:'+photourl.get('src')
        else:
            purl=photourl.get('src')
        #print(purl)
        #print('='*20)
        if not purl.endswith(('jpg', 'gif', 'png')):##没有后缀的加上jpg
            purl = purl + '.jpg'
            #print(purl)
        else:
            purl=purl
        purl=re.sub('thumb180','large',purl) #保证gif打开能动
        #print(purl)
        #print('='*20)
        imglist.append(purl)
    #print(imglist)
    return imglist


def star():
    html = GetHtml(url)
    lll = re.findall('http://jandan.net/ooxx/(.*?)#comments', html) #取下一页网址
    pagenum = int(re.search('[\d]+', lll[0]).group())   #取总共有多少page
    #num=59
    while pagenum > 0:
        newurl = 'http://jandan.net/ooxx/page-' + str(pagenum) + '#comments'#取下一页
        #print(newurl)
        htmls = GetHtml(newurl)
        imgls = GetImg(htmls)
        x = 0
        for imgurl in imgls:
            ax = re.search(u'\.(png|jpg|gif)', imgurl)#取后缀
            # print(ax)
            f = ax.group()
            # print(f)
            if ax.group():
                f = ax.group()
            else:
                pass
            with open(savepath+'%d-%d%s' % (pagenum, x, f), 'wb') as file:  # 图片文件
                logfile = open(savepath+'logfile.txt', 'a') #日志文件
                if f == '.jpg' or f == '.gif':  #只保存了jpg 和gif图
                    file.write(requests.get(imgurl, timeout=30).content)  #图片保存，timeout设置最大为30s
                    logfile.write('当前正在存第'+str(pagenum)+'-'+str(x)+'张图片  '+imgurl+'\n') #日志写
                    print('当前正在存第%d-%d张图片  %s'%(pagenum, x,imgurl))
                    x += 1
        pagenum -= 1


if __name__ == '__main__':
    try:
        savepath='d:/pics/'#保存路径
        if not os.path.exists(savepath):
            os.mkdir(savepath)
        star()
    except requests.exceptions.ConnectionError:
        print('【错误！】当前图片无法下载')