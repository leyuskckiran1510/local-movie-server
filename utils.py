import os


def load_env(file_name: str = '.env'):
    with open(file_name, 'r') as fp:
        data = fp.read()
    dic = {
        i.split('=')[0].strip(): i.split('=')[1].strip()
        for i in data.strip().splitlines()
    }
    os.environ.update(dic)
