def read_file(path: str):
    f = open(path, 'r')
    t = ''.join(f.readlines())
    f.close()
    return t + '\n'
