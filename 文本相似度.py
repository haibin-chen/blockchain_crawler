#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 15:02:30 2018

@author: chenhaibin
"""

import pandas as pd
import numpy as np
import jieba.posseg as jb
from gensim.models import word2vec
from math import sqrt

corpus = []
stopwords = [line.strip() for line in open('stopwords.txt', 'r', encoding='utf-8').readlines()]

#1.爬取文本的处理
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
    c = text.content[i]
    for w in jb.cut(c):
        if 'a' in w.flag or 'l' in w.flag or 'v' in w.flag  or 'zg' in w.flag  or 'd' in w.flag or 'n' in w.flag:
            if w.word not in stopwords:
                s=s+' '+w.word
    corpus.append(s)
    
model2 = word2vec.Word2Vec(corpus,size=100)
word2vec_train = []
for i in range(len(corpus)):
    new_sentence = corpus[i]
    sentence_vec = np.zeros(100)
    count = 0
    for j in range(len(new_sentence)):
        if new_sentence[j] in model2:
            sentence_vec += model2[new_sentence[j]]
            count += 1
    sentence_vec /= count
    word2vec_train.append(sentence_vec)

#句子0 1的相似度
def simi_zeroone():
    sum1 = 0
    sum2 = 0
    vec = 0
    for i in range(len(word2vec_train[0])):
        sum1 += word2vec_train[0][i] * word2vec_train[0][i]
        sum2 += word2vec_train[1][i] * word2vec_train[1][i]
        vec += word2vec_train[0][i] * word2vec_train[1][i]
    cos = vec / (sqrt(sum1)+sqrt(sum2))
    print("文本0 1的相似度为:")
    print(cos)

#筛选和文本0最相似的句子
def simi_zero():
    max_cos = 0
    max_index = 0
    print("文本0为"+text.title[0])
    for j in range(len(word2vec_train)):
        sum1 = 0
        sum2 = 0
        vec = 0
        for i in range(len(word2vec_train[0])):
            sum1 += word2vec_train[0][i] * word2vec_train[0][i]
            sum2 += word2vec_train[j][i] * word2vec_train[j][i]
            vec += word2vec_train[0][i] * word2vec_train[j][i]
        if (vec / (sqrt(sum1)+sqrt(sum2))>max_cos):
            max_cos = vec / (sqrt(sum1)+sqrt(sum2))
            max_index = j
    print("最相似的文本为:")
    print(j)
    print("文本内容为"+text.title[j])
simi_zeroone()
simi_zero()
    
