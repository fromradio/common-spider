# !/usr/bin/env python3.5
# -*- coding: utf-8 -*-
''' @Author: Jingk
    @Date: 2017/10/05
    @Python version：Python 3.5
    @Description: write a list to a file as a row
'''
import csv
import os
import time


def writerow(rowdata, num_row=-1, path='../data/filename',
             delimeter='\t', mode='a', logpath='../log/writefile.log'):
    '''write a list to a file as a row
    '''

    try:
        if num_row != 0:
            with open(path, mode) as flm:
                for item in enumerate(rowdata):
                    flm.write(str(item[1])+delimeter)
                flm.write('\n')
            if num_row > 0:
                print('写入'+ str(num_row)+'行记录')
        elif num_row == 0:
            if not os.path.exists(path):
                with open(path, mode) as flm:
                    for item in enumerate(rowdata):
                        flm.write(str(item[1])+delimeter)
                    flm.write('\n')
                print('写入标题')
            else:
                print('文件已存在')

    except Exception as msg:
        print('错误！写入文件失败')
        print(str(msg))
        with open(logpath, 'a') as loga:
            ltime = str(time.strftime("%Y-%m-%d %H:%M", time.localtime()))
            loga.write('Error occurred when write to \"'+path+'\"\t'+ltime+'\t'+str(msg)+'\n')

def writecsv(rowdata, num_row=-1, path='../data/filename.csv',
             mode='a', logpath='../log/writefile.log'):
    '''write a list to a csvfile as a row
    '''

    try:
        if num_row != 0:
            with open(path, mode) as csvm:
                csvwriter = csv.writer(csvm, dialect='excel')
                csvwriter.writerow(rowdata)
            if num_row > 0:
                print('写入'+ str(num_row)+'行记录')
        elif num_row == 0:
            if not os.path.exists(path):
                with open(path, mode) as csvm:
                    csvwriter = csv.writer(csvm, dialect='excel')
                    csvwriter.writerow(rowdata)
                print('写入标题')
            else:
                print('文件已存在')

    except Exception as msg:
        print('错误！写入文件失败')
        print(str(msg))
        with open(logpath, 'a') as loga:
            ltime = str(time.strftime("%Y-%m-%d %H:%M", time.localtime()))
            loga.write('Error occurred when write to \"'+path+'\"\t'+ltime+'\t'+str(msg)+'\n')

# def mergefile(filelist, path='../data/mergefile', logpath='../log/writefile.log'):

#     '''merge files into one file
#     '''

#     for filepath in filelist:
#         num = 0
#         try:
#             with open(filepath, 'r') as flr:
#                 for line in flr.readlines:
#                     num += 1
#                     writerow(line.strip('\n'), num_row=num, path=path, delimeter='')

#         except Exception as msg:
#             print('错误！合并文件失败')
#             with open(logpath, 'a') as loga:
#                 ltime = str(time.strftime("%Y-%m-%d %H:%M", time.localtime()))
#                 loga.write('Error occurred when open \"'+filepath+'\" or write to \"'
#                            +path+'\"\t'+ltime+'\t'+str(msg)+'\n')
