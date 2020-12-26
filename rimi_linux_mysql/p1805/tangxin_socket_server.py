import select
from socket import *
class Qq_group:
    def __init__(self):
        self.ss=socket(AF_INET,SOCK_STREAM)
        self.ss.bind(('127.0.0.1',8080))
        self.ss.listen(128)


    def run(self):
        while 1:
            rlist,wlist,errorlist=select.select(self.socketlist,[],[])
            for sock in rlist:
                if sock==self.ss:
                     newsocket,addr=self.ss.accept()
                     #可以把套接字和地址放在一个元祖里面，给socketlist，不知道会不会返回哦，不会返回就以字典的形式存在另一个列表里，等发消息的时候再寻址
                     self.socketlist.append(newsocket)

                     newsocket.send('请输入QQ群密码（提示abc）：'.encode())
                     cont = newsocket.recv(1024)
                     if cont==b'abc':
                         newsocket.send('密码正确'.encode())
                     else:
                         try:
                            newsocket.send('密码错误，拜拜'.encode())
                         except Exception:
                             #防止对方关了,发布过去了
                             pass
                         print('----------------')
                         self.socketlist.remove(newsocket)
                         newsocket.close()
                else:
                    cont = sock.recv(1024)
                    print(cont)
                    if len(cont) != 0:
                        # 没存地址，一辈子不知道谁发的
                        # for temp in self.socketlist:
                        #     if temp!=self.ss:
                        #         temp.send(cont)
                        list(map(lambda x: x.send(cont),self.socketlist[1::]))
                    else:
                        print('一个客户端下线啦')
                        self.socketlist.remove(sock)
                        sock.close()

if __name__ == '__main__':
    qq_group=Qq_group()
    print('-----------------start-------------')
    qq_group.run()
    #因为错误在errolist中暂时搞不定，怎么精准拿出来
    #另外为啥客户端意外关闭后就gg了，不知道错误到哪儿去了