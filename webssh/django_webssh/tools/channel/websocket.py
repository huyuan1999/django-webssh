from channels.generic.websocket import WebsocketConsumer
from django_webssh.tools.ssh import SSH
from django.http.request import QueryDict
from django_webssh.tools import tools
import json
import base64


class WebSSH(WebsocketConsumer):
    status = {'code': 1001, 'error': ''}

    def connect(self):
        self.accept()

        query_string = self.scope['query_string']
        connet_info = QueryDict(query_string=query_string, encoding='utf-8')
        obj = tools.ValidationData(connet_info)

        if obj.is_valid():
            self.ssh = SSH(websocker=self)
            host = obj.data.get('host')
            port = int(obj.data.get('port'))
            user = obj.data.get('user')
            auth = obj.data.get('auth')
            pkey = obj.data.get('pkey')
            passwd = obj.data.get('password')
            if passwd:
                password = base64.b64decode(passwd)
            else:
                password = None
        else:
            print(obj.errors.as_json())
            self.send('出现错误')
            self.close()
            return

        if auth == 'key':
            if pkey:
                self.ssh.connect(
                    host=host,
                    user=user,
                    password=password,
                    pkey=pkey,
                    port=port,
                    pty_width=200,
                    pty_height=50
                )
            else:
                self.send('key connect 出现错误')
                self.close()
                return

        elif auth == 'pwd':
            if password:
                self.ssh.connect(
                    host=host,
                    user=user,
                    password=password,
                    port=port,
                    pty_width=200,
                    pty_height=50
                )
            else:
                self.send('pwd connect 出现错误')
                self.close()
                return

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
