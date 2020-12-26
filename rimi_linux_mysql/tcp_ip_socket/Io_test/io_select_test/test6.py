import socket,select
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 13015))
s.listen(10)
import six

s.setblocking(False)
wlist = []
rlist = []
errlist = []
rlist.append(s)
msg_dict = dict()
while True:
    read_list, write_list, e_list = select.select(rlist,wlist,errlist,2)
    for i in read_list:
        if i is s:
            try:
                conn, addr = i.accept()
                conn.setblocking(False)
                rlist.append(conn)
            except Exception:
                pass
        else:
            try:
                data = i.recv(1024)
                #string
                # i.send('asdf')
                msg_dict[i] = data
                rlist.remove(i)
                wlist.append(i)
                print('收到信息: ', data.decode('utf8'))
                if not data:
                    i.close()
                    rlist.remove(i)
            except Exception:
                i.close()
                try:
                    rlist.remove(i)
                except Exception:
                    pass
    for i in write_list:
        try:
            i.send(msg_dict[i])
            rlist.append(i)
        except Exception:
            i.close()
        finally:
            del(msg_dict[i])
            wlist.remove(i)



