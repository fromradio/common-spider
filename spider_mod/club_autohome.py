# !/usr/bin/env python3.5
# -*- coding: utf-8 -*-
''' @Author：Jingk
    @Date：2017/10/08
    @Python version：Python 3.5
    @Name: 汽车之家论坛爬取
    @Description：1.获取安徽论坛汽车之家帖子数据（前一日）
                  2.URL：http://club.autohome.com.cn/bbs/forum-a-100001-1.html?qaType=-1#pvareaid=101061
                  3.字段详情：网址 标题 发帖人 发帖时间 点击量 回复量 最后更新时间
'''
import datetime

import clear
import mysql
import webparse
import writefile


def main():

    '''main
    '''

    begin_time = datetime.datetime.strftime(datetime.datetime.today(), '%Y/%m/%d %H:%M:%S')
    path = '../data/club_autohome.csv' # /home/allfine/crontab/
    logpath = '../log/club_autohome.log' # /home/allfine/crontab/
    database = 'industrial_added_value'
    table = 'club_autohome'
    titles = ['club_autohome_id', 'int not null auto_increment', 'website', 'varchar(100)',
              'title', 'varchar(100)', 'poster', 'varchar(100)', 'post_time', 'date',
              'click_rate', 'int', 'reply_rate', 'int', 'update_time', 'datetime',
              'note', 'varchar(30)']
    columns = ['website', 'title', 'poster', 'post_time', 'click_rate',
               'reply_rate', 'update_time']
    num_row = 0
    writefile.writecsv(columns, num_row=num_row, path=path, logpath=logpath)

    begin_date = datetime.date.today() - datetime.timedelta(1)
    end_date = datetime.date.today() - datetime.timedelta(1)

    sql = mysql.MySQL(passwd='171320', logpath=logpath)
    info = sql.usedatabase(database)
    # if info < 0:
    #     return 0
    sql.createtable(table, titles)

    maxpage = 10
    exit_flag = False
    for i in range(0, maxpage):
        url = 'https://club.autohome.com.cn/bbs/forum-a-100001-'\
              +str(i+1)+'.html?qaType=-1#pvareaid=101061'
        # 帖子网址 帖子标题 发帖人 发贴时间 点击量 回复量 最后回复时间 （其中，点击量 回复量因为异步加载，为空）
        reg = r'<dl class="list_dl".*?<a.*?href="(.*?)">(.*?)</a>.*?<a.*?>(.*?)</a><span class="tdate">(.*?)</span>.*?<span class="fontblue">(.*?)</span>.*?<span class="tcount">(.*?)</span>.*?<span class="ttime">(.*?)</span>.*?</dl>'
        print('正在爬取第'+str(i+1)+'页')
        items, info = webparse.parse(url, reg, logpath=logpath)

        if info < 0:
            continue

        for item in items:
            item = list(item)
            for j, ite in enumerate(item):
                item[j] = clear.filter_tags(ite.strip())

            item_date = datetime.datetime.strptime(item[-1], '%Y-%m-%d %H:%M').date()
            if item_date < begin_date:
                if i == 0:
                    continue
                else:
                    exit_flag = True
                    break
            if item_date > end_date:
                continue
            item[-1] = item[-1] + ':00'

            # 匹配：点击量 回复量
            url1 = 'http://club.autohome.com.cn'+item[0]
            reg1 = r'<font id="x-views">(.*?)</font>.*?<font.*?>(.*?)</font>'
            items1, info = webparse.parse(url1, reg1, logpath=logpath)
            if info < 0:
                print('帖子获取失败'+str(url1))
                item[4] = -1
                item[5] = -1
                num_row += 1
                writefile.writecsv(item, num_row=num_row, path=path, logpath=logpath)
                sql.insertinto(table, item, columns=columns)
            else:
                item[4] = items1[0][0]
                item[5] = items1[0][1]
                num_row += 1
                writefile.writecsv(item, num_row=num_row, path=path, logpath=logpath)
                sql.insertinto(table, item, columns=columns)

        if exit_flag:
            break

    num_sqlrow, info = sql.querymysql(table)
    sql.close()
    end_time = datetime.datetime.strftime(datetime.datetime.today(), '%Y/%m/%d %H:%M:%S')
    with open(logpath, 'a') as fla:
        fla.write('From '+begin_time+' to '+end_time+', we crawled '+str(num_row)+' rows'+'\n')
        fla.write('There are '+str(num_sqlrow)+' rows in mysql\t'+end_time+'\n')
    print('From '+begin_time+' to '+end_time+', we crawled '+str(num_row)+' rows')
    print('There are '+str(num_sqlrow)+' rows in mysql\t'+end_time)

if __name__ == '__main__':
    main()
