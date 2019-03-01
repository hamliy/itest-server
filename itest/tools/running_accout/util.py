# encoding: utf-8
"""
@author: han.li
@file  : util.py
@time  : 1/30/19 5:12 PM
@dec   : 
"""
import time
import random

def get_random_timestamp(day=0,):
    if day != 0:
        return int(round(time.time() * 1000)) - day*24*60*60*1000
    else:
        return  int(round(time.time() *1000)) - random.randint(1000,86400000)

def get_random_str_number(start, end):
    return str(random.randint(100000, 1000000))

def time_str_to_stamp(time_str):
    timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    # 转换为时间戳:
    return int(time.mktime(timeArray))*1000

def time_stamp_to_str(time_stamp):
    time_s = int(int(time_stamp)/1000)
    time_array = time.localtime(time_s)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_array)

if __name__ == '__main__':
    a= '1381419601000'
    print(time_stamp_to_str(a))

