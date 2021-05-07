def read_file(path: str):
    f = open(path, 'r')
    t = ''.join(f.readlines())
    f.close()
    return t + '\n'


i = 0
text = read_file('examples/math.c')


def is_digit_16(s: str):
    return len(s) == 1 and s in '0123456789abcdefABCDEF'


def is_digit_16_not_zero(s: str):
    return len(s) == 1 and s in '0123456789abcdefABCDEF'


def is_digit(s: str):
    return len(s) == 1 and s in '0123456789'


def is_digit_not_zero(s: str):
    return len(s) == 1 and s in '123456789'


def is_not_digit(s: str):
    return len(s) == 1 and s in 'abcdefghijklmnopqrstuvwxyz_ABCDIFJHIJKLMNOPQRSTUVWXYZ'


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


def up_i():
    global i
    if i < len(text) - 1:
        i += 1


def find_id_or_static_words():
    global i, text
    if is_not_digit(text[i]):
        s = text[i]
        up_i()
        while is_digit(text[i]) or is_not_digit(text[i]):
            s += text[i]
            up_i()

        if s == 'void':
            print('VOID')
        elif s == 'if':
            print('IF')
        elif s == 'else':
            print('ELSE')
        elif s == 'short':
            print('SHORT')
        elif s == 'int':
            print('INT')
        elif s == 'long':
            print('LONG')
        else:
            print('ID: ' + s)


def find_one_symbols():
    global i, text
    if text[i] == '(':
        print('ROUND_LEFT')
        up_i()
    if text[i] == ')':
        print('ROUND_RIGHT')
        up_i()
    if text[i] == '{':
        print('CURLY_LEFT')
        up_i()
    if text[i] == '}':
        print('CURLY_RIGHT')
        up_i()
    if text[i] == ';':
        print('SEMICOLON')
        up_i()
    if text[i] == '=':
        print('ASSIGN')
        up_i()
    if text[i] == '+':
        print('PLUS')
        up_i()
    if text[i] == '-':
        print('MINUS')
        up_i()
    if text[i] == '*':
        print('STAR')
        up_i()
    if text[i] == '/':
        print('SLASH')
        up_i()
    if text[i] == '%':
        print('PERCENT')
        up_i()
    if text[i] == ',':
        print('COMMA')
        up_i()
    if text[i] == '<':
        print('LESS')
        up_i()
    if text[i] == '>':
        print('GREATER')
        up_i()


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
        while is_digit(text[i]):
            s += text[i]
            up_i()
        if s == '0x':
            print('ERROR')
        else:
            print('HEX: ' + s)


def find_two_symbols():
    global i, text
    if text[i:i + 2] == '>>':
        print('R_SHIFT')
        up_i()
        up_i()
    if text[i:i + 2] == '<<':
        print('L_SHIFT')
        up_i()
        up_i()
    if text[i:i + 2] == '==':
        print('EQ')
        up_i()
        up_i()
    if text[i:i + 2] == '!=':
        print('NOT_EQ')
        up_i()
        up_i()
    if text[i:i + 2] == '<=':
        print('LESS_EQ')
        up_i()
        up_i()
    if text[i:i + 2] == '>=':
        print('GREATER_EQ')
        up_i()
        up_i()


if __name__ == '__main__':
    while i < len(text) - 2:
        skip_white_symbols_and_comments()
        find_two_symbols()
        find_one_symbols()
        find_id_or_static_words()
        find_consts()
    print('EOF')
