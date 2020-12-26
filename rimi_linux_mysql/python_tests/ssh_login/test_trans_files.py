import os
import sys
import paramiko
#文件传输链接
t = paramiko.Transport('10.2.1.64', 22)
t.connect(username='students', password='123456')
#传输文件
sftp = paramiko.SFTPClient.from_transport(t)

#from to
sftp.put('test.logs', '/Users/students/test_log.log')
t.close()
#
# sftp.get('/Users/canvas/test_log.log', 'log2.log')
# t.close()