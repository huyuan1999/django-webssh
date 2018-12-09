from channels.generic.websocket import WebsocketConsumer
from django_webssh.tools.ssh import SSH
import json

class WebSSH(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.ssh = SSH(websocker=self)
        # 作为测试, 生成业务建议从数据库查询或者获取前端页面给定的值
        self.ssh.connect(
            user='root',
            password='123',
            host='127.0.0.1',
            pty_width=238,
            pty_height=57
        )

    def disconnect(self, close_code):
        self.ssh.close()

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if type(data) == dict:
            data = data['data']
            self.ssh.shell(data)