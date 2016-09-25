#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag

def getBook():
    return Opinion

class Economist(BaseFeedBook):
    title                 = '人民网-观点'
    description           = '人民网评&洞鉴专栏&原创观点.'
    language              = 'zh-cn'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    coverfile             = "cv_people.jpg"
    deliver_days          = ['Friday',]
    extra_css      = '''
        h2 { font-size: small;  }
        h1 { font-size: medium;  }
        '''
        
    feeds = [
            ('Index', 'http://opinion.people.com.cn/GB/223228/index.html'),
           ]
    
    def ParseFeedUrls(self):
        """ return list like [(section,title,url,desc),..] """
        mainurl = 'http://opinion.people.com.cn/GB/223228/index.html'
        urls = []
        urladded = set()
        opener = URLOpener(self.host)
        result = opener.open(mainurl)
        if result.status_code != 200:
            self.log.warn('fetch rss failed:%s'%mainurl)
            return []
            
        content = result.content.decode(self.feed_encoding)
        soup = BeautifulSoup(content, "lxml")
        

        for section in soup.find_all('section', attrs={'id':lambda x: x and 'section' in x}):
            h2 = section.find('h2')
            if h2 is None:
                self.log.warn('h2 is empty')
                continue
            sectitle = string_of_tag(h2).strip()
            if not sectitle:
                self.log.warn('h2 string is empty')
                continue
            #self.log.info('Found section: %s' % section_title)
            articles = []
            subsection = ''
            for node in section.find_all('article'):
                subsec = node.find('h5')
                if subsec is not None:
                    subsection = string_of_tag(subsec)
                prefix = (subsection + ': ') if subsection else ''
                a = node.find('a', attrs={"href":True}, recursive=False)
                if a is not None:
                    url = a['href']
                    if url.startswith(r'/'):
                        url = 'http://opinion.people.com.cn' + url
                    url += '/print'
                    title = string_of_tag(a)
                    if title:
                        title = prefix + title
                        #self.log.info('\tFound article:%s' % title)
                        if url not in urladded:
                            urls.append((sectitle,title,url,None))
                            urladded.add(url)
        if len(urls) == 0:
            self.log.warn('len of urls is zero.')
        return urls
        
