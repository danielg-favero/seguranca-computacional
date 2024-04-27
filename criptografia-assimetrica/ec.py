from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

clear = lambda: os.system('clear')

class ECKeyGen(object):
    def __init__(self) -> None:
        self.__private_key = None
        self.public_key = None
        pass

    # Gerar chave privada EC
    def generate_private_key(self):
        self.__private_key = ec.generate_private_key(
            ec.SECP521R1(), default_backend()
        )

    # Gerar a chave pública EC
    def generate_public_key(self):
        try:
            self.public_key = self.__private_key.public_key()
        except:
            print("Erro: é preciso gerar a chave privada antes de obter a pública")

    # Salvar as chaves públicas e privadas
    def save(self, name):
        try:
            with open(f"{name}_ec_pub.pem", "wb") as f:
                f.write(self.public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))

            with open(f"{name}_ec_priv.pem", "wb") as f:
                f.write(self.__private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
        except:
            print("Erro: é preciso gerar a chave privada antes de salvar")

class ECKeys(object):
    def __init__(self) -> None:
        pass

    def load_private_key(self, path):
        with open(path, "rb") as key_file:
            self.__private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())
        
    def load_public_key(self, path):
        with open(path, "rb") as key_file:
            self.public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

    def derive(self):
        try:
            shared_key = self.__private_key.exchange(ec.ECDH(), self.public_key)
            derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'handshake data', backend=default_backend()).derive(shared_key)
            return derived_key
        except:
            print("Erro: é preciso carregar a chave privada antes de derivar")

class Encryptor(object):
    def __init__(self) -> None:
        pass

    def encrypt(self, plain_text: str, key):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_text = encryptor.update(plain_text.encode()) + encryptor.finalize()

        return iv, encrypted_text

    def decrypt(self, encrypted_text: str, iv, key):
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return (decryptor.update(encrypted_text) + decryptor.finalize()).decode("utf-8")

def file_exists(file_path: str):
    if os.path.exists(file_path):
        return True
    else:
        print("Arquivo não encontrado, tente novamente.\n")
        return False

def main():
    clear()

    key_gen = ECKeyGen()
    keys = ECKeys()
    encryptor = Encryptor()

    choice = -1

    while choice != '4':
        clear()
        print("1. Gerar par de Chaves")
        print("2. Carregar par de Chaves")
        print("3. Criptografar e Decriptografar uma mensagem")
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
            if choice == '2':
                private_key_file_path = input("Digite o caminho para o arquivo da chave privada: ")

                if file_exists(private_key_file_path):
                    public_key_file_path = input("Digite o caminho para o arquivo da chave publica: ")

                    if file_exists(public_key_file_path):
                        keys.load_private_key(private_key_file_path)
                        keys.load_public_key(public_key_file_path)

                        print("\nChaves públicas e privadas carregadas com sucesso!")
            if choice == '3':
                key = keys.derive()

                plain_text = input("Digite o texto a ser criptografado: ")

                iv, encrypted_text = encryptor.encrypt(plain_text, key)
                plain_text = encryptor.decrypt(encrypted_text, iv, key)

                print("\n")
                print(f"Texto criptografado: {encrypted_text}")
                print(f"Texto decriptografado: {plain_text}")

            input("\nPressione qualquer tecla para continuar...")
        elif choice != '4':
            input("Opção inválida, tente novamente...\n")

if __name__ == "__main__":
    main()



