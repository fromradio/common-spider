# !/usr/bin/env python3.5
# -*- encoding: utf-8 -*-
''' @Author: Jingk
    @Date: 2017/10/05
    @Python version：Python 3.5
    @Description: operate mysql
'''
import time

import pymysql


class MySQL():

    '''mysql
    '''

    def __init__(self, host='localhost', port=3306,
                 user='root', passwd='171320', logpath='../log/sql.log'):
        self.cursor = None
        self.conn = None
        self.host = host
        self.port = port
        self.user = user
        self.password = passwd
        self.logpath = logpath

    def usedatabase(self, database):
        '''use database
        '''

        info = 0
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                        passwd=self.password, db=database, charset='utf8')
            self.cursor = self.conn.cursor()

        except Exception as msg:
            info = -1
            with open(self.logpath, 'a') as fla:
                ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                fla.write('Error occurred when connect to mysql\thost='+str(self.host)
                          +', port='+str(self.port)+', user='+str(self.user)
                          +', passwd='+str(self.password)+', database='+str(database)+
                          '\t'+str(msg)+'\t'+ltime+'\n')
            print('Error occurred when connect to mysql\n'+str(msg))
        return info

    def createtable(self, table, titles):
        '''create table
        titles:['id', 'int not null auto_increment', ..., 'note', 'varchar(30)']
        titles[0] shall be a primary key
        '''

        info = 0
        sqltitle = str('')
        for index, title in enumerate(titles):
            if index%2 == 0:
                sqltitle = sqltitle + '`'+ title + '`'
            else:
                sqltitle = sqltitle + ' ' + title + ', '
        sql = 'CREATE TABLE IF NOT EXISTS `' + table + '`(' + sqltitle + \
                'PRIMARY KEY (`'+ titles[0] + '`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8'

        try:
            self.cursor.execute(sql)
            self.conn.commit()

        except Exception as msg:
            info = -1
            with open(self.logpath, 'a') as fla:
                ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                fla.write('Error occurred when create table\t' + str(sql)\
                          + '\t' + str(msg)+'\t'+ltime+'\n')
            print('Error occurred when create table\n' + str(sql) + '\n' + str(msg))
        return info

    def querymysql(self, table, columns='*', condition=None, printrow=-1):
        '''select columns from table
        columns:['column1', 'column2',...]
        condition:'column_a < a and column_b > b...'
        '''

        info = 0
        if columns == '*':
            sql = 'SELECT * FROM ' + table
        else:
            sqlcolumn = str('')
            for column in columns:
                sqlcolumn = sqlcolumn + column + ', '
            sqlcolumn = sqlcolumn.strip(', ') # 删去最后一个逗号
            sql = 'SELECT ' + sqlcolumn + ' FROM ' + table
        if condition:
            sql = sql + ' WHERE ' + condition

        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            print('查询到' + str(len(rows)) + '条记录')
            if printrow >= 0:
                for row in rows:
                    print(row)

        except Exception as msg:
            info = -1
            with open(self.logpath, 'a') as fla:
                ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                fla.write('Error occurred when query mysql\t' + str(sql)\
                          + '\t' + str(msg)+'\t'+ltime+'\n')
            print('Error occurred when query mysql\n' + str(sql)+ '\n' + str(msg))
        return len(rows), info

    def insertinto(self, table, values, columns=None):
        '''insert into table values()
        values:['value1', 'value2',...]
        columns:['column1', 'column2',...]
        '''

        info = 0
        sqlvalue = str('')
        for value in values:
            sqlvalue = sqlvalue + '\'' + value + '\'' + ', '
        sqlvalue = sqlvalue.strip(', ') # 删去最后一个逗号
        if columns is None:
            sql = 'INSERT INTO ' + table + ' VALUES(' + sqlvalue + ')'
        else:
            sqlcolumn = str('')
            for column in columns:
                sqlcolumn = sqlcolumn + column + ', '
            sqlcolumn = sqlcolumn.strip(', ') # 删去最后一个逗号
            sql = 'INSERT INTO ' + table + '(' + sqlcolumn + ')' + ' VALUES(' + sqlvalue + ')'

        try:
            self.cursor.execute(sql)
            self.conn.commit()

        except Exception as msg:
            info = -1
            with open(self.logpath, 'a') as fla:
                ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                fla.write('Error occurred when insert into mysql\t' + str(sql)\
                          + '\t' + str(msg)+'\t'+ltime+'\n')
            print('Error occurred when insert into mysql\n' + str(sql)+ '\n' + str(msg))
        return info

    def executestr(self, arg):
        '''execute string
        '''

        info = 0
        try:
            self.cursor.execute(arg)
            self.conn.commit()
        
        except Exception as msg:
            info = -1
            with open(self.logpath, 'a') as fla:
                ltime = str(time.strftime('%Y-%m-%d %H:%M', time.localtime()))
                fla.write('Error occurred when execute string\t' + str(arg)\
                          + '\t' + str(msg)+'\t'+ltime+'\n')
            print('Error occurred when execute string\n' + str(arg)+ '\n' + str(msg))
        return info

    # def updateMysqlSN(self,name,sex):
    #     sql = "UPDATE " + self.table + " SET sex='" + sex + "'" + " WHERE name='" + name + "'"
    #     print("update sn:" + sql)

    #     try:
    #         self.cursor.execute(sql)
    #         self.conn.commit()
    #     except:
    #         self.conn.rollback()


    def close(self):

        '''close cursor
        '''

        self.cursor.close()
        self.conn.close()
