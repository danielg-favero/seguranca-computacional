from Crypto.Cipher import DES
import os

clear = lambda: os.system('clear')

class DESCipher:
    def __init__(self, key: str, mode=DES.MODE_ECB) -> None:
        self.key = key.encode()
        self.mode = mode

    def pad(self, text: str):
        return text + ((8 - len(text) % 8) * ' ')

    def unpad(self, text: bytes):
        return text.decode().rstrip(' ')
    
    def pad_bin(self, text: str):
        return text + ((8 - len(text) % 8) * b' ')

    def unpad_bin(self, text: bytes):
        return text.rstrip(b' ')

    def encrypt_file(self, input):
        cipher = DES.new(self.key, self.mode)
        padded_text = self.pad_bin(input)
        encrypted_text = cipher.encrypt(padded_text)

        return encrypted_text

    def decrypt_file(self, input):
        cipher = DES.new(self.key, self.mode)
        decrypted_text = cipher.decrypt(input)
        unpadded_text = self.unpad_bin(decrypted_text)

        return unpadded_text

    def encrypt(self, text: str):
        cipher = DES.new(self.key, self.mode)
        padded_text = self.pad(text)
        encrypted_text = cipher.encrypt(padded_text.encode())

        return encrypted_text.hex()
    
    def decrypt(self, text: str):
        cipher = DES.new(self.key, self.mode)
        bin_text = bytes.fromhex(text)
        decrypted_text = cipher.decrypt(bin_text)
        unpadded_text = self.unpad(decrypted_text)

        return unpadded_text

def open_file(file_path: str, type:str = ''):
    with open(file_path, 'r' + type) as file:
        res = file.read()
    
    return res

def write_file(file_path: str, data, type:str = ''):
    with open(file_path, 'w' + type) as file:
        file.write(data)

def file_exists(file_path: str):
    if os.path.exists(file_path):
        return True
    else:
        print("Arquivo não encontrado, tente novamente.\n")
        return False

def menu():
    clear()
    print("1. Criptografar texto")
    print("2. Decriptografar texto")
    print("3. Criptografar texto de um arquivo de texto")
    print("4. Decriptografar texto de um arquivo de texto")
    print("5. Criptografar um arquivo binário")
    print("6. Decriptografar um arquivo binário")
    print("7. Sair")

    choice = input("\nEscolha uma opção: ")

    return choice

def main():
    clear()
    choice = -1
    
    key = input("Informe uma chave de 64 bits (8 caracteres): ")

    while len(key) != 8:
        clear()
        print("ERRO: A CHAVE DEVE TER 8 CARACTERES (64 BITS)!\n")
        key = input("Informe uma chave de 64 bits (8 caracteres): ")

    cipher = DESCipher(key)

    while choice != '7':
        choice = menu()
        
        if choice in ['1', '2', '3', '4', '5', '6']:

            clear()

            if choice == '1':
                plain_text = input("Digite o texto a ser criptografado: ")
                encrypted_text = cipher.encrypt(plain_text)

                print(f"Texto criptografado: {encrypted_text}\n")

            elif choice == '2':
                encrypted_text = input("Digite o texto criptografado: ")
                decrypted_text = cipher.decrypt(encrypted_text)

                print(f"Texto decriptografado: {decrypted_text}\n")

            elif choice == '3':
                file_path = input("Digite o caminho para o arquivo: ")

                if file_exists(file_path):
                    file = open_file(file_path)
                    encrypted = cipher.encrypt(file)
                    write_file(file_path + '.encrypted', encrypted)

                    print("Arquivo criptografado com sucesso.\n")

            elif choice == '4':
                file_path = input("Digite o caminho para o arquivo: ")

                if file_exists(file_path):
                    file = open_file(file_path)
                    decrypted_text = cipher.decrypt(file)
                    write_file(file_path[:-10] + '.decrypted', decrypted_text)

                    print("Arquivo decriptografado com sucesso.\n")

            elif choice == '5':
                file_path = input("Digite o caminho para o arquivo: ")

                if file_exists(file_path):
                    file = open_file(file_path, 'b')
                    encrypted = cipher.encrypt_file(file)
                    write_file(file_path + '.encrypted', encrypted, 'b')
                    
                    print("Arquivo binário criptografado com sucesso.\n")

            elif choice == '6':
                file_path = input("Digite o caminho para o arquivo: ")

                if file_exists(file_path):
                    file = open_file(file_path,'b')
                    decrypted_text = cipher.decrypt_file(file)
                    write_file(file_path[:-14] + '_decrypted.jpg', decrypted_text, 'b')

                    print("Arquivo binário decriptografado com sucesso.\n")

            input("Pressione qualquer tecla para continuar...")
        elif choice != '7':
            input("Opção inválida, tente novamente...\n")

if __name__ == "__main__":
    main()
