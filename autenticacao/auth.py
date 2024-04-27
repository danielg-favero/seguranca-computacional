from Crypto.Cipher import AES
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from base64 import b64encode, b64decode
import os

def file_exists(file_path: str):
    if os.path.exists(file_path):
        return True
    else:
        print("Arquivo não encontrado, tente novamente.\n")
        return False

class AESCipher(object):
    def __init__(self) -> None:
        self.block_size: int = AES.block_size

    def set_key(self, key: str) -> None:
        self.key = key.encode()
    
    def set_mode(self, mode) -> None:
        self.mode = mode

    def __pad(self, plain_text):
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str.encode()
        return padded_plain_text
    
    def __unpad(self, plain_text: bytes):
        last_character = plain_text[len(plain_text) - 1:]
        bytes_to_remove = ord(last_character)
        return plain_text[:-bytes_to_remove]

    def encrypt(self, plain_text: bytes):
        cipher = AES.new(self.key, self.mode)
        padded_text = self.__pad(plain_text)
        encrypted_text = cipher.encrypt(padded_text)

        return b64encode(encrypted_text).decode("utf-8")
        
    def decrypt(self, encrypted_text: bytes):
        encrypted_text = b64decode(encrypted_text)
        cipher = AES.new(self.key, self.mode)
        plain_text = cipher.decrypt(encrypted_text)

        return self.__unpad(plain_text)
    
class RSACipher(object):
    def __init__(self) -> None:
        pass

    def encryt(self, plain_text: bytes, public_key):
        encrypted_text = public_key.encrypt(
            plain_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted_text
    
    def decrypt(self, encrypted_text, private_key):
        plain_text = private_key.decrypt(
            encrypted_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return plain_text
    
    def load_private_key(self, file_path):
        if(file_exists(file_path)):
            with open(file_path, "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                )

                return private_key
            
    def load_public_key(self, file_path):
        if(file_exists(file_path)):
            with open(file_path, "rb") as key_file:
                public_key = serialization.load_pem_public_key(
                    key_file.read(),
                )

                return public_key