from hash import Hasher
from auth import AESCipher, RSACipher
from sender import Sender
from receiver import Receiver
import os
import sys

clear = lambda: os.system('clear')

salt = b'salt_example'
SHA256_HASH_LENGTH = 32
SALT_LENGTH = len(salt)

def create_symmetric_cipher():
    symmetric_cipher = AESCipher()
    symmetric_cipher.set_mode(1)
    symmetric_cipher.set_key('asdfghjklzxcvbnm')

    return symmetric_cipher

def create_assymetric_cipher():
    assymmetric_cipher = RSACipher()
    return assymmetric_cipher

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

def pipeline1_send():
    hasher = Hasher()
    symmetric_cipher = create_symmetric_cipher()

    plain_text = input('Digite o texto a ser criptografado: ')
    plain_text = plain_text.encode()
    hashed_message = hasher.hash_message(plain_text)
    message = plain_text + hashed_message
    encrypted_message = symmetric_cipher.encrypt(message)

    Sender.send(encrypted_message)
    print('Mensagem enviada com sucesso...\n')

def pipeline1_receive():
    hasher = Hasher()
    symmetric_cipher = create_symmetric_cipher()

    file_path = input('Digite o caminho do arquivo: ')
    received_file = Receiver.receive(file_path)
    received_encrypted_message = received_file.read()

    message = symmetric_cipher.decrypt(received_encrypted_message)
    plain_text = message[:-SHA256_HASH_LENGTH]
    hashed_message = message[-SHA256_HASH_LENGTH:]

    hasher.compare_hash(hasher.hash_message(plain_text), hashed_message)

def pipeline2_send():
    hasher = Hasher()
    symmetric_cipher = create_symmetric_cipher()

    plain_text = input('Digite o texto a ser criptografado: ')
    hashed_message = hasher.hash_message(plain_text.encode())
    encrypted_hash = symmetric_cipher.encrypt(hashed_message)
    message = plain_text + encrypted_hash

    Sender.send(message)
    print('Mensagem enviada com sucesso...\n')

def pipeline2_receive():
    hasher = Hasher()
    symmetric_cipher = create_symmetric_cipher()

    file_path = input('Digite o caminho do arquivo: ')
    received_file = Receiver.receive(file_path)
    received_encrypted_message = received_file.read()

    plain_text = received_encrypted_message[:-64]
    encrypted_hashed_message = received_encrypted_message[-64:]
    hashed_message = symmetric_cipher.decrypt(encrypted_hashed_message.encode())

    hasher.compare_hash(hasher.hash_message(plain_text.encode()), hashed_message)

def pipeline3_send():
    hasher = Hasher()
    assymmetric_cipher = create_assymetric_cipher()

    plain_text = input('Digite o texto a ser enviado: ')
    public_key_path = input('Digite o caminho da chave publica: ')
    public_key = assymmetric_cipher.load_public_key(public_key_path)

    hashed_message = hasher.hash_message(plain_text.encode())
    encrypted_hash_message = assymmetric_cipher.encryt(hashed_message, public_key)
    message = plain_text.encode() + encrypted_hash_message

    Sender.send(message, 'wb', 'message.bin')
    print('Mensagem enviada com sucesso...\n')
    pass

def pipeline3_receive():
    hasher = Hasher()
    assymmetric_cipher = create_assymetric_cipher()

    file_path = input('Digite o caminho do arquivo: ')
    private_key_path = input('Digite o caminho da chave privada: ')
    private_key = assymmetric_cipher.load_private_key(private_key_path)

    received_file = Receiver.receive(file_path, 'rb')
    received_encrypted_message = received_file.read()

    plain_text = received_encrypted_message[:-512]
    encrypted_hash_message = received_encrypted_message[-512:]

    decrypted_hash_message = assymmetric_cipher.decrypt(encrypted_hash_message, private_key)

    hasher.compare_hash(hasher.hash_message(plain_text), decrypted_hash_message)
    pass

def pipeline4_send():
    hasher = Hasher()
    symmetric_cipher = create_symmetric_cipher()
    assymmetric_cipher = create_assymetric_cipher()

    plain_text = input('Digite o texto a ser enviado: ')
    public_key_path = input('Digite o caminho da chave publica: ')
    public_key = assymmetric_cipher.load_public_key(public_key_path)

    hashed_message = hasher.hash_message(plain_text.encode())
    encrypted_hash_message = assymmetric_cipher.encryt(hashed_message, public_key)
    message = plain_text.encode() + encrypted_hash_message

    encrypted_message = symmetric_cipher.encrypt(message)

    Sender.send(encrypted_message)
    print('Mensagem enviada com sucesso...\n')

def pipeline4_receive():
    hasher = Hasher()
    symmetric_cipher = create_symmetric_cipher()
    assymmetric_cipher = create_assymetric_cipher()

    file_path = input('Digite o caminho do arquivo: ')
    private_key_path = input('Digite o caminho da chave privada: ')
    private_key = assymmetric_cipher.load_private_key(private_key_path)

    received_file = Receiver.receive(file_path)
    received_encrypted_message = received_file.read()

    message = symmetric_cipher.decrypt(received_encrypted_message)
    plain_text = message[:-512]
    encrypted_hash_message = message[-512:]

    decrypted_hash_message = assymmetric_cipher.decrypt(encrypted_hash_message, private_key)

    hasher.compare_hash(hasher.hash_message(plain_text), decrypted_hash_message)

def pipeline5_send():
    hasher = Hasher()

    plain_text = input('Digite o texto a ser enviado: ')

    hashed_message = hasher.hash_message(plain_text.encode() + salt)
    message = plain_text.encode() + hashed_message

    Sender.send(message, 'wb', 'message.bin')
    print('Mensagem enviada com sucesso...\n')

def pipeline5_receive():
    hasher = Hasher()

    file_path = input('Digite o caminho do arquivo: ')
    received_file = Receiver.receive(file_path, 'rb')
    received_hashed_message = received_file.read()

    plain_text = received_hashed_message[:-SHA256_HASH_LENGTH]
    hashed_message = received_hashed_message[-SHA256_HASH_LENGTH:]

    hasher.compare_hash(hasher.hash_message(plain_text + salt), hashed_message)

def pipeline6_send():
    hasher = Hasher()
    symmetric_cipher = create_symmetric_cipher()

    plain_text = input('Digite o texto a ser enviado: ')

    hashed_message = hasher.hash_message(plain_text.encode() + salt)
    message = plain_text.encode() + hashed_message

    encrypted_hash_message = symmetric_cipher.encrypt(message)

    Sender.send(encrypted_hash_message)
    print('Mensagem enviada com sucesso...\n')

    pass

def pipeline6_receive():
    hasher = Hasher()
    symmetric_cipher = create_symmetric_cipher()

    file_path = input('Digite o caminho do arquivo: ')
    received_file = Receiver.receive(file_path)
    received_hashed_message = received_file.read()

    decrypted_hash_message = symmetric_cipher.decrypt(received_hashed_message)

    plain_text = decrypted_hash_message[:-SHA256_HASH_LENGTH]
    hashed_message = decrypted_hash_message[-SHA256_HASH_LENGTH:]

    hasher.compare_hash(hasher.hash_message(plain_text + salt), hashed_message)

    pass

def main():
    options = {
        '1': {
            'label': 'Enviar mensgaem com Hash',
            'execute': pipeline1_send
        },
        '2': {
            'label': 'Receber mensagem com Hash',
            'execute': pipeline1_receive
        },
        '3': {
            'label': 'Enviar mensagem com Criptografia Simétrica no Hash',
            'execute': pipeline2_send
        },
        '4': {
            'label': 'Receber criptografia Criptografia Simétrica no Hash',
            'execute': pipeline2_receive
        },
        '5': {
            'label': 'Enviar mensagem com Hash + Criptografia Assimétrica',
            'execute': pipeline3_send
        },
        '6': {
            'label': 'Receber mensagem com Hash + Criptografia Assimétrica',
            'execute': pipeline3_receive
        },
        '7': {
            'label': 'Enviar mensagem com Hash + Criptografia Simétrica + Criptografia Assimétrica',
            'execute': pipeline4_send
        },
        '8': {
            'label': 'Receber mensagem com Hash + Criptografia Simétrica + Criptografia Assimétrica',
            'execute': pipeline4_receive
        },
        '9': {
            'label': 'Enviar mensagem com Hash + Salt',
            'execute': pipeline5_send
        },
        '10': {
            'label': 'Receber mensagem com Hash + Salt',
            'execute': pipeline5_receive
        },
        '11': {
            'label': 'Enviar mensagem com Hash + Salt + Criptografia Assimétrica',
            'execute': pipeline6_send
        },
        '12': {
            'label': 'Receber mensagem com Hash + Salt + Criptografia Assimétrica',
            'execute': pipeline6_receive
        },
    }

    menu(options)

if __name__ == "__main__":
    main()
