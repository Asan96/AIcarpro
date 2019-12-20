#!/usr/bin/env python
# coding=utf-8
import os
from datetime import datetime

path_lst = ['F:\\aicar\\AIcarpro\\car\\test.py', 'F:\\aicar\\AIcarpro\\car\\test3.py']

def clear_log(dirs=path_lst):
    for path in dirs:
        size = os.path.getsize(path)/1024/1024  # 获取文件大小 MB为单位
        if size > 10:
            print('log file is too big, will clear it')
            with open(path, "w+") as f:
                f.truncate()
        else:
            continue
    print(str(datetime.now()))
if __name__ == '__main__':
    clear_log()
