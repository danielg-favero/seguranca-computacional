import time
class Receiver():
    @staticmethod
    def receive(path: str, type='r'):
        time.sleep(3)
        f = open(path, type)
        return f