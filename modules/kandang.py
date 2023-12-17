import os

def list_kandang():
    kandang = os.listdir(f'database/')
    kandang.sort(key = lambda x: int(x[1:]))
    return kandang
