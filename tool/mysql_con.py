import pymysql
import re

def my_con(target_list):
    sql = "insert into dict VALUES (%s,%s)"
    conn = pymysql.connect(host='192.168.3.95',port=3306,user = "root",passwd = "123456",charset='utf8')
    cursor = conn.cursor()
    cursor.execute("drop database if EXISTS stu")
    cursor.execute("create database stu")
    cursor.execute("use stu")
    try:
        cursor.execute("drop table if EXISTS dict")
    except Exception:
        pass
    cursor.execute("create table dict(sourword VARCHAR (30),wordmean VARCHAR (255))")
    # for i in target_list:
    #     sql = "insert into dict VALUES (%s,%s)" % (i[0],i[1])
    cursor.executemany(sql,target_list)
    cursor.execute("create table users(phone int(11) primary key,name varchar(30),pwd varchar(128))")
    cursor.execute("commit")
    cursor.close()
    conn.close()

def get_list():
    target_list = []
    f = open("dict.txt","r",encoding="utf-8")
    data = f.readlines()
    for i in data:
        s = i.split(" ",1)
        # print(s[1])
        s2 = re.findall(r' +(.*?)\n',s[-1])
        # s2 = s[1].strip()
        if s2:
             # print(s2)
            target_list.append((s[0],s2[0]))
    return target_list


if __name__ == '__main__':
    a=get_list()

    my_con(a)
