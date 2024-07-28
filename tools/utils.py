import os
import logging

import json

import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from binascii import b2a_hex, a2b_hex

import pandas as pd



class FilesUtil():
    """
    用来进行文件操作的工具类
    """
    def __init__(self):
        pass

    @staticmethod
    def get_data_from_file(file_path):
        """
        读取文件中的数据
        :param file_path: 文件路径, 目前仅支持json、txt、csv、xls、xlsx
        :return: 数据
        """
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            elif file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = f.read()
            elif file_path.endswith('.csv'):
                data = pd.read_csv(file_path)
            elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
                data = pd.read_excel(file_path)
            else:
                raise ValueError("不支持的文件类型,请检查文件后缀")
            return data
        except Exception as e:
            logging.error("读取json文件出错：%s" % e)
            return None
    
    @staticmethod
    def write_data_to_file(file_path,data):
        """
        将数据写入文件中
        :param file_path: 文件保存路径
        :param data: 数据
        :return: 无
        """
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)
            elif file_path.endswith('.txt') or file_path.endswith('.log') or file_path.endswith('.md') or file_path.endswith('.html'):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(data)
            elif file_path.endswith('.csv'):
                data.to_csv(file_path, index=False)
            elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
                data.to_excel(file_path, index=False)
            else:
                raise ValueError("不支持的文件类型,请检查文件后缀:仅支持json、txt、csv、xls、xlsx、log、md、html")
        except Exception as e:
            logging.error("写入json文件出错：%s" % e)
            return None
        



class EncryptDecryptUtil():
    """
    用来进行加密解密的工具类
    """
    def __init__(self):
        self.one = None


    @staticmethod
    def md5_encrypt(text):
        """
        md5加密
        :param text: 待加密的字符串
        :return: 加密后的字符串
        """
        md5 = hashlib.md5()
        md5.update(text.encode('utf-8'))
        return md5.hexdigest()
    # md5 无解密
    
    @staticmethod
    def base64_encrypt(input_data):
        """
        将输入数据进行 base64 编码
        Args:
            input_data (bytes/str): 待编码的数据,可以是 bytes 或 str 类型
        Returns:
            str: 编码后的 base64 字符串
        """
        if isinstance(input_data, str):
            input_data = input_data.encode('utf-8')
        encoded = base64.b64encode(input_data)
        return encoded.decode('utf-8')
    
    @staticmethod
    def base64_decrypt(base64_string):
        """
        将 base64 字符串解码
        Args:
            base64_string (str): 待解码的 base64 字符串
        Returns:
            bytes: 解码后的二进制数据
        """
        decoded = base64.b64decode(base64_string)
        return decoded.decode('utf-8')
    

    @staticmethod
    def aes_encrypt(text, key, mode=AES.MODE_ECB, style='pkcs7', str_mode="base64"):
        """
        aes加密
        :param text: 待加密的字符串
        :param key: 加密密钥
        :return: 加密后的字符串
        """
        if isinstance(text, str):
            pass
        else:
            raise TypeError("text must be str")
        text_bytes = text.encode('utf-8')
        key_bytes = key.encode('utf-8')
        # 初始化加密器
        cipher = AES.new(key_bytes, mode=mode)
        # 加密
        encrypt_text = cipher.encrypt(pad(text_bytes, AES.block_size, style=style))
        # 加密结果转为16进制字符串
        if str_mode == "hex":
            encrypt_text = b2a_hex(encrypt_text)
        elif str_mode == "base64":
            encrypt_text = base64.encodebytes(encrypt_text)
        return encrypt_text.decode('utf-8')
    
    @staticmethod
    def aes_decrypt(text, key, mode=AES.MODE_ECB, style='pkcs7', str_mode="base64"):
        """
        aes解密
        :param text: 待解密的字符串
        :param key: 解密密钥    
        :return: 解密后的字符串
        """
        if isinstance(text, str):
            text_bytes = text.encode('utf-8')
        else:
            text_bytes = text
        if str_mode == "hex":
            text = a2b_hex(text_bytes)
        elif str_mode == "base64":
            text = base64.decodebytes(text_bytes)

        key_bytes = key.encode('utf-8')
        # 初始化解密器
        cipher = AES.new(key_bytes, mode=mode)
        # 解密
        decrypt_text = cipher.decrypt(text)
        # 去除填充字符
        decrypt_text = unpad(decrypt_text, AES.block_size, style=style)
        # 解密结果转为字符串
        decrypt_text = decrypt_text.decode('utf-8')
        return decrypt_text