from utils.Lexem import Lexem
from utils.utils import static_words, one_symbols, two_symbols, is_not_digit, is_digit, is_digit_16, read_file

i = 0
col = 1
row = 1
text = ''


def get_row():
    global row
    return row


def get_col():
    global col
    return col


def up_i():
    global i, col, row
    if i < len(text) - 1:
        if text[i] == '\n':
            row += 1
            col = 0
        else:
            col += 1
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
    if s in two_symbols.keys():
        name = two_symbols[s]
        up_i()
        up_i()
        return Lexem(name), True
    return None, False


def find_one_symbols():
    global i, text
    s = text[i]
    if s in one_symbols.keys():
        name = one_symbols[s]
        up_i()
        return Lexem(name), True
    return None, False


def find_id_or_static_words():
    global i, text
    if is_not_digit(text[i]):
        s = text[i]
        up_i()
        while is_digit(text[i]) or is_not_digit(text[i]):
            s += text[i]
            up_i()
        if s in static_words.keys():
            return Lexem(static_words[s]), True
        else:
            return Lexem('ID', s), True
    return None, False


def find_consts():
    global i, text
    if is_digit(text[i]):
        s = text[i]
        up_i()
        while is_digit(text[i]):
            s += text[i]
            up_i()
        return Lexem('DEC', s), True
    return None, False


def find_consts_hex():
    global i, text
    if text[i:i + 2] == '0x':
        s = text[i:i + 2]
        up_i()
        up_i()
        if is_digit_16(text[i]):
            s += text[i]
            up_i()
            while is_digit_16(text[i]):
                s += text[i]
                up_i()
            return Lexem('HEX', s), True
        else:
            return Lexem('HEX', '0x0'), True
    return None, False


def load_file(path: str):
    global i, col, row, text
    print(path)
    i = 0
    col = 1
    row = 1
    text = read_file(path)


def next_lex():
    skip_white_symbols_and_comments()
    lex, ok = find_two_symbols()
    if ok:
        return lex
    lex, ok = find_one_symbols()
    if ok:
        return lex
    lex, ok = find_id_or_static_words()
    if ok:
        return lex
    lex, ok = find_consts()
    if ok:
        return lex
    lex, ok = find_consts_hex()
    if ok:
        return lex
    return Lexem('EOF')


def read_lexem():
    global i, col, row
    tmp_i, tmp_col, tmp_row = i, col, row
    lex = next_lex()
    i, col, row = tmp_i, tmp_col, tmp_row
    return lex


def g():
    global i, col, row
    return i, col, row


def s(ni, ncol, nrow):
    global i, col, row
    i, col, row = ni, ncol, nrow


def read_second_lex():
    global i, col, row
    tmp_i, tmp_col, tmp_row = i, col, row
    next_lex()
    lex = next_lex()
    i, col, row = tmp_i, tmp_col, tmp_row
    return lex


def test(path: str):
    load_file(path)
    lex = next_lex()
    while lex.name != 'EOF' and lex.name != 'ERROR':
        print(lex)
        lex = next_lex()
    print(lex)
    print()


if __name__ == '__main__':
    test('examples/code.c')
