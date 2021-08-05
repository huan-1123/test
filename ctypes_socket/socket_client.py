import socket
import traceback
import os


REMOTE_LOG_UNIX = "/var/remote_log_ser.sock"
REMOTE_LOG_UNIX_CLI = "/var/remote_log_cli_strategy.sock"
MAX_SIZE = 1

class ClientSocket(object):
    # 单例模式
    _first_init = False
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(ClientSocket, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not cls._first_init:
            self.file_addr = REMOTE_LOG_UNIX
            self.cli_addr = REMOTE_LOG_UNIX_CLI
            self.client = None
            cls._first_init = True

    # 选择连接方式，创建socket客户端连接
    def client_connect(self):
        try:
            self.client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            self.client.settimeout(0.1)
            if os.path.exists(self.cli_addr):
                # 解绑客户端连接地址
                os.unlink(self.cli_addr)
            # 绑定客户端连接地址
            self.client.bind(self.cli_addr)

        except Exception as e:
            print('socket client connect error {}.'.format(e) + traceback.format_exc())

    # 客户端socket的向服务端发送数据
    def client_send_data(self, data):
        try:
            if self.client == None:
                self.client_connect()

            self.client.sendto(data, self.file_addr)
            self.server_recv_data()
        except Exception as e:
            print('socket client send data error {}.'.format(e) + traceback.format_exc())

    def server_recv_data(self):
        try:
            data = self.client.recvfrom(MAX_SIZE)
            if data[0] != '\x00':
                print("send log error, data is {}".format(data))
        except Exception as e:
            print('server return data error {}.'.format(e) + traceback.format_exc())

    # 关闭客户端socket连接
    def client_close(self):
        if self.client == None:
            return
        else:
            self.client.close()