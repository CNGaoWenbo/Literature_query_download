# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:04:47 2019

@author: Gao Wenbo @ Nanjing
"""
##Wiley文献纯文本获取
from crossref.restful import Works
from crossref.restful import Journals
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
works=Works()
journals = Journals()
import os

def acquire_text(metadata,index,path):
    url=metadata['URL']
    journal_name=metadata['container-title']
    atype=metadata['type']
    date=metadata['published-print']['date-parts']
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    driver = webdriver.Chrome()#创建浏览器
    driver.get(url)# 访问网址，并且会等待完全加载除非AJAX    
    try:#加载完所需部分即停止进行下一步，节省时间
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'article-section__content')))
    finally:    
        source_code = driver.page_source
        soup = BeautifulSoup(source_code,features='lxml')
        #所需内容的class name（Wiley）
        class_title = 'citation__title'
        class_abstract = 'abstract-group'
        class_content = 'article-section__content'
        class_figure = 'figure__image'
        #定位所需内容
        obj_title = soup.find_all('h1',{'class':class_title})
        obj_abstract = soup.find_all('div',{'class':class_abstract})
        obj_content = soup.find_all('section',{'class':class_content})
        obj_figure = soup.find_all('img',{'class':class_figure})
        #写入信息
        abstract = ''
        content = ''
        title = ''
        for text in obj_abstract:#摘要
            text = abstract + text.get_text()
            abstract = text
        for text in obj_content:#正文
            text = content + text.get_text()
            content = text
        for text in obj_title:#标题
            text = title + text.get_text()
            title = text
        ##<写入txt文件
        file = open(path+str(index)+'_'+'.txt',mode='w+',encoding='UTF-8')
        file.write(str(title)+'\n'+url+'\n'+atype+'\n'+str(date)+journal_name[0]+'\n'+abstract+content)
        file.close()
        driver.close()
        print('成功下载: '+title)
        ##完成写入txt>
        '''
        #图片下载模块
        os.mkdir(path+str(index)+'figure\\')
        for fig in obj_figure:#图片
            fig_url = 'https://onlinelibrary.wiley.com'+fig['src']
            r=requests.get(fig_url,stream=True)
            image_name = fig_url[-20:].split('/')
            with open(path+str(index)+'figure\\'+image_name[0], 'wb') as ff:#ff: figure file
                for chunk in r.iter_content(chunk_size=128):
                    ff.write(chunk)
        ##图片下载模块
'''
##<输入模块
key_words = 'nanozyme'#搜索关键词
path = 'c:\\Users\\asdqw\\Desktop\\Get_Literature\\'+key_words+'\\'#存储目录
date = '2000'#起始年份    
num = 100#文献量
##输入结束>
try:
    os.mkdir(path)
except:
    pass
index = 0#文献序号
metalist = works.query(bibliographic=key_words,publisher_name='Wiley-Blackwell').filter(from_online_pub_date=date)
count = works.query(bibliographic=key_words,publisher_name='Wiley-Blackwell').filter(from_online_pub_date=date).count()    
print('总文献数：'+str(count))
print('完成Corssref元数据检索')
for i in metalist:#.sample(num):
    index += 1
    print('目前进度: '+str(index)+'/'+str(count+1))
    try:
        acquire_text(i,index,path)
    except:
        print('下载失败')
        file = open(path+'Failed'+str(index)+'.txt',mode='w+',encoding='UTF-8')
        file.write(i['URL'])
        file.close()
        pass
    print('网址: '+i['URL']+'\n')

#URL = 'http://dx.doi.org/10.1002/aoc.4820'
#acquire_text(URL,index)    
