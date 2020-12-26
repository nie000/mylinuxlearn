import paramiko
import os


def remote_upload(host, username, private_key, remote_path, local_path, port):
    key = paramiko.RSAKey.from_private_key_file(private_key)
    h = paramiko.Transport(host, port)
    h.connect(username=username, pkey=key)
    sftp = paramiko.SFTPClient.from_transport(h)
    sftp.put(local_path, remote_path)
    h.close()


if __name__ == '__main__':
    private_key_path = os.path.join('/Users', 'canvas', '.ssh', 'id_rsa')
    # 把公钥加载进入paramiko框架
    host = '176.122.175.246'
    port = 29371
    username = 'root'
    local_path = 'test.logs'
    remote_path = '/Users/canvas/test_log.log'

    remote_upload(host, username, private_key_path, local_path, remote_path, port)
