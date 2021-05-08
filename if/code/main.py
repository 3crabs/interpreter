from consts import static_words, one_symbols, two_symbols
from is_functions import is_not_digit, is_digit, is_digit_not_zero, is_digit_16_not_zero, is_digit_16


def read_file(path: str):
    f = open(path, 'r')
    t = ''.join(f.readlines())
    f.close()
    return t + '\n'


i = 0
text = read_file('examples/math.c')


def up_i():
    global i
    if i < len(text) - 1:
        i += 1


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
        if text[i] in '\t\n ':
            has = True
            up_i()


def find_two_symbols():
    global i, text
    s = text[i:i + 2]
    lex = ''
    if s in two_symbols.keys():
        lex = two_symbols[s]
        up_i()
        up_i()
    print(lex)


def find_one_symbols():
    global i, text
    s = text[i]
    lex = ''
    if s in one_symbols.keys():
        lex = one_symbols[s]
        up_i()
    print(lex)


def find_id_or_static_words():
    global i, text
    if is_not_digit(text[i]):
        s = text[i]
        up_i()
        while is_digit(text[i]) or is_not_digit(text[i]):
            s += text[i]
            up_i()

        if s in static_words.keys():
            print(static_words[s])
        else:
            print('ID: ' + s)


def find_consts():
    global i, text
    if is_digit_not_zero(text[i]):
        s = text[i]
        up_i()
        while is_digit(text[i]):
            s += text[i]
            up_i()
        print('DEC: ' + s)
    if text[i:i + 2] == '0x':
        s = text[i:i + 2]
        up_i()
        up_i()
        if is_digit_16_not_zero(text[i]):
            s = text[i]
            up_i()
            while is_digit_16(text[i]):
                s += text[i]
                up_i()
            print('DEC: ' + s)
        else:
            print('ERROR')
        if s == '0x':
            print('ERROR')
        else:
            print('HEX: ' + s)


if __name__ == '__main__':
    while i < len(text) - 2:
        skip_white_symbols_and_comments()
        find_two_symbols()
        find_one_symbols()
        find_id_or_static_words()
        find_consts()
    print('EOF')
