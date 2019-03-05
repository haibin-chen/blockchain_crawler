#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 15:02:30 2018

@author: chenhaibin
"""

import matplotlib.pyplot as plt
import pandas as pd

def simple_analyse()
    analyse = pd.read_csv('answer.csv')
    print(analyse['classification'].value_counts())
    #利好 2172 利空462 中立40

#1.柱形图
def zhu()
    X = ['positive','negative','neutral']
    Y = [2172,462,40]
    plt.bar(X, Y)
    for x,y in zip(X,Y):
        if x=='positive':
            plt.text(x,y+0.1,str(Y[0]), ha='center')
        if x=='negative':
            plt.text(x,y+0.1,str(Y[1]), ha='center')
        if x=='neutral':
            plt.text(x,y+0.1,str(Y[2]), ha='center')
    plt.savefig('/Users/chenhaibin/Desktop/computer_network/bitebi/bitebi/zhuxingtu.jpg',dpi=300)
    plt.show()

lable ='positive','negative','neutral'
plt.axes(aspect=1) #此处设置的目的 是为了让饼状图画出来是圆形
plt.pie([2172/2674,462/2672,40/2674],labels=lable,autopct='%.2f%%')
plt.savefig('/Users/chenhaibin/Desktop/computer_network/bitebi/bitebi/bintu.jpg',dpi=300)
plt.show()

#2.折线图随时间
def zhexian()
    train_csv = pd.read_csv('/Users/chenhaibin/Desktop/computer_network/bitebi/bitebi/answer.csv')
    train_csv = train_csv.fillna({'information':"20190101"})

    train_csv['time'] = train_csv['information'].apply(lambda information:str(information)[0:4]+str(information)[5:7])

    t = []
    for i in range(len(train_csv)):
        if train_csv.time[i] not in t:
            t.append(train_csv.time[i])
    t.remove(' ')
    t.remove("['\\n  ")
    t_list = [int(i) for i in t]
    t_list.sort()
    t_list = [str(i) for i in t_list]

    l1 = [0] * len(t_list) #利好
    l2 = [0] * len(t_list) #总数
    l3 = []

    for i in range(len(train_csv)):
        if train_csv.classification[i] == '利好' and train_csv.time[i] != ' ' and train_csv.time[i] != "['\\n  ":
            l1[t_list.index(train_csv.time[i])] += 1
        if train_csv.time[i] != ' ' and train_csv.time[i] != "['\\n  ":
            l2[t_list.index(train_csv.time[i])] += 1

    for i in range(len(l1)):
        if l1[i]!=0:
            l3.append(l1[i] / l2[i])
    
    #图像优化处理

    plt.ylabel('y')
    plt.xlabel('month')
    plt.title('2012-2018')

    plt.plot(l3)
    plt.savefig('/Users/chenhaibin/Desktop/computer_network/bitebi/bitebi/zhexiantu.jpg',dpi=300)
    plt.show()

simple_analyse()
zhu()
zhexian()
