#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 23:56:41 2018

@author: chenhaibin
"""


import pandas as pd
import numpy as np
import jieba.posseg as jb
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.sklearn

stopwords = [line.strip() for line in open('stopwords.txt', 'r', encoding='utf-8').readlines()]

text = pd.read_csv('baidu_crawl.csv',delimiter=',',encoding='utf-8')
#text.drop_duplicates(subset=['title','content','date'],keep=False)
text.dropna(subset = ['content','title','date'],axis=0,inplace=True)
#text = text[0:500]

all_corpus = ""
corpus = []

for i, row in text.iterrows():
    print(i)
    every_corpus = ""
    c = text.title[i]
    for w in jb.cut(c):
        if 'a' in w.flag or 'l' in w.flag or 'v' in w.flag  or 'zg' in w.flag  or 'd' in w.flag or 'n' in w.flag:
            if w.word not in stopwords:
                all_corpus=all_corpus+' '+w.word
                every_corpus = every_corpus + ' ' + w.word
    c = text.content[i]
    for w in jb.cut(c):
        if 'a' in w.flag or 'l' in w.flag or 'v' in w.flag  or 'zg' in w.flag  or 'd' in w.flag or 'n' in w.flag:
            if w.word not in stopwords:
                all_corpus=all_corpus+' '+w.word
                every_corpus = every_corpus + ' ' + w.word
    corpus.append(every_corpus)
'''
wc = WordCloud(font_path='/Users/chenhaibin/Desktop/computer_network/bitebi/src/苹方黑体-准-简.ttf',
               background_color='white',
               width=1000,
               height=800,
               ).generate(all_corpus)
wc.to_file('baidu_all.png') 
'''

'''
tr4w = TextRank4Keyword(stop_words_file=stopwords)  # 导入停止词


# 使用词性过滤，文本小写，窗口为2
tr4w.train(text=text, speech_tag_filter=True, lower=True, window=2)  

print('关键词：')
# 20个关键词且每个的长度最小为1
print('/'.join(tr4w.get_keywords(20, word_min_len=1))) 

print('关键短语：')
# 20个关键词去构造短语，短语在原文本中出现次数最少为2
print('/'.join(tr4w.get_keyphrases(keywords_num=20, min_occur_num= 2)) ) 

tr4s = TextRank4Sentence(stop_words_file=stopwords)

# 使用词性过滤，文本小写，使用words_all_filters生成句子之间的相似性
tr4s.train(text=text, speech_tag_filter=True, lower=True, source = 'all_filters')

print ('摘要：')
print ('\n'.join(tr4s.get_key_sentences(num=3))) # 重要性最高的三个句子
'''



def word2vec(word_list):
    tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                    min_df=10)
    tf = tf_vectorizer.fit_transform(corpus)
    print(tf.shape)

    lda = LatentDirichletAllocation(n_topics=10)
    #用变分贝叶斯方法训练模型
    lda.fit(tf)
    

    #依次输出每个主题的关键词表
    tf_feature_names = tf_vectorizer.get_feature_names()
    return lda,tf,tf_feature_names,tf_vectorizer

def pyLDAvisUI(lda,tf,tf_vectorizer):
    page = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
    pyLDAvis.save_html(page, 'lda.html')        #将主题可视化数据保存为html文件
    pyLDAvis.save_json(page,'lda.json') 

lda, tf, tf_feature_names, tf_vectorizer = word2vec(all_corpus)
pyLDAvisUI(lda, tf, tf_vectorizer)
