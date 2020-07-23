# coding:utf-8

"""
################多进程
import os

print('Process (%s) start...' % os.getpid())
# Only works on Unix/Linux/Mac:
pid = os.fork()
if pid == 0:
    print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
else:
    print('I (%s) just created a child process (%s).' % (os.getpid(), pid))
"""

'''
#################多进程
from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
'''

'''
#################批量创建子进程
##对Pool对象调用join()方法会等待所有子进程执行完毕，调用join()之前必须先调用close()，调用close()之后就不能继续添加新的Process了。
from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(5) #Pool的默认大小是CPU的核数
    for i in range(10):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
'''


'''
#################外部子进程
import subprocess

print('$ nslookup www.python.org')
r = subprocess.call(['nslookup', 'www.python.org'])
print('Exit code:', r)
'''

'''
#################外部子进程输入
### 代码相当于在命令行执行命令nslookup，然后手动输入：
### set q=mx
### python.org
### exit

import subprocess
print('$ nslookup')
p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
print(output.decode('utf-8'))
print('Exit code:', p.returncode)
'''

'''
#################进程间通信
from multiprocessing import Process, Queue
import os, time, random

# 写数据进程执行的代码:
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

# 读数据进程执行的代码:
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)

if __name__=='__main__':
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入:
    pw.start()
    # 启动子进程pr，读取:
    pr.start()
    # 等待pw结束:
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()
'''
'''多线程和多进程最大的不同在于，多进程中，同一个变量，各自有一份拷贝存在于每个进程中，互不影响，
而多线程中，所有变量都由所有线程共享，所以，任何一个变量都可以被任何一个线程修改'''

'''
#################创建多线程
### 启动一个线程就是把一个函数传入并创建Thread实例，然后调用start()开始执行
import time, threading
# 创建并启动一个新线程
def loop():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop, name='')
t.start()
t.join()
print('thread %s ended.' % threading.current_thread().name)
'''

'''
#################多个线程同时操作一个变量
import time, threading

# 假定这是你的银行存款:
balance = 0

def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(10000):
        change_it(n)

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)
'''

'''
#################线程锁
import time, threading
# 假定这是你的银行存款:
balance = 0
lock = threading.Lock()
def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(100000):
        # 先要获取锁:
        lock.acquire()
        try:
            # 放心地改吧:
            change_it(n)
        finally:
            # 改完了一定要释放锁:
            lock.release()

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)
'''

'''Python的线程虽然是真正的线程，但解释器执行代码时，有一个GIL锁：Global Interpreter Lock，任何Python线程执行前，必须先获得GIL锁，然后
，每执行100条字节码，解释器就自动释放GIL锁，让别的线程有机会执行。这个GIL全局锁实际上把所有线程的执行代码都给上了锁，所以，多线程在Python中
只能交替执行，即使100个线程跑在100核CPU上，也只能用到1个核。
GIL是Python解释器设计的历史遗留问题，通常我们用的解释器是官方实现的CPython，要真正利用多核，除非重写一个不带GIL的解释器。
所以，在Python中，可以使用多线程，但不要指望能有效利用多核。如果一定要通过多线程利用多核，那只能通过C扩展来实现，不过这样就失去了Python简单易
用的特点。
不过，也不用过于担心，Python虽然不能利用多线程实现多核任务，但可以通过多进程实现多核任务。多个Python进程有各自独立的GIL锁，互不影响。'''


'''
#####################图像处理标准库
#PIL：Python Imaging Library
from PIL import Image,ImageFilter

# 打开一个jpg图像文件，注意是当前路径:
im = Image.open('test.png')
# 获得图像尺寸:
w, h = im.size
print('Original image size: %sx%s' % (w, h))
# 缩放到50%:
im.thumbnail((w//2, h//2))
print('Resize image to: %sx%s' % (w//2, h//2))
# 把缩放后的图像用jpeg格式保存:
im.save('thumbnail.jpg', 'jpeg')

# 应用模糊滤镜:
im2 = im.filter(ImageFilter.BLUR)
im2.save('blur.jpg', 'jpeg')
'''


'''
############################生成随机验证码图片
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import random
import string

# 随机字码:
def rndChar():
    n = random.randint(48, 57),random.randint(65, 90),random.randint(97, 122)
    #n = string.digits + string.ascii_uppercase + string.ascii_lowercase
    return chr(random.choice(n))

# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

# 创建图片 240 x 60:cd 
width = 60 * 4
height = 60
image = Image.new('RGB', (width, height), (255, 255, 255))
# 创建Font对象:
font = ImageFont.truetype('/usr/share/fonts/truetype/abyssinica/AbyssinicaSIL-R.ttf', 36)
# 创建Draw对象:
draw = ImageDraw.Draw(image)
# 填充每个像素颜色:
for x in range(width):
    for y in range(height):
        draw.point((x, y), fill=rndColor())
# 输出文字:
for t in range(4):
    draw.text((60 * t + 10, 10), rndChar(), font=font, fill=rndColor2())
# 模糊处理:
#image = image.filter(ImageFilter.BLUR)
image.save('./code.jpg', 'jpeg')
'''


'''
import requests

r = requests.get('https://www.douban.com/', headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'})
print(r.status_code,r.encoding)


#GET请求
r = requests.get('https://www.douban.com/') 
###带参数的GET，传入一个dict作为params参数：
r = requests.get('https://www.douban.com/search', params={'q': 'python', 'cat': '1001'})

#POST请求
#发送POST请求，只需要把get()方法变成post()，然后传入data参数作为POST请求的数据
r = requests.post('https://accounts.douban.com/login', data={'form_email': 'abc@example.com','form_password':'123456'})
###requests默认使用application/x-www-form-urlencoded对POST数据编码。如果要传递JSON数据，可以直接传入json参数：
params = {'key': 'value'}
r = requests.post(url, json=params) # 内部自动序列化为JSON

###需要传入HTTP Header时，我们传入一个dict作为headers参数：
r = requests.get('https://www.douban.com/', headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'})
'''


'''
##############chardet
import chardet
###用chardet对一个bytes检测编码
str1 = '离离原上草，一岁一枯荣'.encode('gbk')
str2 = b'Hello, world!'
print(chardet.detect(str1))
print(chardet.detect(str2))
print(str1,str1.decode('gbk'),str2,str2.decode('utf-8'))
'''


'''
# ################ 系统信息 process and system utilities
import psutil
print('CPU逻辑数量:', psutil.cpu_count())  # CPU逻辑数量
print('CPU物理核心:', psutil.cpu_count(logical=False))    # CPU物理核心
print('统计CPU的用户／系统／空闲时间：', psutil.cpu_times())
# print('CPU使用率:', psutil.cpu_percent(interval=1, percpu=True))
print('物理内存信息:', psutil.virtual_memory())
print('磁盘分区信息:', psutil.disk_partitions())
print('磁盘使用情况:', psutil.disk_usage('/'))
print('获取网络接口信息:', psutil.net_if_addrs())
print('获取网络接口状态:', psutil.net_if_stats())
print('网络连接信息:', psutil.net_connections())
print('所有进程ID:', psutil.pids())
# print(psutil.test())
'''


'''
# ########### 图形界面库 Tkinter
from tkinter import *
import tkinter.messagebox as messagebox

class Application(Frame):
    def __init__(self, main=None):
        Frame.__init__(self, main)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertButton = Button(self, text='Hello', command=self.hello)
        self.alertButton.pack()

    def hello(self):
        name = self.nameInput.get() or 'world'
        messagebox.showinfo('Message', 'Hello, %s' % name)

app = Application()
# 设置窗口标题:
app.main.title('Hello World')
# 主消息循环:
app.mainloop()
'''


'''
import socket

# 创建一个socket: AF_INET指定使用IPv4协议, IPv6指定为AF_INET6,SOCK_STREAM指定使用面向流的TCP协议
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('www.sina.com.cn', 80))  # 建立连接

# 发送数据:
s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')

# 接收数据:
buffer = []
while True:
    # 每次最多接收1k字节:
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break
data = b''.join(buffer)

# 接收到的数据包括HTTP头和网页本身,把HTTP头和网页分离,把HTTP头打印出来,网页内容保存到文件：
header, html = data.split(b'\r\n\r\n', 1)
print(header.decode('utf-8'))
# 把接收的数据写入文件:
with open('./html_file/sina.html', 'wb') as f:
    f.write(html)

# 关闭连接:
s.close()
'''


'''
# ################################### 发送邮件
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


from_addr = input('From: ')
password = input('Password: ')
to_addr = input('To: ')
smtp_server = input('SMTP server: ')

# 构造MIMEText对象时, 第一个参数是邮件正文, 第二个参数是MIME的subtype,'plain'表示纯文本,
# 最终的MIME就是'text/plain', 最后一定要用utf-8编码保证多语言兼容性. 
msg = MIMEText('send by python code test...', 'plain', 'utf-8')
msg['From'] = _format_addr('Python code test <%s>' % from_addr)
msg['To'] = _format_addr('zhong <%s>' % to_addr)
msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
'''


'''
# #################################### 获取邮件
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

import poplib

# 输入邮件地址, 口令和POP3服务器地址:
email = input('Email: ')
password = input('Password: ')
pop3_server = input('POP3 server: ')


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))

    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))


# 连接到POP3服务器:
server = poplib.POP3(pop3_server)
# 可以打开或关闭调试信息:
server.set_debuglevel(1)
# 可选:打印POP3服务器的欢迎文字:
print(server.getwelcome().decode('utf-8'))
# 身份认证:
server.user(email)
server.pass_(password)
# stat()返回邮件数量和占用空间:
print('Messages: %s. Size: %s' % server.stat())
# list()返回所有邮件的编号:
resp, mails, octets = server.list()
# 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
print(mails)
# 获取最新一封邮件, 注意索引号从1开始:
index = len(mails)
resp, lines, octets = server.retr(index)
# lines存储了邮件的原始文本的每一行,
# 可以获得整个邮件的原始文本:
msg_content = b'\r\n'.join(lines).decode('utf-8')
# 稍后解析出邮件:
msg = Parser().parsestr(msg_content)
print_info(msg)
# 可以根据邮件索引号直接从服务器删除邮件:
# server.dele(index)
# 关闭连接:
server.quit()
'''


'''
import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
# cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
# cursor.execute('insert into user (id, name) values (\'1\', \'Michael\')')
print(cursor.rowcount)
data = cursor.execute('select * from user where id=?', ('1',)).fetchall()
print(data)
cursor.close()
conn.commit()
conn.close()
'''


'''
# 导入MySQL驱动:
import mysql.connector
# 创建mysql连接
conn = mysql.connector.connect(user='root', password='root', database='test')
cursor = conn.cursor()
# 创建user表:
# cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
# 插入一行记录，注意MySQL的占位符是%s:
# cursor.execute('insert into user (id, name) values (%s, %s)', ['3', 'Linda'])
# 提交事务:
conn.commit()

# 查询:
cursor.execute('select * from user ')
result = cursor.fetchall()
print(result)
# 关闭Cursor和Connection:
cursor.close()
conn.close()
'''


'''
# ########################## ORM(Object-Relational Mapping)框架之SQLAlchemy
# ### 把关系数据库的表结构映射到对象上
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))


# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/test')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# #######有了ORM，我们向数据库表中添加一行记录，可以视为添加一个Class对象
# #######关键是获取session,然后把对象添加到session,最后提交并关闭.DBSession对象可视为当前数据库连接.
# 创建session对象:
session = DBSession()
# 创建User对象:
# new_user = User(id='4', name='Bob')
# 添加到session:
# session.add(new_user)
# 提交到数据库:
# session.commit()
# 关闭session:
session.close()

# ########查询数据
# 创建Session:
session = DBSession()
# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
user = session.query(User).filter(User.id == '4').one()
users = session.query(User).all()
# 打印类型和对象的name属性:
print('type:', type(user))
print('name:', user.name)
for u in users:
    print('id:', u.id, 'name:', u.name)
# 关闭Session:
session.close()
'''


'''
# ######### consumer函数是一个generator，把一个consumer传入produce后：
#
#     首先调用c.send(None)启动生成器；
#
#     然后，一旦生产了东西，通过c.send(n)切换到consumer执行；
#
#     consumer通过yield拿到消息，处理，又通过yield把结果传回；
#
#     produce拿到consumer处理的结果，继续生产下一条消息；
#
#     produce决定不生产了，通过c.close()关闭consumer，整个过程结束。
#
# 整个流程无锁，由一个线程执行，produce和consumer协作完成任务
def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'


def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()


c = consumer()
produce(c)
'''


'''
def triangles():
    t = [1]
    while True:
        yield t
        t.append(0)
        t = [t[i-1]+t[i] for i in range(len(t))]

    # L = [1]  # 初始值
    # while True:
    #    yield (L)
    #    k = [L[j] + L[j + 1] for j in range(len(L)-1)
    #    L = [1] + k + [1]


n = 0
results = []
result = []
for t in triangles():
    print(t)
    results.append(t[:])  # results.append(t) ???????????????
    result.append(t)
    n = n + 1
    if n == 10:
        break
print(results)
print(result)
if results == [
    [1],
    [1, 1],
    [1, 2, 1],
    [1, 3, 3, 1],
    [1, 4, 6, 4, 1],
    [1, 5, 10, 10, 5, 1],
    [1, 6, 15, 20, 15, 6, 1],
    [1, 7, 21, 35, 35, 21, 7, 1],
    [1, 8, 28, 56, 70, 56, 28, 8, 1],
    [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
]:
    print('测试通过!')
else:
    print('测试失败!')
'''
























