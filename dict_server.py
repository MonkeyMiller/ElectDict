from socket import *
import sys
from Users import *
from multiprocessing import Process
HOST = "127.0.0.1"
PORT = 8890
ADDR = (HOST,PORT)
def connect(conn):
    user = Users()
    while True:
        data = conn.recv(1024)
        if not data:
            sys.exit()
        else:
            data = data.decode()
            print(data)
            info = data.split(" ")
            if info[0] == "R":

                if user.regist(info[1],info[2],info[3]):
                    conn.send(b"OK")
                else:
                    conn.send(b"fail to regist")
            elif info[0] == "L":
                if user.login(info[1],info[2]):
                    conn.send(b"OK")
                else:
                    conn.send(b"fail to login")
            elif info[0] == "Q":
                print(info)
                r = user.query_word(info[1], info[2])
                print("测试这一步")
                if not r:
                    conn.send(b"fail to find")
                else:
                    print(r)
                    conn.send(r.encode())

def main():
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(5)
    print('服务器已经启动！')
    while True:
        try:
            conn,addr = sockfd.accept()
            print("Connect from ",addr)
        except KeyboardInterrupt as e:
            print(e)
        except Exception as e:
            print(e)

        p = Process(target=connect,args=(conn,))
        p.daemon = True
        p.start()
if __name__ == '__main__':
    main()