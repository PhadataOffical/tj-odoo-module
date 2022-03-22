
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

AESKEY = '6m4SNklr5eZspUjd'
AESIV = 's5IUgjA9h2DWmFS8'


class AESCipher(object):

    def __init__(self):
        """"
        CBC加密需要一个十六位的key(密钥)和一个十六位iv(偏移量)
        """
        self.key = self.check_key(AESKEY)
        self.iv = self.check_key(AESIV)
        self.BS = 16
        self.mode = AES.MODE_CBC
        self.pad = lambda s: pad(s.encode(), self.BS, style='pkcs7')
        self.unpad = lambda s: unpad(s, self.BS, style='pkcs7')

    def check_key(self, key):
        """
        检测key的长度是否为16,24或者32bytes的长度
        """
        try:
            if isinstance(key, bytes):
                assert len(key) in [16, 24, 32]
                return key
            elif isinstance(key, str):
                assert len(key.encode()) in [16, 24, 32]
                return key.encode()
            else:
                raise Exception(f'密钥必须为str或bytes,不能为{type(key)}')
        except AssertionError:
            print('输入的长度不正确')

    def check_data(self, data):
        """
        检测加密的数据类型
        """
        if isinstance(data, int):
            data = str(data)
        elif isinstance(data, bytes):
            data = data.decode()
        elif isinstance(data, str):
            pass
        else:
            raise Exception(f'加密的数据必须为str或bytes,不能为{type(data)}')
        return data

    def encrypt(self, raw):
        raw = self.check_data(raw)
        raw = self.pad(raw)
        cipher = AES.new(self.key, self.mode, self.iv)
        return base64.b64encode(cipher.encrypt(raw)).decode()

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, self.mode, self.iv)
        return self.unpad(cipher.decrypt(enc)).decode()
