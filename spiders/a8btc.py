# -*- coding: utf-8 -*-
import scrapy
import csv
import os
import pandas as pd

class A8btcSpider(scrapy.Spider):
    name = 'a8btc'
    allowed_domains = ['https://www.8btc.com']
    #start_urls = ['https://www.8btc.com/p/bitcoin']
    start_urls = ['https://www.8btc.com/article/301959']
    
    '''

    '''
    
    def parse(self, response):
        # 先获取每一页中的文章链接
        '''
        headers = {
            'Cookie':'UM_distinctid=164253c069b3f-02265862c6ddda-47e1137-100200-164253c069eb7;'
                +'yd_cookie=8ab1eadd-ec8f-4774a72a9d138e474562faf5866cc57a99cb;'
                    +'CNZZDATA5934906=cnzz_eid%3D1004817248-1529628310-null%26ntime%3D1529720185;'
                    +'QINGCLOUDELB=836e074b593c4f44bd48f6f76fb94554c2f4da300bc4aee30249f3e95199a4b3|Wy3Bl|Wy3Ai',
        }
        #先登录后从浏览器复制获取cookie 绕开登录验证
        '''
        
        '''
        这一份代码是针对特定页
        fileName = '/Users/chenhaibin/Desktop/computer_network/bitebi/bitebi/bitebitest.csv'
        i = {}
        dataframe = pd.DataFrame({'title':['test'],'content':['test'],'information':['test']})
        for j in range(40):
            i['title'+str(j+1)] = response.xpath('/html/body/div[@id="app"]/div[@class="bbt-main"]/div[@class="bbt-container"]/div[@class="bbt-row"]/div[@class="bbt-col-xs-17"]/div[1]/div[@class="article-item-warp"]['+str(j+1)+']/div[@class="article-item bbt-clearfix"]/div[@class="article-item__body"]/h3[@class="article-item__title"]/a[@class="link-dark-major font-bold bbt-block"]/text()').extract()
            i['content'+str(j+1)] = response.xpath('/html/body/div[@id="app"]/div[@class="bbt-main"]/div[@class="bbt-container"]/div[@class="bbt-row"]/div[@class="bbt-col-xs-17"]/div[1]/div[@class="article-item-warp"]['+str(j+1)+']/div[@class="article-item bbt-clearfix"]/div[@class="article-item__body"]/div[@class="article-item__content"]/text()').extract()
            i['information'+str(j+1)] = response.xpath('/html/body/div[@id="app"]/div[@class="bbt-main"]/div[@class="bbt-container"]/div[@class="bbt-row"]/div[@class="bbt-col-xs-17"]/div[1]/div[@class="article-item-warp"]['+str(j+1)+']/div[@class="article-item bbt-clearfix"]/div[@class="article-item__body"]/div[@class="article-item__info bbt-clearfix"]/div[@class="article-item__author"]/text()').extract()
            dataframe1 = pd.DataFrame({'title':[i['title'+str(j+1)]],'content':[i['content'+str(j+1)]],'information':[i['information'+str(j+1)]]})
            dataframe = pd.concat((dataframe,dataframe1))

        print("爬到了");
        #print(i)
        dataframe.to_csv('/Users/chenhaibin/Desktop/computer_network/bitebi/bitebi/bitebitest.csv')
        '''
        i = {}
        i['title'] = response.xpath('/html/body/div[@id="app"]/div[@class="main bbt-main"]/div[@class="main__header"]/div[@class="header__main"]/div[@class="bbt-container"]/h1/text()').extract()
        i['information'] = response.xpath('/html/body/div[@id="app"]/div[@class="main bbt-main"]/div[@class="main__header"]/div[@class="header__main"]/div[@class="bbt-container"]/div[@class="header__info"]/span[@class="header__info-item"][1]/text()').extract()
        i['content'] = response.xpath('/html/body/div[@id="app"]/div[@class="main bbt-main"]/div[@class="main__body main__body--normal"]/div[@class="bbt-container"]/div[@class="bbt-row"]/div[@class="bbt-col-xs-16"]/div[@class="bbt-html"]/p[1]/text()').extract()
        dataframe1 = pd.DataFrame({'title':[i['title']],'content':[i['content']],'information':[i['information']]})
        dataframe1.to_csv('/Users/chenhaibin/Desktop/computer_network/bitebi/bitebi/bitebitest.csv', mode='a', header=False)
        
        #无限爬
        urls = response.xpath('/html/body/div[@id="app"]/div[@class="main bbt-main"]/div[@class="main__body main__body--normal"]/div[@class="bbt-container"]/div[@class="bbt-row"]/div[@class="bbt-col-xs-16"]/div[@class="bbt-module related-module"]/div[@class="bbt-row"]/div[@class="bbt-col-xs-8"]/div[@class="related-module__item"]/div[@class="item__title"]/a/@href').extract()
        for url in urls:
            url = "https://www.8btc.com" + url
            print ("go to " + url)
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)
        

