import paramiko
import os
#找到公钥的地址 / \
# private_key_path = '/Users/canvas/.ssh/id_rsa'
# private_key_path = os.path.join('Users','canvas','.ssh','id_rsa')
# #把公钥加载进入paramiko框架
# key = paramiko.RSAKey.from_private_key_file(private_key_path)
# #初始化paraiko客户端
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# #ssh免密链接
# ssh.connect('111.231.203.174', 22, 'root', key)
# #打印出标准输出
# stdin, stdout, stderr = ssh.exec_command('df -hT')
# print(stdout.read())
# ssh.close()


private_key_path = '/Users/canvas/.ssh/id_rsa'
key = paramiko.RSAKey.from_private_key_file(private_key_path)

t = paramiko.Transport(('111.231.203.174', 22))
t.connect(username='root', pkey=key)

sftp = paramiko.SFTPClient.from_transport(t)
sftp.put('test.logs', '/root/log.log')

t.close()
