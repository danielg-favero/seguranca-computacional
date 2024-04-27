import time

class Sender():
    @staticmethod
    def send(message: str, type='w', name: str = 'message.txt'):
        with open(name, type) as f:
            time.sleep(1)
            f.write(message)