import pymysql
import hashlib
def jm(pwd):
    salt = "!@#$"
    hash = hashlib.md5(salt.encode())#产生加密对象
    hash.update(pwd.encode())#加密处理
    re = hash.hexdigest()
    print(re)
    return re

class Users():
    def __init__(self):
        self.db = pymysql.connect(host="192.168.3.95",port=3306,\
                                  user ="root",passwd="123456",charset="utf8",database="stu")
        self.cur = self.db.cursor()

    def regist(self,phone,name,pwd):
        sql = "insert into users values (%s,%s,%s)"
        select_sql = "select name from users where phone = %s"
        print(phone)
        self.cur.execute(select_sql,[phone])
        r = self.cur.fetchone()
        if r:
            print("执行这一步")
            return False
        pwd = jm(pwd)
        print("加密")
        try:
            self.cur.execute(sql,[phone,name,pwd])
            print("插入数据")
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
    def login(self,phone,pwd):
        pwd = jm(pwd)
        sql = "select pwd from users where phone = %s"
        self.cur.execute(sql, [phone])
        r = self.cur.fetchone()
        if r[0] == pwd:
            return True

    def query_word(self,phone,word):
        sql = "select * from dict where sourword = %s"
        inssql = "insert into histo values (%s,%s)"
        self.cur.execute(sql,[word])
        r = self.cur.fetchone()
        if r:
            try:
                self.cur.execute(inssql,[phone,word])
                self.db.commit()
            except:
                self.db.rollback()
            print(r[1])
            r = r[1]
            return r



if __name__ == '__main__':
    u =Users()
    u.query_word(15990030825,"exit")