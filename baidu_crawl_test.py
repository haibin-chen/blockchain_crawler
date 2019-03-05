#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 17:07:44 2018

@author: chenhaibin
"""
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import urllib
import urllib.request

PAGE_NUM = 2

HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/45.0.2454.101 Safari/537.36'),
                          'referer': 'http://stats.nba.com/scores/'}

'''
for k in range(0, PAGE_NUM):
    url = 'http://www.baidu.com/s?wd=%s&pn=%i' % ('区块链',k*10)
    content = requests.get(url,headers=headers)
    soup = BeautifulSoup(content.text,'html.parser')
    
    dom_tree = etree.HTML(content)
    title = dom_tree.xpath('/html/body/div[@id="wrapper"]/div[@id="wrapper_wrapper"]/div[@id="container"]/div[@id="content_left"]/div[@id="1"]/h3[@class="t c-gap-bottom-small"]/a')
    print(title.text)
    
    abstract = []
    link = dom_tree.xpath('/html/body/div[@id="wrapper"]/div[@id="wrapper_wrapper"]/div[@id="container"]/div[@id="content_left"]/div[@id="1"]/h3[@class="t c-gap-bottom-small"]/a/@href').extract()
    content = []
    
    print(title)
    print(link)
    allNews = soup.find_all('div', { 'id', 'result c-container '})
    for hotNews in allNews:
        h3 = hotNews.find(name = "h3", attrs = { "class": re.compile( "t")}).find('a')
        title.append(h3.text.replace("\"",""))
        div = hotNews.find(name = "div", attrs = { "class": re.compile( "c-abstract")})
        abstract.append(div.text.replace("\"",""))
        a = hotNews.find(name = "a", attrs = { "class": re.compile( "c-showurl")})
        detail_url = a.get('href')
        link.append(detail_url)
        print(title)
        print(abstract)
        print(detail_url)
'''

__all__ = ['APIError', 'API']

DEBUG_LEVEL = 1

import sys
import socket
import json
import urllib
import urllib.request
# import urllib2
import time
# from urllib.parse import urlparse
from collections import Iterable


class APIError(Exception):
    code = None
    """HTTP status code"""

    url = None
    """request URL"""

    body = None
    """server response body; or detailed error information"""

    def __init__(self, code, url, body):
        self.code = code
        self.url = url
        self.body = body

    def __str__(self):
        return 'code={s.code}\nurl={s.url}\n{s.body}'.format(s=self)

    __repr__ = __str__


class API(object):
    token = None
    server = 'http://api.url2io.com/'

    decode_result = True
    timeout = None
    max_retries = None
    retry_delay = None

    def __init__(self, token, srv=None,
                 decode_result=True, timeout=30, max_retries=5,
                 retry_delay=3):
        """:param srv: The API server address
        :param decode_result: whether to json_decode the result
        :param timeout: HTTP request timeout in seconds
        :param max_retries: maximal number of retries after catching URL error
            or socket error
        :param retry_delay: time to sleep before retrying"""
        self.token = token
        if srv:
            self.server = srv
        self.decode_result = decode_result
        assert timeout >= 0 or timeout is None
        assert max_retries >= 0
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        _setup_apiobj(self, self, [])

    def update_request(self, request):
        """overwrite this function to update the request before sending it to
        server"""
        pass


def _setup_apiobj(self, apiobj, path):
    if self is not apiobj:
        self._api = apiobj
        self._urlbase = apiobj.server + '/'.join(path)

    lvl = len(path)
    done = set()
    for i in _APIS:
        if len(i) <= lvl:
            continue
        cur = i[lvl]
        if i[:lvl] == path and cur not in done:
            done.add(cur)
            setattr(self, cur, _APIProxy(apiobj, i[:lvl + 1]))


class _APIProxy(object):
    _api = None

    _urlbase = None

    def __init__(self, apiobj, path):
        _setup_apiobj(self, apiobj, path)

    def __call__(self, post=False, *args, **kwargs):
        # /article
        # url = 'http://xxxx.xxx',
        # fields = ['next',],
        #
        if len(args):
            raise TypeError('only keyword arguments are allowed')
        if not isinstance(post, bool):
            raise TypeError('post argument can only be True or False')

        url = self.geturl(**kwargs)
        # print(url)

        request = urllib.request.Request(url, headers = HEADERS)

        self._api.update_request(request)

        retry = self._api.max_retries
        while True:
            retry -= 1
            try:
                # ret = request.read()
                ret = urllib.request.urlopen(url=request,
                                             timeout=self._api.timeout)
                break
            # except urllib.error.HTTPError as e:
            #     raise APIError(e.code, url, e.read())
            except:
                pass
            break
            '''
            except (socket.error, urllib.error.HTTPError) as e:
                if retry < 0:
                    # raise e
                    return json.loads(e.read())
                _print_debug('caught error: {}; retrying'.format(e))
                time.sleep(self._api.retry_delay)
            '''

        try:
            ret = ret.read()
        except:
            ret = 0
        if self._api.decode_result:
            try:
                if ret != 0:
                    ret = json.loads(ret)
            except:
                pass
            '''
            except BaseException:
                raise APIError(-1,
                               url,
                               'json decode error, value={0!r}'.format(ret))
            '''
        return ret

    def _mkarg(self, kargs):
        """change the argument list (encode value, add api key/secret)
        :return: the new argument list"""

        def enc(x):
            # if isinstance(x, unicode):
            #    return x.encode('utf-8')
            # return str(x)
            return x.encode('utf-8') if isinstance(x, str) else str(x)

        kargs = kargs.copy()
        kargs['token'] = self._api.token
        for (k, v) in kargs.items():
            if isinstance(v, Iterable) and not isinstance(v, str):
                kargs[k] = ','.join('%s' % id for id in [enc(i) for i in v])
            else:
                kargs[k] = enc(v)

        return kargs

    def geturl(self, **kargs):
        """return the request url"""
        return self._urlbase + '?' + urllib.parse.urlencode(self._mkarg(kargs))


def _print_debug(msg):
    if DEBUG_LEVEL:
        sys.stderr.write(str(msg) + '\n')


_APIS = [
    '/article',
    # '/images',
]

_APIS = [i.split('/')[1:] for i in _APIS]

def get_real(o_url):
    '''获取重定向url指向的网址'''
    r = requests.get(o_url, allow_redirects = False)    #禁止自动跳转
    if r.status_code == 302:
        try:
            return r.headers['location']    #返回指向的地址
        except:
            pass
    return o_url 
    
token = 'm5G1IMPXTSyhfiL-1FrG8A'
api = API(token)
PAGE_NUM = 5000
for k in range(187, PAGE_NUM):
    url = 'http://www.baidu.com/s?wd=%s&pn=%i' % ('区块链',k*10)
    #url = 'https://www.cnblogs.com/zhuweiheng/p/8206188.html'
    content = requests.get(url,headers=HEADERS)
    soup = BeautifulSoup(content.text,'html.parser')
    link = []
    allNews = soup.find_all('div', { 'id', 'result c-container '})
    for hotNews in allNews:
        try:
            h3 = hotNews.find(name = "h3", attrs = { "class": re.compile( "t")}).find('a')
            div = hotNews.find(name = "div", attrs = { "class": re.compile( "c-abstract")})
            a = hotNews.find(name = "a", attrs = { "class": re.compile( "c-showurl")})
            detail_url = a.get('href')
            detail_url = get_real(detail_url)
            link.append(detail_url)
            print(detail_url)
        
            ret = api.article(url=detail_url, fields=['text','next'])
            if ret != 0:
                i = {}
                i['title'] = ret['title']
                i['content'] = ret['text'].replace('\r','').replace('\n','')
                i['date'] = ret['date']
                print(i)
        
            depth = 0
            while ret != 0 and ret.get('next') and depth < 20:
                if ret != 0:
                    ret = api.article(url=ret.get('next'), fields=['next','text'])
                    depth += 1
            dataframe1 = pd.DataFrame({'title':[i['title']],'content':[i['content']],'date':[i['date']]})
            dataframe1.to_csv('/Users/chenhaibin/Desktop/baidu.csv', mode='a', header=False) 
        except:
            pass
    print("now is page:")
    print(k)
    time.sleep(0.5)
