static_words = {
    'void': 'VOID',
    'switch': 'SWITCH',
    '_int64': 'INT64',
    'int': 'INT',
    'break': 'BREAK',
    'default': 'DEFAULT',
    'case': 'CASE'
}

one_symbols = {
    '(': 'ROUND_LEFT',
    ')': 'ROUND_RIGHT',
    '{': 'CURLY_LEFT',
    '}': 'CURLY_RIGHT',
    ';': 'SEMICOLON',
    '=': 'ASSIGN',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'STAR',
    '/': 'SLASH',
    '%': 'PERCENT',
    ',': 'COMMA',
    '<': 'LESS',
    '>': 'GREATER',
    ':': 'COLON'
}

two_symbols = {
    '>>': 'R_SHIFT',
    '<<': 'L_SHIFT',
    '==': 'EQ',
    '!=': 'NOT_EQ',
    '<=': 'LESS_EQ',
    '>=': 'GREATER_EQ'
}


def read_file(path: str):
    f = open(path, 'r')
    t = ''.join(f.readlines())
    f.close()
    return t + '\n\0'


def is_digit_16(s: str):
    return len(s) == 1 and s in '0123456789abcdefABCDEF'


def is_digit(s: str):
    return len(s) == 1 and s in '0123456789'


def is_not_digit(s: str):
    return len(s) == 1 and s in 'abcdefghijklmnopqrstuvwxyz_ABCDIFJHIJKLMNOPQRSTUVWXYZ'
