# python paramiko

## 概述

关于ssh登录python的paramiko库也提供了ssh的登录功能,我们可以通过paramiko库更加深入的了解ssh登录

## 使用方式

1. 密码登录

	```
	
	import paramiko
	#new出来一个ssh客户端
	ssh_client = paramiko.SSHClient()
	#ssh需要询问是否加入key,为了不让那一步把程序卡住,这个条件会设置自动添加key
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	#让ssh客户端去使用账户密码连接远程服务器
	ssh_client.connect('127.0.0.1',22,'canvas','tusbasa1')
	#执行命令
	cmd = 'ls /;pwd'
	#解包标准输出
	stdin,stdout,stderr = ssh_client.exec_command(cmd)
	
	for line in stdout:
	    print(line)
	    
	```
2. 免密登录

    ```
    import paramiko
	
	#找到公钥的地址
	private_key_path = '/Users/canvas/.ssh/id_rsa'
	#把公钥加载进入paramiko框架
	key = paramiko.RSAKey.from_private_key_file(private_key_path)
	#初始化paraiko客户端
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	#ssh免密链接
	ssh.connect('111.231.203.174', 22, 'root', key)
	#打印出标准输出
	stdin, stdout, stderr = ssh.exec_command('df -h')
	print(stdout.read())
	ssh.close()
    ```
3. 文件传输

    ```
    import paramiko
	#文件传输链接
	t = paramiko.Transport('127.0.0.1', 22)
	t.connect(username='rimi', password='mima')
	#传输文件
	sftp = paramiko.SFTPClient.from_transport(t)
	
	#from to
	sftp.put('test.logs', '/Users/canvas/test_log.log')
	t.close()
	
	sftp.get('/Users/canvas/test_log.log', 'log2.log')
t.close()
    ```
    
4. 免密传输

	```
	private_key_path = '/Users/canvas/.ssh/id_rsa'
	key = paramiko.RSAKey.from_private_key_file(private_key_path)
	
	t = paramiko.Transport(('111.231.203.174', 22))
	t.connect(username='root', pkey=key)
	
	sftp = paramiko.SFTPClient.from_transport(t)
	sftp.put('test.logs', '/root/log.log')
	
	t.close()
	```
	
