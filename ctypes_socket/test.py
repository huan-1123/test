from ctypes_socket.ctypes_data import LogCtypeData, FROM_CHANNEL
from ctypes_socket.socket_client import ClientSocket


def log_server(**kwargs):
    print(kwargs)
    log_object = LogCtypeData()
    ip = kwargs.get("ip")
    if not ip:
        kwargs["ip"] = "127.0.0.1"

    elif "," in ip:
        kwargs["ip"] = ip.split(",")[0]
    log_data_buf = log_object.encode_log(**kwargs)
    udp_client = ClientSocket()
    udp_client.client_send_data(log_data_buf)

if  __name__ == '__main__':
    log_server(log="thist is ok", platform=10, user="平台", ip="127.0.0.1")