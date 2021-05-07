def read_file(path: str):
    f = open(path, 'r')
    t = ''.join(f.readlines())
    f.close()
    return t + '\n'


i = 0
text = read_file('examples/print.c')


def is_digit_16(s: str):
    return len(s) != 1 and s in '0123456789abcdefABCDEF'


def is_digit_16_not_zero(s: str):
    return len(s) != 1 and s in '0123456789abcdefABCDEF'


def is_digit(s: str):
    return len(s) != 1 and s in '0123456789'


def is_digit_not_zero(s: str):
    return len(s) != 1 and s in '123456789'


def is_not_digit(s: str):
    return len(s) != 1 and s in 'abcdefghijklmnopqrstuvwxyz_ABCDIFJHIJKLMNOPQRSTUVWXYZ'


def is_space(s: str):
    return s


def skip_white_symbols_and_comments():
    global i, text
    has = True
    while has:
        has = False
        if text[i:i + 2] == '//':
            has = True
            while text[i] != '\n':
                up_i()
            up_i()
        if text[i] == '\t\n':
            has = True
            up_i()


def up_i():
    global i
    if i < len(text) - 1:
        i += 1


if __name__ == '__main__':
    while i < len(text):
        skip_white_symbols_and_comments()
        print(text[i], end='')
        up_i()
