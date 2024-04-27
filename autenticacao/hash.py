from hashlib import sha256

class Hasher():
    def __init__(self) -> None:
        pass

    def hash_message(self, message: bytes):
        m = sha256()
        m.update(message)

        return m.digest()

    def compare_hash(self, message: str, hashed_message: bytes):
        if(hashed_message == message):
            print('Mensagem Autenticada com sucesso\n')
        else: 
            print('Falha na Autenticação\n')