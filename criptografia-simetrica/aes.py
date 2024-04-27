from Crypto.Cipher import AES
import os
import sys
import random
from base64 import b64encode, b64decode

clear = lambda: os.system('clear')

class AESCipher(object):
    def __init__(self) -> None:
        self.block_size = AES.block_size

    def set_key(self, key: str) -> None:
        self.key = key.encode()
    
    def set_mode(self, mode) -> None:
        self.mode = mode

    def __pad(self, plain_text):
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text
    
    def __unpad(self, plain_text: str):
        last_character = plain_text[len(plain_text) - 1:]
        bytes_to_remove = ord(last_character)
        return plain_text[:-bytes_to_remove]

    def encrypt(self, plain_text: str):
        if self.mode == AES.MODE_ECB:
            cipher = AES.new(self.key, self.mode)
            padded_text = self.__pad(plain_text)
            encrypted_text = cipher.encrypt(padded_text.encode())

            return b64encode(encrypted_text).decode("utf-8")
        elif self.mode == AES.MODE_CTR:
            nonce_size = 8
            nonce = random.randbytes(nonce_size)

            cipher = AES.new(self.key, self.mode, nonce=nonce)
            padded_text = self.__pad(plain_text)
            encrypted_text = cipher.encrypt(padded_text.encode())

            return b64encode(nonce + encrypted_text).decode("utf-8")
        else:
            iv = random.randbytes(self.block_size)
            cipher = AES.new(self.key, self.mode, iv=iv)
            padded_text = self.__pad(plain_text)
            encrypted_text = cipher.encrypt(padded_text.encode())

            return b64encode(iv + encrypted_text).decode("utf-8")
    
    def decrypt(self, encrypted_text: str):
        encrypted_text = b64decode(encrypted_text)

        if self.mode == AES.MODE_ECB:
            cipher = AES.new(self.key, self.mode)
            plain_text = cipher.decrypt(encrypted_text).decode("utf-8")
            return self.__unpad(plain_text)
        elif self.mode == AES.MODE_CTR:
            nonce_size = 8
            nonce = encrypted_text[:nonce_size]

            cipher = AES.new(self.key, self.mode, nonce=nonce)
            plain_text = cipher.decrypt(encrypted_text[nonce_size:]).decode("utf-8")
            return self.__unpad(plain_text)
        else:
            iv = encrypted_text[:self.block_size]
            cipher = AES.new(self.key, self.mode, iv=iv)
            plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
            return self.__unpad(plain_text)

def choice_menu(cipher):
    choice = -1

    while choice != '3':
        clear()
        print("1. Criptografar texto")
        print("2. Decriptografar texto")
        print("3. Sair")

        choice = input("\nEscolha uma opção: ")
        
        if choice in ['1', '2']:
            if choice == '1':
                plain_text = input("Digite o texto a ser criptografado: ")
                encrypted_text = cipher.encrypt(plain_text)

                print(f"Texto criptografado: {encrypted_text}\n")

            elif choice == '2':
                encrypted_text = input("Digite o texto criptografado: ")
                decrypted_text = cipher.decrypt(encrypted_text)

                print(f"Texto decriptografado: {decrypted_text}\n")

            input("Pressione qualquer tecla para continuar...\n")
        elif choice != '3':
            input("Opção inválida, tente novamente...\n")
    
    sys.exit()

def key_menu():
    key_size = -1

    while key_size != '3':
        clear()
        print("Qual o tipo de chave irá utilizar?")
        print("1. 128 Bits (16 caracteres)")
        print("2. 256 Bits (32 caracteres)")
        print("3. Sair")

        key_size = input("\nEscolha uma opção: ")

        if key_size in ['1', '2']:
            clear()

            bits_count = 128 * int(key_size)
            char_count = 128 * int(key_size) / 8

            key = input(f"Informe uma chave de {bits_count} bits ({char_count} caracteres): ")

            while len(key) != char_count:
                clear()
                print(f"ERRO: A CHAVE DEVE TER {char_count} CARACTERES ({bits_count} BITS)!\n")
                key = input(f"Informe uma chave de {bits_count} bits ({char_count} caracteres): ")

            return key
        elif key_size != '3':
            input("Opção inválida, tente novamente...\n")
    
    sys.exit()

def mode_menu():
    mode = -1

    while mode != '7':
        clear()
        print("Qual o modo de operação irá utilizar?")
        print("1. ECB")
        print("2. CBC")
        print("3. CFB")
        print("5. OFB")
        print("6. CTR")
        print("7. Sair")

        mode = input("\nEscolha uma opção: ")

        if mode in ['1', '2', '3', '5', '6']:
            clear()
            return int(mode)
        elif mode != '7':
            input("Opção inválida, tente novamente...\n")
    
    sys.exit()

def main():
    clear()
    
    cipher = AESCipher()

    key = key_menu()
    cipher.set_key(key)

    mode = mode_menu()
    cipher.set_mode(mode)

    choice_menu(cipher)

if __name__ == "__main__":
    main()
