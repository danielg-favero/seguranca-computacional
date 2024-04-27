import os
import sys
from dsa import DSAKeyGen
from aes import AESCipher
from signer import Signer
from mailer import Mailer
from dss import DSSVerifier
from file import file_exists

clear = lambda: os.system('clear')

def create_cipher():
    aes = AESCipher()
    aes.set_key("Sixteen byte key")
    aes.set_mode(1)

    return aes

def menu(options):
    choice = -1

    last_option = str(int(list(options)[-1]) + 1)

    while choice != last_option:
        clear()
        for key, value in options.items():
            print(f"{key}. {value['label']}")
        print(f"{last_option}. Sair")

        choice = input("\nEscolha uma opção: ")
        
        if choice in options:
            options[choice]['execute']()

            input("Pressione qualquer tecla para continuar...\n")
        elif choice != last_option:
            input("Opção inválida, tente novamente...\n")
    
    sys.exit()

def generate_key_pair():
    dsa = DSAKeyGen()
    private_key, public_key = dsa.generate_key_pair()

    dsa.save('keys/dsa_key.priv', private_key)
    dsa.save('keys/dsa_key.pub', public_key)

    print("Chaves Geradas Com Sucesso!\n")

def sign_message():
    signer = Signer()
    dsa = DSAKeyGen()

    private_key_path = input('Informe o caminho da chave privada: ')

    if file_exists(private_key_path):
        private_key = dsa.load(private_key_path)

        plain_text = input('Digite a mensagem a ser assinada: ')
        signature = signer.sign(plain_text, private_key)
        message = plain_text.encode() + signature

        with open('signed_files/signed', 'wb') as f:
            f.write(message)
            print('Mensagem assinada com sucesso')

def sign_encrypted_message():
    signer = Signer()
    dsa = DSAKeyGen()
    aes = create_cipher()

    private_key_path = input('Informe o caminho da chave privada: ')

    if file_exists(private_key_path):
        private_key = dsa.load(private_key_path)

        plain_text = input('Digite a mensagem a ser assinada: ')
        signature = signer.sign(plain_text, private_key)

        encrypted_message = aes.encrypt(plain_text.encode() + signature)

        with open('signed_files/signed_encrypted', 'wb') as f:
            f.write(encrypted_message.encode())
            print('Mensagem assinada com sucesso')

def send_to_email():
    mailer = Mailer()
    mailer.login()

    msg_file = input('Informe o caminho do arquivo assinado: ')
    public_key = input('Informe o caminho da chave pública: ')

    if file_exists(msg_file) and file_exists(public_key):
        receiver = input('Informe o email do destinatário: ')
        subject = input('Informe o assunto da mensagem: ')
        body = input('Informe o corpo do email: ')
        
        mailer.send(
            receiver, 
            subject, 
            body, 
            attachments=[
                msg_file,
                public_key
            ]
        )

def verify_message():
    dsa = DSAKeyGen()
    dss = DSSVerifier()

    msg_file_path = input('Informe o caminho do arquivo assinado: ')
    public_key_file_path = input('Informe o caminho da chave pública: ')

    if file_exists(msg_file_path) and file_exists(public_key_file_path):
        msg_file = open(msg_file_path, 'rb')
        signed_message = msg_file.read()

        public_key = dsa.load(public_key_file_path)
        dss.set_key(public_key)
        
        plain_text, signature = signed_message[:-56], signed_message[-56:]

        if dss.verify(plain_text, signature):
            print('Mensagem válida')
        else:
            print('Mensagem inválida')

def verify_encrypted_message():
    dsa = DSAKeyGen()
    dss = DSSVerifier()
    aes = create_cipher()

    msg_file_path = input('Informe o caminho do arquivo assinado: ')
    public_key_file_path = input('Informe o caminho da chave pública: ')

    if file_exists(msg_file_path) and file_exists(public_key_file_path):
        msg_file = open(msg_file_path, 'rb')
        encrypted_signed_message = msg_file.read()

        public_key = dsa.load(public_key_file_path)
        dss.set_key(public_key)
        
        signed_message = aes.decrypt(encrypted_signed_message)
        plain_text, signature = signed_message[:-56], signed_message[-56:]

        if dss.verify(plain_text, signature):
            print('Mensagem válida')
        else:
            print('Mensagem inválida')

def main():
    options = {
        '1': {
            'label': 'Gerar par de chaves',
            'execute': generate_key_pair
        },
        '2': {
            'label': 'Assinar mensagem sem criptografia',
            'execute': sign_message
        },
        '3': {
            'label': 'Assinar mensagem com criptografia',
            'execute': sign_encrypted_message
        },
        '4': {
            'label': 'Verificar mensagem recebida por email',
            'execute': verify_message
        },
        '5': {
            'label': 'Verificar mensagem criptografada recebida por email',
            'execute': verify_encrypted_message
        },
        '6': {
            'label': 'Enviar mensagem assinada por email',
            'execute': send_to_email
        },
    }

    menu(options)

if __name__ == "__main__":
    main()