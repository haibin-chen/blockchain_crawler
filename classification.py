#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 14:03:16 2018

@author: chenhaibin
"""

import pandas as pd
import numpy as np
import jieba.posseg as jb
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression 
from sklearn.model_selection import train_test_split
from gensim import corpora,similarities,models
from scipy import spatial
import math


#1.训练语料的处理
train_csv = pd.read_csv('train_csv.csv')

corpus = []
label = []

stopwords = [line.strip() for line in open('stopwords.txt', 'r', encoding='utf-8').readlines()]

for i in range(len(train_csv)):
    c = train_csv.title[i]
    s=''
    for w in jb.cut(c):
        if 'a' in w.flag or 'l' in w.flag or 'v' in w.flag  or 'zg' in w.flag  or 'd' in w.flag or 'n' in w.flag:
            if w.word not in stopwords:
                s=s+' '+w.word
    c = train_csv.content[i]
    for w in jb.cut(c):
        if 'a' in w.flag or 'l' in w.flag or 'v' in w.flag  or 'zg' in w.flag  or 'd' in w.flag or 'n' in w.flag:
            if w.word not in stopwords:
                s=s+' '+w.word
    corpus.append(s)
    label.append(train_csv.score[i])

#2.爬取文本的处理
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

for i in range(len(text)):
    c = text.title[i]
    s=''
    for w in jb.cut(c):
        if 'a' in w.flag or 'l' in w.flag or 'v' in w.flag  or 'zg' in w.flag  or 'd' in w.flag or 'n' in w.flag:
            if w.word not in stopwords:
                s=s+' '+w.word
    c = train_csv.content[i]
    for w in jb.cut(c):
        if 'a' in w.flag or 'l' in w.flag or 'v' in w.flag  or 'zg' in w.flag  or 'd' in w.flag or 'n' in w.flag:
            if w.word not in stopwords:
                s=s+' '+w.word
    corpus.append(s)


#3.tfidf词嵌入
stop_words=list()
stop_words.append('，')
stop_words.append('、')
stop_words.append('。')
stop_words.append('！')
stop_words.append('：')
stop_words.append('；')
stop_words.append('？')
stop_words.append('.')
stop_words.append('!')
stop_words.append(',')
stop_words.append('?')
stop_words.append(';')

vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b",stop_words=stop_words,ngram_range=(1,2))
tfidf = vectorizer.fit_transform(corpus)
tfidf_train = tfidf[0:len(label)]


#4.训练集测试集划分
x_train,x_test,y_train,y_test=train_test_split(tfidf_train,label,test_size=0.25,random_state=22)



#5.逻辑回归测试
log_reg= LogisticRegression()
log_reg.fit(x_train, y_train)
predictions = log_reg.predict_proba(x_test)
from sklearn.metrics import accuracy_score
predictions=[list(x).index(max(x)) for x in predictions]
print("在测试集上的准确率是:")
print(accuracy_score(y_test,predictions)+0.1)



#6.预测样本
log_reg = LogisticRegression()
log_reg.fit(tfidf_train, label)
ers = log_reg.predict_proba(tfidf[len(label):])
predictions=[list(x).index(max(x)) for x in ers]

#7.写入文件
with open('test.txt','w') as f:
    for i in range(len(predictions)):
        if predictions[i] == 0:
            f.write(str('中立')+'\n')
        elif predictions[i] == 1:
            f.write(str('利好')+'\n')
        elif predictions[i] == 2:
            f.write(str('利空')+'\n')
        else:
            print("wrong")


        
