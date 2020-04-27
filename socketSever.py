from socket import *
from time import ctime
from qiandao import qiandao
import logging

file = open('config.json','r',encoding='utf-8')
config=json.load(file)
usrname = config['usrname']
usrdata = config['usrdata']

HOST = ''
PORT = 4396
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

def logger_config(log_path, logging_name):
    logger = logging.getLogger(logging_name)
    logger.setLevel(level=logging.DEBUG)
    handler = logging.FileHandler(log_path, encoding='UTF-8')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger

while True:
    print('等待连接...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('来自于:', addr)
    while True:
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        ans = "请求签到码为"+str(bytes.decode(data)) + "(注意有无空格)\n"
        for i in range(len(usrname)):
            try:
                state = 400
                while (state == 400):
                    state = qiandao(bytes.decode(data), usrdata[i])
                    if (state == 400):
                        continue
                    elif (state == 401):
                        ans = ans + usrname[i] + ":签到码失效\n"
                        break
                    else:
                        ans = ans + usrname[i] + ":签到成功\n"
                        break
            except BaseException:
                ans = ans + usrname[i] + ":账号异常(签到过多)\n"
        logger = logger_config(log_path='log.txt', logging_name=ans)
        logger.info("info")
        tcpCliSock.send(('[%s]\n%s' % (ctime(), ans)).encode())
    tcpCliSock.close()
tcpSerSock.close()
