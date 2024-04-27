from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import os

clear = lambda: os.system('clear')

def open_file(file_path: str):
    with open(file_path, 'r') as file:
        res = file.read()
    
    return res

def file_exists(file_path: str):
    if os.path.exists(file_path):
        return True
    else:
        print("Arquivo não encontrado, tente novamente.\n")
        return False

class RSAKeyGen(object):
    def __init__(self) -> None:
        self.__private_key = None
        self.public_key = None
        pass

    # Gerar chave privada RSA
    def generate_private_key(self):
        self.__private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )

    # Gerar a chave pública RSA
    def generate_public_key(self):
        try:
            self.public_key = self.__private_key.public_key()
        except:
            print("Erro: é preciso gerar a chave privada antes de obter a pública")

    # Salvar as chaves públicas e privadas
    def save(self, name):
        try:
            with open(f"{name}_rsa_pub.pem", "wb") as f:
                f.write(self.public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))

            with open(f"{name}_rsa_priv.pem", "wb") as f:
                f.write(self.__private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
        except:
            print("Erro: é preciso gerar a chave privada antes de salvar")

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

class RSAEncrypter(object):
    def __init__(self) -> None:
        pass

    # Criptografar uma mensagem
    def encrypt(self, plain_text: str, public_key):
        encrypted_text = public_key.encrypt(
            plain_text.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted_text.hex()

    # Função para decriptografar uma mensagem
    def decrypt(self, encrypted_text, private_key):
        plain_text = private_key.decrypt(
            bytes.fromhex(encrypted_text),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return plain_text.decode()

def main():
    clear()

    key_gen = RSAKeyGen()
    encrypter = RSAEncrypter()

    choice = -1

    while choice != '4':
        clear()
        print("1. Gerar par de Chaves")
        print("2. Criptografar texto")
        print("3. Decriptografar texto")
        print("4. Sair")

        choice = input("\nEscolha uma opção: ")
        
        clear()
        if choice in ['1', '2', '3']:
            if choice == '1':
                key_gen.generate_private_key()
                key_gen.generate_public_key()
                key_name = input("Informe o nome para o par de chaves: ")

                key_gen.save(key_name)

                print("\nChaves públicas e privadas salvas com sucesso!")

            elif choice == '2':
                plain_text = input("Digite o texto plano: ")
                public_key_file_path = input("Digite o caminho para a chave pública: ")
                public_key = key_gen.load_public_key(public_key_file_path)

                if(public_key):
                    encrypted_text = encrypter.encrypt(plain_text, public_key)
                    print(f"Texto criptografado: {encrypted_text}\n")
                else:
                    print("Erro: Não foi possível encontrar o arquivo da chave pública, tente novamente...\n")

            elif choice == '3':
                encrypted_text = input("Digite o texto criptografado: ")
                private_key_file_path = input("Digite o caminho para a chave privada: ")
                private_key = key_gen.load_private_key(private_key_file_path)

                if(private_key):
                    encrypted_text = encrypter.decrypt(encrypted_text, private_key)
                    print(f"Texto decriptografado: {encrypted_text}\n")
                else:
                    print("Erro: Não foi possível encontrar o arquivo da chave privada, tente novamente...\n")

            input("Pressione qualquer tecla para continuar...")
        elif choice != '4':
            input("Opção inválida, tente novamente...\n")

if __name__ == "__main__":
    main()



