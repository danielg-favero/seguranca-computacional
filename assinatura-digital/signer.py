from Crypto.Hash import SHA256
from Crypto.Signature import DSS

class Signer(object):
    def __init__(self) -> None:
        self.__signer = None
        pass

    def sign(self, message: str, private_key):
        self.__signer = DSS.new(private_key, 'fips-186-3')
        hashed_message = SHA256.new(message.encode())
        signature = self.__signer.sign(hashed_message)
        return signature
