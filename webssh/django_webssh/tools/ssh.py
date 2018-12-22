import paramiko
from threading import Thread
import socket
import json


class SSH:
    def __init__(self, websocker):
        self.websocker = websocker

    def connect(self, host, user, password, pkey=None, port=22, timeout=30, term='xterm', pty_width=80, pty_height=24):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if pkey:
                key = paramiko.RSAKey.from_private_key_file(pkey) or \
                      paramiko.DSSKey.from_private_key_file(pkey) or \
                      paramiko.ECDSAKey.from_private_key_file(pkey) or \
                      paramiko.Ed25519Key.from_private_key_file(pkey)
                ssh_client.connect(username=user, passphrase=password,
                                   hostname=host, port=port, pkey=key, timeout=timeout)
            else:
                ssh_client.connect(username=user, password=password,
                                   hostname=host, port=port, timeout=timeout)

            transport = ssh_client.get_transport()
            self.channel = transport.open_session()
            self.channel.get_pty(term=term, width=pty_width, height=pty_height)
            self.channel.invoke_shell()
            for i in range(2): self.websocker.send(json.dumps(self.channel.recv(1024).decode('utf-8')))
        except socket.timeout as e:
            print('ssh 连接超时, 关闭 websocker 连接')
            self.websocker.close()
        except Exception as e:
            print('发送未知错误:{}, 无法连接ssh, 关闭 websocker 连接'.format(str(e)))
            self.websocker.close()

    def django_to_ssh(self, data):
        try:
            self.channel.send(data)
            return
        except:
            self.close()

    def websocket_to_django(self):
        try:
            while True:
                data = self.channel.recv(1024).decode('utf-8')
                if not len(data):
                    return
                self.websocker.send(json.dumps(data))
        except:
            self.close()

    def close(self):
        self.channel.close()
        self.websocker.close()

    def shell(self, data):
        Thread(target=self.django_to_ssh, args=(data,)).start()
        Thread(target=self.websocket_to_django).start()
