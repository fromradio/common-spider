#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# copyright@mathu
# Author: Ruimin Wang, wangruimin@qiyi.com
# Func:


from ..utils.exception import GeneratorException


class BasicIterator(object):
    def __init__(self,
                 prefix,
                 suffix,
                 max_page):
        self.prefix = prefix
        self.suffix = suffix
        self.max_page = max_page

    def iter(self):
        for i in range(max_page):
            url = "{}{}{}".format(self.prefix, i+1, self.suffix)
            yield url

def filter_tags(htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=replaceCharEntity(s)#替换实体
    return s

class BasicConditioner(object):
    def __init__(self, begin_date, reg, pos):
        self.begin_date = begin_date
        self.reg = reg
        self.pos = pos
    def judge(self, content):
        regs = re.findall(self.reg, content, re.S)
        for item in items:
            item = list(item)
            for j, i in enumerate(item):
                item[j] = filter_tags(i)
            item_date = datetime.datetime.strptime(item[-1], "%Y-%m-%d %H:%M").date()
            if item_date < begin_date:
                if i > 0:
                    break




class BasicGenerator(object):
    def __init__(self,
                 loader,
                 iterator_class,
                 conditioner,
                 time_interval=500,
                 timeout=200,
                 num_retries=5,
                 data=None,
                 header=None
                ):
        self.time_interval = time_interval
        self.timeout = timeout
        self.num_retries = num_retries
        self.data = data
        self.header = header
        pass

    def generate(self, *args):
        iterator = iterator_class(args)
        for url in iterator.iter():
            content = loader.load_url(url, self.data, self.header, self.timeout,
                                      self.time_interval, self.num_retries)
            if contioner.judge(content):
                break
            yield url
        # yield according to time set up
        pass

