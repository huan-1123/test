from ctypes import *
import struct
import socket
import traceback
# import os

"""
unsigned char from	日志来源				    MSG_FROM_WEBUI=0,MSG_FROM_RESTAPI=10
char user[USER_NAME_SIZE+1]	操作用户		    USER_NAME_SIZE = 252
unsigned int from_ip 来源ip                 int ip
int module  模块：资产模块					SG_LOG_MOD_PROPERTY=100
int type	日志类型：操作日志				SG_LOG_TYPE_OPERATE=0
int severity 日志级别：						SG_LOG_LEVEL_INFO=6
char log[SG_LOG_MSG_SIZE] 日志内容:	SG_LOG_MSG_SIZE=1024; 

"""

USER_NAME_SIZE = 252 + 1
SG_LOG_MSG_SIZE = 1024
FROM_CHANNEL = {
    "MSG_FROM_WEBUI": 0,
    "MSG_FROM_RESTAPI": 10
}

MAX_SIZE = 1


class LogCtypeData(Structure):
    _fields_ = [
        ("from_platform", c_ubyte),
        ("user", c_char*USER_NAME_SIZE),
        ("from_ip", c_uint),
        ("module", c_int),
        ("type", c_int),
        ("severity", c_int),
        ("log", c_char*SG_LOG_MSG_SIZE),
    ]

    # 判断字符长度是否超标准
    def char_size(self, char_data, data_length):
        try:
            data_bytes = char_data.encode("utf-8")
            if len(data_bytes) > data_length:
                return 0
            return data_bytes
        except Exception as e:
            print('char size length out of range error {}.'.format(e) + traceback.format_exc())

    # 数据类型标准化
    def data_log_info(self, log, platform, user, ip, module, type, severity):
        try:
            self.from_platform = platform
            self.user = user.encode("utf-8")
            self.from_ip = struct.unpack('!I', socket.inet_aton(ip))[0]
            self.module = module
            self.type = type
            self.severity = severity
            self.log = log.encode("utf-8")
        except Exception as e:
            print('log info data assignment error {}.'.format(e) + traceback.format_exc())

    # 获取结构体内存地址
    def encode_log(self,log, platform=FROM_CHANNEL["MSG_FROM_WEBUI"], user="平台", ip="127.0.0.1", module=100, type=0, severity=6):
        try:
            self.data_log_info(log,platform,user,ip,module,type,severity)
            return string_at(addressof(self), sizeof(self))
        except Exception as e:
            print('encode log info error {}.'.format(e) + traceback.format_exc())

    # 根据结构体内存地址读取结构体
    def decode(self, data):
        return memmove(addressof(self), data, sizeof(self))
