import socket,select
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 13029))
s.listen(10)
s.setblocking(False)
wlist = []
rlist = []
errlist = []
msg_dict = dict()
rlist.append(s)

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
                msg_dict[i] = data
                print('收到信息: ', data.decode('utf8'))
                if not data:
                    i.close()
                    rlist.remove(i)
                    continue
                wlist.append(i)
                rlist.remove(i)
            except Exception:
                i.close()
                rlist.remove(i)
    for i in write_list:
        try:
            i.send(msg_dict[i])
            rlist.append(i)
        except Exception:
            i.close()
        finally:
            wlist.remove(i)
            del(msg_dict[i])
