import paramiko
#new出来一个ssh客户端
ssh_client = paramiko.SSHClient()
#ssh需要询问是否加入key,为了不让那一步把程序卡住,这个条件会设置自动添加key
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#让ssh客户端去使用账户密码连接远程服务器
ssh_client.connect('10.2.1.64',22,'students','123456')
#执行命令
cmd = 'ifconfig;ls;top;ls /;'
#解包标准输出

stdin,stdout,stderr = ssh_client.exec_command(cmd)

for line in stdout:
    print(line)
#
# a1,a2,a3,a4 = (1,2,4,56)