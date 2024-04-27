import os

def file_exists(file_path: str):
    if os.path.exists(file_path):
        return True
    else:
        print("Arquivo não encontrado, tente novamente.\n")
        return False
