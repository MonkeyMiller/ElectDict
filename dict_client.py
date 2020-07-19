from socket import *
import sys
import getpass
HOST = "127.0.0.1"
PORT = 8890
ADDR = (HOST,PORT)
sockfd = socket()
try:
    sockfd.connect(ADDR)
except KeyboardInterrupt:
    sys.exit("客户端断开")
def do_query(phone):
    while True:
        word = input("请输入单词 ##退出查询：")
        if word == "##":
            return
        data = "Q %s %s" % (phone,word)
        print(data)
        sockfd.send(data.encode())
        print("信息已发送")
        meaning = sockfd.recv(1024)
        if not meaning:
            continue
        else:
            print(meaning.decode())
def do_history(phone):
    data = "H %s" % (phone)
    sockfd.send(data.encode())
    while True:
        history = sockfd.recv(1024)
        if history == "##":
            break
        print(history.decode())
def login(phone):
    while True:
        print("==================%s===================")
        print("=      1、查单词 2、查历史 3、退出    =")
        print("=======================================")
        cmd = input("Command:")
        if cmd.strip() == '1':
            do_query(phone)
        elif cmd.strip() == '2':
            do_history(phone)
        elif cmd.strip() == '3':
            break
        else:
            print("请输入正确命令!")
def do_regist():
    while True:
        phone = input("请输入手机号 ：")
        if len(phone)>11 or not phone.isdigit():
            print("请输入正确的手机号： ")
            continue
        name = input("请输入昵称 ：")
        passwd =getpass.getpass("请输入密码 ：")
        passwd1 = getpass.getpass("请再次确认密码 ：")
        if passwd != passwd1 or " " in (name or passwd):
            print("昵称和密码不要有空格")
            continue
        data = "R %s %s %s"%(phone,name,passwd)
        sockfd.send(data.encode())
        status = sockfd.recv(1024)
        if not status:
            return
        else:
            login(phone)
            print(status.decode())

def do_login():
    while True:
        phone = input("请输入手机号 ：")
        if len(phone) > 11 or not phone.isdigit():
            print("请输入正确的手机号： ")
            continue
        passwd = getpass.getpass("请输入密码 ：")
        if " " in passwd:
            continue
        data = "L %s %s"%(phone,passwd)
        sockfd.send(data.encode())
        status = sockfd.recv(1024)
        if not status:
            return
        else:
            login(phone)
            print(status.decode())
def run():
    while True:
        print("==================首页=================")
        print("=      1、注册 2、登录 3、退出        =")
        print("=======================================")
        cmd = input("Command:")
        if cmd.strip() == '1':
            do_regist()
        elif cmd.strip() == '2':
            do_login()
        elif cmd.strip() == '3':
            sys.exit()
        else:
            print("请输入正确命令!")

if __name__ == '__main__':
    run()