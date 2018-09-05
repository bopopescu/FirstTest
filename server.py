# coding:utf-8

import socket
import threading
import time

'''
# ################### TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 9999))             # 绑定监听的地址和端口
s.listen(5)                             # 开始监听端口,等待连接的最大数量为5
print('Waiting for connection...')


def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)


while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
'''


# ##################### UDP
# 创建一个socket: SOCK_DGRAM指定了Socket的类型是UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 9999))
print('Bind UDP on 9999...')


def UDPlink(data, addr):
    print('Received %s' % data, 'from %s:%s.' % addr)
    s.sendto(b'Hello, %s!' % data, addr)


while True:
    data, addr = s.recvfrom(1024)
    if not data:
        break
    # 创建新线程来处理UDP接收的信息:
    t = threading.Thread(target=UDPlink, args=(data, addr))
    t.start()



