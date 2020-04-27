from socket import *
from time import ctime
from qiandao import qiandao
import logging

usrname = ["xwh", "xd"]
usrdata = ["fa46b599-6ec7-4621-b9e2-cde380035faa", "760107f9-0b50-405b-bc4c-b82fa60b1cc5"]

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

def logger_config(log_path, logging_name):
    '''
    配置log
    :param log_path: 输出log路径
    :param logging_name: 记录中name，可随意
    :return:
    '''
    '''
    logger是日志对象，handler是流处理器，console是控制台输出（没有console也可以，将不会在控制台输出，会在日志文件中输出）
    '''
    # 获取logger对象,取名
    logger = logging.getLogger(logging_name)
    # 输出DEBUG及以上级别的信息，针对所有输出的第一层过滤
    logger.setLevel(level=logging.DEBUG)
    # 获取文件日志句柄并设置日志级别，第二层过滤
    handler = logging.FileHandler(log_path, encoding='UTF-8')
    handler.setLevel(logging.INFO)
    # 生成并设置文件日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # console相当于控制台输出，handler文件输出。获取流句柄并设置日志级别，第二层过滤
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # 为logger对象添加句柄
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
        print('[%s]\n%s' % (ctime(), ans))
        tcpCliSock.send(('[%s]\n%s' % (ctime(), ans)).encode())
    tcpCliSock.close()
tcpSerSock.close()
