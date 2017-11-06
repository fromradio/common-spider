# !/usr/bin/env python3.5
# -*- encoding: utf-8 -*-
''' @Author: Jingk
    @Date: 2017/10/25
    @Python version：Python 3.5
    @Description: parse web pages
    @Update: -----------------------
             Version 1.2.1, 2017/10/26
             ** Modify function gethtml() to return html rather than None when req.url!=url.
             -----------------------
             Version 1.2, 2017/10/25
             ** class Driver
             -- Fixed a bug, add function quit()
             -----------------------
             Version 1.1, 2017/10/24
             ** class Driver
             -- Add function executejs().
             -----------------------
             Version 1.0, 2017/10/23
             ** class Driver
             -- Add function sendkeys().
             -- Modify function geturl(), now we have geturl() and getcurrent(). Notice that
                geturl() contains get() but getcurrent() not, so getcurrent() must be used after
                get(), but geturl() can be used right after the initialize of Driver().
             -- Add options to get(), now we can choose maximum try times.
             -- Add parameter 'info' to functions to record if the function executed correctly.
             -----------------------
'''
import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def parse(url, reg, header=None, tsleep=0.1, tout=-1, logpath='../log/webparse.log', retries=3):
    '''
    parse pages using requests.get
    url: 网址
    reg: 待匹配正则表达式
    header: 浏览器头文件
    tsleep: 获取网址前sleep的时间
    tout: 最大获取时间
    logpath: 日志路径
    retries: 最大重复获取次数
    '''

    time.sleep(tsleep)
    if header is None:
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        header = {'User-Agent' : user_agent}
    items = None
    info = 0    # 记录是否正常获取网页并解析

    while info <= retries and info >= 0:
        try:
            if tout >= 0:
                req = requests.get(url, headers=header, timeout=tout)
            else:
                req = requests.get(url, headers=header)
            if req:
                if not req.url == url:
                    info = -3
                    print('异常！获取网页地址改变')
                    print('原网址：'+str(url))
                    print('获取网址：'+str(req.url))
                    with open(logpath, 'a') as fla:
                        ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                        fla.write('Error: the url changed from \"'+str(url)
                                  +'\" to \"'+str(req.url)+'\"\t'+ltime+'\n')
                else:
                    html = req.text
                    items = re.findall(reg, html, re.S)
                    if items == []:
                        info = -2
                        print('警告！获取的网页中没有匹配字段')
                        with open(logpath, 'a') as fla:
                            ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                            fla.write('Warnning: no string found in \"'+str(req.url)
                                      +'\" matching \"'+str(reg)+'\"\t'+ltime+'\n')
                return items, info

        except Exception as msg:
            if info >= retries:
                info = -1
                print(str(msg)+'\"'+str(url)+'\"')
                with open(logpath, 'a') as fla:
                    ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                    fla.write(str(msg)+'\"'+str(url)+'\"\t'+ltime+'\n')
            else:
                info += 1
                print('第'+str(info)+'次重连中...'+str(url))

    return items, info

def parse_post(url, reg, post, headers=None, tsleep=0.1, tout=-1,
               logpath='../log/webparse.log', retries=3):
    '''
    parse pages using requests.post
    post: 待post的数据, dict格式
    '''

    time.sleep(tsleep)
    if headers is None:
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent' : user_agent}
    items = None
    info = 0    # 记录是否正常获取网页并解析

    while info <= retries and info >= 0:
        try:
            if tout >= 0:
                req = requests.post(url, data=post, headers=headers, timeout=tout)
            else:
                req = requests.post(url, data=post, headers=headers)
            if req:
                if not req.url == url:
                    info = -3
                    print('异常！获取网页地址改变')
                    print('原网址：'+str(url))
                    print('获取网址：'+str(req.url))
                    with open(logpath, 'a') as fla:
                        ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                        fla.write('Error: the url changed from \"'+str(url)
                                  +'\" to \"'+str(req.url)+'\"\t'+ltime+'\n')
                else:
                    html = req.text
                    items = re.findall(reg, html, re.S)
                    if items == []:
                        info = -2
                        print('警告！获取的网页中没有匹配字段')
                        with open(logpath, 'a') as fla:
                            ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                            fla.write('Warnning: no string found in \"'+str(req.url)
                                      +'\" matching \"'+str(reg)+'\"\t'+ltime+'\n')
                return items, info

        except Exception as msg:
            if info >= retries:
                info = -1
                print(str(msg)+'\"'+str(url)+'\"')
                with open(logpath, 'a') as fla:
                    ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                    fla.write(str(msg)+'\"'+str(url)+'\"\t'+ltime+'\n')
            else:
                info += 1
                print('第'+str(info)+'次重连中...'+str(url))

    return items, info

def gethtml(url, header=None, tsleep=0.1, tout=-1, logpath='../log/webparse.log', retries=3):
    '''return html using requests
    '''

    time.sleep(tsleep)
    if header is None:
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        header = {'User-Agent' : user_agent}
    html  =None
    info = 0    # 记录是否正常获取网页并解析

    while info <= retries and info >= 0:
        try:
            if tout >= 0:
                req = requests.get(url, headers=header, timeout=tout)
            else:
                req = requests.get(url, headers=header)
            if req:
                if not req.url == url:
                    info = -3
                    print('异常！获取网页地址改变')
                    print('原网址：'+str(url))
                    print('获取网址：'+str(req.url))
                    with open(logpath, 'a') as fla:
                        ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                        fla.write('Error: the url changed from \"'+str(url)
                                +'\" to \"'+str(req.url)+'\"\t'+ltime+'\n')
                html = req.text
                return html, info

        except Exception as msg:
            if info >= retries:
                info = -1
                print(str(msg)+'\"'+str(url)+'\"')
                with open(logpath, 'a') as fla:
                    ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                    fla.write(str(msg)+'\"'+str(url)+'\"\t'+ltime+'\n')
            else:
                info += 1
                print('第'+str(info)+'次重连中...'+str(url))

    return html, info

class Driver:
    '''driverparse
    '''

    def __init__(self, headers=None, wait=10, logpath=None):
        if logpath is None:
            self.logpath = '../log/webparse.log'
        else:
            self.logpath = logpath

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        if headers is None:
            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0',
                       'Connection': 'keep-alive'
                  }
        for key, value in headers.items():
            dcap['phantomjs.page.customHeaders.{}'.format(key)] = value
        # dcap['phantomjs.page.settings.loadImages'] = False
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)

        self.driver.implicitly_wait(wait)

    def addcookies(self, cookies):
        '''add cookies
        '''
        self.driver.add_cookie(cookies)

    def get(self, url, retries=-1):
        '''get url
        
           retries: the maximum try times, if retries < 0,
           the driver will get url infinitely until the url loaded successfully
        '''
        info = 0    # 记录是否正常获取网页并解析
        if retries < 0:
            while 1:
                try:
                    self.driver.get(url)
                    break

                except Exception as msg:
                    info += 1
                    print(str(msg)+'\"'+str(url)+'\"')
                    with open(self.logpath, 'a') as fla:
                        ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                        fla.write(str(msg)+'\"'+str(url)+'\"\t'+ltime+'\n')
                    print('重连中... '+str(url))
            return info

        while info <= retries and info >= 0:
            try:
                self.driver.get(url)
                break

            except Exception as msg:
                if info >= retries:
                    info = -1
                    print(str(msg)+'\"'+str(url)+'\"')
                    with open(self.logpath, 'a') as fla:
                        ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                        fla.write(str(msg)+'\"'+str(url)+'\"\t'+ltime+'\n')
                else:
                    info += 1
                    print('第'+str(info)+'次重连中...'+str(url))

        return info

    def getcurrent(self):
        '''get html text of current page

           This must be used after Driver.get(url)
        '''
        return self.driver.page_source

    def gethtml(self, url, tsleep=-1):
        '''get html text of a given url
        '''
        info = self.get(url)
        html = None
        if info >= 0:
            if tsleep > 0:
                time.sleep(tsleep)
            html = self.driver.page_source
        return html, info

    def scshot(self, picname=None):
        '''screenshot
        '''
        if picname is None:
            ltime = str(time.strftime('%Y%m%d%H%M%S', time.localtime()))
            self.driver.save_screenshot(ltime+'.png')
        else:
            self.driver.save_screenshot(picname)

    def click(self, value, byid='xpath', tsleep=1):
        '''
        click element in the html
        value: 元素的查找值
        byid: 元素查找方式
        '''
        info = 0
        try:
            clickbutton = self.driver.find_element(byid, value)
            clickbutton.click()
            time.sleep(tsleep)

        except Exception as msg:
            print(str(msg)+'\"'+str(value)+'\"')
            with open(self.logpath, 'a') as fla:
                ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                fla.write(str(msg)+'\"'+str(value)+'\"\t'+ltime+'\n')
            info = -1
            return info
        return info

    def sendkeys(self, keys, key_box, byid='xpath', tsleep=0.5):
        '''send keys

           keys: keywords needed to be sent
           key_box: the box in which keywords put
        '''
        time.sleep(tsleep)
        info = 0
        try:
            keybox = self.driver.find_element(byid, key_box)
            keybox.clear()
            keybox.sendkeys(keys)
            time.sleep(tsleep)

        except Exception as msg:
            print(str(msg)+'\"'+str(keys)+'\"'+'\"'+str(key_box)+'\"')
            with open(self.logpath, 'a') as fla:
                ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                fla.write(str(msg)+'\"'+str(keys)+'\"'+str(key_box)+'\"'+'\"\t'+ltime+'\n')
            info = -1
            return info
        return info

    def scrollbottom(self, times=1, tsleep=10):
        '''scrollbottom
        '''
        for i in range(times):
            print("开始执行第", str(i + 1), "次下拉操作")
            # 执行JavaScript实现网页下拉倒底部
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("第", str(i + 1), "次下拉操作执行完毕")
            print("第", str(i + 1), "次等待网页加载......")
            time.sleep(tsleep) # 等待（时间可以根据自己的网速而定）页面加载出来再执行下拉操作

    def parse(self, reg):
        '''parse
        '''
        info = 0
        html = self.driver.page_source
        items = re.findall(reg, html, re.S)
        if items is None or items == []:
            info = -2
            print('警告！获取的网页中没有匹配字段')
            with open(self.logpath, 'a') as fla:
                ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                fla.write('Warnning: no string found matching \"'+str(reg)+'\"\t'+ltime+'\n')
        return items, info

    def bsparse(self, arg):
        '''parse using bs4
        '''
        info = 0
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        items = soup.find_all(arg)
        if items is None or items == []:
            info = -2
            print('警告！获取的网页中没有匹配字段')
            with open(self.logpath, 'a') as fla:
                ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                fla.write('Warnning: no string found matching \"'+str(arg)+'\"\t'+ltime+'\n')
        return items, info

    def executejs(self, javascript, tsleep=1):
        '''execute javascripts
        '''
        info = 0
        try:
            self.driver.execute_script(javascript)
            time.sleep(tsleep)
            return info

        except Exception as msg:
            print(str(msg)+'\"'+str(javascript)+'\"')
            with open(self.logpath, 'a') as fla:
                ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                fla.write(str(msg)+'\"'+str(javascript)+'\"'+'\t'+ltime+'\n')
            info = -1
            return info

    def quit(self):
        '''quit driver
        '''
        try:
            self.driver.quit()
        except Exception as msg:
            print(str(msg))
            with open(self.logpath, 'a') as fla:
                ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                fla.write(str(msg)+'\t'+ltime+'\n')

'''测试模块
'''
if __name__ == '__main__':
    test = Driver()
    html, info = test.gethtml('http://hotels.ctrip.com/hotel/5683212.html?isFull=F#ctm_ref=hod_sr_lst_dl_n_1_1')
    if info >= 0:
        print(html)
    test.quit()
    test1 = Driver()
    html1, info = test1.gethtml('https://detail.tmall.com/item.htm?id=547037068061&ali_refid=a3_430583_1006:1102664551:N:%E5%A4%A7%E7%B1%B3:1c308690f7fdbc71caa80a7c0dc38d55&ali_trackid=1_1c308690f7fdbc71caa80a7c0dc38d55&spm=a230r.1.14.1')
    if info >= 0:
        print(html1)
    test1.quit()
    

    test2 = Driver(wait=5, logpath='webparse.log')
    info = test2.get('http://hotels.ctrip.com/hotel/5683212.html?isFull=F#ctm_ref=hod_sr_lst_dl_n_1_1', retries=3)
    if info >= 0:
        js = 'document.getElementById("cc_txtCheckIn").value="2018-12-25";'
        js2 = 'document.getElementById("cc_txtCheckOut").value="2018-12-26";'
        test2.executejs(js)
        test2.executejs(js2)
        test2.click('//*[@id="changeBtn"]')
        html2 = test2.getcurrent()
        test2.scshot('1.png')
        with open('1.html', 'w') as flw:
            flw.write(html2)
        # print(html2)
    test2.quit()
