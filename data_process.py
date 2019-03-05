#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 09:54:17 2018

@author: chenhaibin
"""

import pandas as pd
import numpy as np
import jieba.posseg as jb
from wordcloud import WordCloud
from matplotlib import pyplot as plt

text = pd.read_csv('bitebitest.csv',delimiter=',')
for i in range(1873):
    text['title'][i+20] = text['title'][i+20][2:-2]
    text['content'][i+20] = text['content'][i+20][2:-2]
    text['information'][i+20] = text['information'][i+20][14:24]
    if text['title'][i+20] == '[]' or text['content'][i+20] == '[]':
        text.drop([i+20],inplace=True)
for i in range(20):
    text['title'][i] = text['title'][i][2:-2]
    text['content'][i] = text['content'][i][2:-2]
    text['information'][i] = text['information'][i][14:24]
text.drop_duplicates(subset=['title','content','information'],keep=False)

print(text.describe())
text.to_csv('answer.csv')


#任务1 词云
title_corpus = ""
all_corpus = ""

stopwords = [line.strip() for line in open('/Users/chenhaibin/Desktop/computer_network/bitebi/bitebi/stopwords.txt', 'r', encoding='utf-8').readlines()]

for i in range(len(text)):
    c = text.title[i]
    for w in jb.cut(c):
        if 'a' in w.flag or 'l' in w.flag or 'v' in w.flag  or 'zg' in w.flag  or 'd' in w.flag or 'n' in w.flag:
            #形容词 习用语 动词 状态词 副词 名词
            if w.word not in stopwords:
                title_corpus=title_corpus+' '+w.word
                all_corpus=all_corpus+' '+w.word
    c = text.content[i]
    for w in jb.cut(c):
        if 'a' in w.flag or 'l' in w.flag or 'v' in w.flag  or 'zg' in w.flag  or 'd' in w.flag or 'n' in w.flag:
            if w.word not in stopwords:
                all_corpus=all_corpus+' '+w.word
            
wc = WordCloud(font_path='/Users/chenhaibin/Desktop/computer_network/bitebi/bitebi/苹方黑体-准-简.ttf',
               background_color='white',
               width=1000,
               height=800,
               ).generate(title_corpus)
wc.to_file('title.png')

wc = WordCloud(font_path='/Users/chenhaibin/Desktop/computer_network/bitebi/bitebi/苹方黑体-准-简.ttf',
               background_color='white',
               width=1000,
               height=800,
               ).generate(all_corpus)
wc.to_file('all.png') 





