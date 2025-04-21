from binascii import b2a_hex, a2b_hex

from Crypto.Cipher import AES


# python版aes-cbc-pkcs7加密解密hex字符串输入输出

class AesHex(object):
    def __init__(self, key: str, iv: str):
        self.key = key.encode('utf-8')
        self.iv = iv.encode('utf-8')
        self.mode = AES.MODE_CBC

    def encrypt(self, content):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        content_padding = self.pkcs7padding(content)
        encrypt_bytes = cipher.encrypt(content_padding.encode('utf-8'))
        return b2a_hex(encrypt_bytes).decode('utf-8')

    def decrypt(self, content):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        content = a2b_hex(content)
        text = cipher.decrypt(content).decode('utf-8')
        return self.pkcs7unpadding(text)

    def pkcs7unpadding(self, text):
        length = len(text)
        unpadding = ord(text[length - 1])
        return text[0:length - unpadding]

    def pkcs7padding(self, text):
        bs = 16
        length = len(text)
        bytes_length = len(text.encode('utf-8'))
        padding_size = length if (bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        padding_text = chr(padding) * padding
        return text + padding_text


if __name__ == '__main__':
    data = 'this is Aes encryption with pkcs7'
    print("origin", data)
    _key = "1111111111111111"  # 允许16,24,32字节长度
    _iv = "2222222222222222"  # 只允许16字节长度
    pc = AesHex(_key, _iv)
    en = pc.encrypt(data)
    print("encrypt", en)
    de = pc.decrypt(en)
    print("decrypt", de)
