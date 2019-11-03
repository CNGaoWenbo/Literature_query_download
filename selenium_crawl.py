# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 16:24:21 2019

@author: asdqw
"""
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.ui as ui
#chromedriver.exe要放在本文件（*.py）同一文件夹内

driver = webdriver.Chrome()#创建浏览器
url = 'https://onlinelibrary.wiley.com/doi/full/10.1002/anie.201904766'
driver.get(url)# 访问网址，并且会等待完全加载除非AJAX
#wait = ui.WebDriverWait(browser,10)
#abstract = browser.find_element_by_class_name('abstract-group').text
#browser.refresh()
#artice = wait.until(lambda browser: browser.find_element_by_class_name('article-section article-section__full'))
#article = browser.find_element_by_class_name('article-section article-section__full').text
#article-section__content只能获取摘要部分
#article-section article-section__full获取不到，无法返回

driver.close()

#/html/body/div[3]/div/div[2]/main/div[1]/div/section/div/div/div/div/article/div/div[1]/div[4]/article/div[1]/section/div
#section-1-en > div
#section-1-en > div
#<div class="article-section__content en main">
