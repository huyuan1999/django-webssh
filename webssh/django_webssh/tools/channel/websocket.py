from channels.generic.websocket import WebsocketConsumer
from django_webssh.tools.ssh import SSH
from django.http.request import QueryDict
from django_webssh import models
from django.utils.six import StringIO
import json
import base64


class WebSSH(WebsocketConsumer):
    status = {'code': 1001, 'error': ''}

    def connect(self):
        self.accept()

        query_string = self.scope['query_string']
        connet_argv = QueryDict(query_string=query_string, encoding='utf-8')
        unique = connet_argv.get('unique')
        width = connet_argv.get('width')
        height = connet_argv.get('height')

        width = int(width)
        height = int(height)

        connect_info = models.HostTmp.objects.get(unique=unique)

        host = connect_info.host
        port = connect_info.port
        user = connect_info.user
        auth = connect_info.auth
        pwd = connect_info.password

        if pwd:
            password = base64.b64decode(pwd).decode('utf-8')
        else:
            password = None

        self.ssh = SSH(websocker=self)

        if auth == 'key':
            pkey = connect_info.pkey
            obj = StringIO()
            obj.write(pkey)
            obj.flush()
            obj.seek(0)
            self.pkey = obj

            self.ssh.connect(
                host=host,
                user=user,
                password=password,
                pkey=self.pkey,
                port=port,
                pty_width=width,
                pty_height=height
            )
        else:
            self.ssh.connect(
                host=host,
                user=user,
                password=password,
                port=port,
                pty_width=width,
                pty_height=height
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
