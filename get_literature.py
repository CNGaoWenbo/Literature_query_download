# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:04:47 2019

@author: asdqw
"""

from crossref.restful import Works
from crossref.restful import Journals
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
works=Works()
journals = Journals()
import os
def acquire_text(url,index):

#    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#    from selenium.webdriver.support.ui import WebDriverWait
#    desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
#    desired_capabilities["pageLoadStrategy"] = "eager" # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出    
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    #element.get_attribute('text')


    driver = webdriver.Chrome()#创建浏览器
    driver.get(url)# 访问网址，并且会等待完全加载除非AJAX
    
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'article-section__content')))
    finally:    
        source_code = driver.page_source
        soup = BeautifulSoup(source_code,features='lxml')
        class_title = 'citation__title'
        class_abstract = 'abstract-group'
        class_content = 'article-section__content'
        class_figure = 'figure__image'
    #   fullcontent = soup.find_all('div',{'class':'article__body'})
        obj_title = soup.find_all('h1',{'class':class_title})
        obj_abstract = soup.find_all('div',{'class':class_abstract})
        obj_content = soup.find_all('div',{'class':class_content})
        obj_figure = soup.find_all('img',{'class':class_figure})
        path = 'c:\\Users\\asdqw\\Desktop\\Get_Literature\\'
        abstract = ''
        content = ''
        title = ''
        for text in obj_abstract:
            text = abstract + text.get_text()
            abstract = text
        for text in obj_content:
            text = content + text.get_text()
            content = text
        for text in obj_title:
            text = title + text.get_text()
            title = text
        os.mkdir(path+str(index)+'figure\\')
        for fig in obj_figure:#图片
            fig_url = 'https://onlinelibrary.wiley.com'+fig['src']
            r=requests.get(fig_url,stream=True)
            image_name = fig_url[-20:].split('/')
            with open(path+str(index)+'figure\\'+image_name[0], 'wb') as ff:
                for chunk in r.iter_content(chunk_size=128):
                    ff.write(chunk)

        file = open(path+str(index)+title+'.txt',mode='w+',encoding='UTF-8')
        file.write(abstract+content)
        file.close()
        driver.close()

index = 0

for i in works.query(bibliographic='mof',publisher_name='Wiley-Blackwell').filter(from_online_pub_date='2017').sample(10):
    index += 1
    acquire_text(i['URL'],index)
    print(i['URL'])

#URL = 'http://dx.doi.org/10.1002/aoc.4820'
#acquire_text(URL,index)    