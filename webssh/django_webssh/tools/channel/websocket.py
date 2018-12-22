from channels.generic.websocket import WebsocketConsumer
from django_webssh.tools.ssh import SSH
from urllib import parse
import json
import base64

class WebSSH(WebsocketConsumer):

    status = {'code':1001, 'error':''}

    def connect(self):
        self.accept()

        query_string = self.scope['query_string']
        connet_info = parse.parse_qs(query_string.decode('utf-8'))

        host = connet_info.get('host')
        port = connet_info.get('port')
        user = connet_info.get('user')
        auth = connet_info.get('auth').pop()
        pkey = connet_info.get('pkey')
        password = connet_info.get('password')

        if not host or not port or not user:
            print('主机、端口和用户名不能为空')
            self.status['error'] = '主机、端口和用户名不能为空'
            self.send(json.dumps(self.status))
            self.close()
        else:
            self.ssh = SSH(websocker=self)
            if auth == 'key':
                if not pkey:
                    print('请指定秘钥文件')
                    self.status['error'] = '请指定秘钥文件'
                    self.send(json.dumps(self.status))
                    self.close()
                else:
                    if password:
                        pwd = password[0]
                        password = base64.b64decode(pwd)
                    else:
                        password = None

                    self.ssh.connect(
                        user=user[0],
                        password=password,
                        host=host[0],
                        pkey=pkey[0],
                        port=port[0],
                        pty_width=230,
                        pty_height=50
                    )
            else:
                if not password:
                    print('请输入密码')
                    self.status['error'] = '请输入密码'
                    self.send(json.dumps(self.status))
                    self.close()
                else:
                    self.ssh.connect(
                        user=user[0],
                        password=base64.b64decode(password[0]),
                        host=host[0],
                        port=port[0],
                        pty_width=230,
                        pty_height=50
                    )

    def disconnect(self, close_code):
        try:
            self.ssh.close()
        except:
            pass

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if type(data) == dict:
            data = data['data']
            self.ssh.shell(data)