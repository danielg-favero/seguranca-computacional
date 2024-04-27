from Crypto.PublicKey import DSA
from file import file_exists

class DSAKeyGen(object):
    def __init__(self) -> None:
        pass

    def generate_key_pair(self):
        key =  DSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        return private_key, public_key
        
    def save(self, file_name, key):
        with open(file_name, 'wb') as f:
            f.write(key)

    def load(self, file_name):
        if file_exists(file_name):
            f = open(file_name, 'rb')
            return DSA.import_key(f.read())
        else:
            print(f"Não foi possível encontrar arquivo {file_name}")