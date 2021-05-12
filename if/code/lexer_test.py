from scanner import load_file, read_lex, next_lex, get_col, get_row

DEBUG = True


def is_type(name: str):
    return name in ['SHORT', 'INT', 'LONG']


def program():
    if DEBUG:
        print('program')
    lex = read_lex()
    if lex.name == 'EOF':
        return
    if lex.name == 'VOID':
        function()
    elif is_type(lex.name):
        variable()
    else:
        err('Ожидался тип (short, int, long) или void')


def function():
    if DEBUG:
        print('function')
    lex = next_lex()
    if lex.name != 'VOID':
        err('Ожидался void')
    lex = next_lex()
    if lex.name != 'ID':
        err(f'Ожидался идентификатор {lex}')
    lex = next_lex()
    if lex.name != 'ROUND_LEFT':
        err(f'Ожидался ( {lex}')
    lex = next_lex()
    if lex.name != 'ROUND_RIGHT':
        err(f'Ожидался ) {lex}')
    composite_operator()


def composite_operator():
    if DEBUG:
        print('composite_operator')
    lex = next_lex()
    if lex.name != 'CURLY_LEFT':
        err('Ожидался {')
    lex = read_lex()
    while lex.name != 'EOF' and lex.name != 'CURLY_RIGHT':
        if lex.name == 'ID':
            call_function()
        if is_type(lex.name):
            variable()
        if lex.name == 'IF':
            call_if()
        lex = read_lex()
    if lex.name != 'CURLY_RIGHT':
        err('Ожидался }')


def call_function():
    if DEBUG:
        print('call_function')
    lex = next_lex()
    if lex.name != 'ID':
        err('Ожидался идентификатор')
    lex = next_lex()
    if lex.name != 'ROUND_LEFT':
        err('Ожидался (')
    expression()
    lex = next_lex()
    if lex.name != 'ROUND_RIGHT':
        err('Ожидался )')
    lex = next_lex()
    if lex.name != 'SEMICOLON':
        err('Ожидался ;')


def expression():
    if DEBUG:
        print('expression')
    expression_1()


def expression_1():
    if DEBUG:
        print('expression_1')
    expression_2()
    lex = read_lex()
    while lex.name == 'EQ' or lex.name == 'NOT_EQ':
        next_lex()
        expression_2()
        lex = read_lex()


def expression_2():
    if DEBUG:
        print('expression_2')
    expression_3()
    lex = read_lex()
    while lex.name == 'LESS' or lex.name == 'GREATER' or lex.name == 'LESS_EQ' or lex.name == 'GREATER_EQ':
        next_lex()
        expression_3()
        lex = read_lex()


def expression_3():
    if DEBUG:
        print('expression_3')
    expression_4()
    lex = read_lex()
    while lex.name == 'R_SHIFT' or lex.name == 'L_SHIFT':
        next_lex()
        expression_4()
        lex = read_lex()


def expression_4():
    if DEBUG:
        print('expression_4')
    expression_5()
    lex = read_lex()
    while lex.name == 'PLUS' or lex.name == 'MINUS':
        next_lex()
        expression_5()
        lex = read_lex()


def expression_5():
    if DEBUG:
        print('expression_5')
    expression_6()
    lex = read_lex()
    while lex.name == 'STAR' or lex.name == 'SLASH' or lex.name == 'PERCENT':
        next_lex()
        expression_6()
        lex = read_lex()


def expression_6():
    if DEBUG:
        print('expression_6')
    lex = read_lex()
    while lex.name == 'MINUS' or lex.name == 'PLUS':
        next_lex()
        lex = read_lex()
    expression_7()


def expression_7():
    if DEBUG:
        print('expression_7')
    next_lex()


def variable():
    if DEBUG:
        print('variable')
    lex = next_lex()
    if not is_type(lex.name):
        err('Ожидался тип (short, int, long)')
    f = True
    while f:
        lex = next_lex()
        if lex.name != 'ID':
            err('Ожидался идентификатор')
        lex = next_lex()
        if lex.name != 'ASSIGN':
            err('Ожидался =')
        expression()
        lex = read_lex()
        f = False
        if lex.name == 'COMMA':
            f = True
            next_lex()
    lex = next_lex()
    if lex.name != 'SEMICOLON':
        err('Ожидался ;')


def call_if():
    if DEBUG:
        print('call_if')
    lex = next_lex()
    if not lex.name == 'IF':
        err('Ожидался if')
    lex = next_lex()
    if lex.name != 'ROUND_LEFT':
        err('Ожидался (')
    expression()
    lex = next_lex()
    if lex.name != 'ROUND_RIGHT':
        err('Ожидался )')
    composite_operator()
    lex = read_lex()
    if lex.name == 'ELSE':
        next_lex()
        composite_operator()


def err(text: str):
    print(text, 'Найден:', read_lex(), 'Строка:', get_row(), 'Символ:', get_col())
    exit(1)


if __name__ == '__main__':
    load_file('examples/empty.c')
    program()
    if DEBUG:
        print()
    load_file('examples/hex.c')
    program()
    if DEBUG:
        print()
    load_file('examples/if.c')
    program()
    if DEBUG:
        print()
    load_file('examples/math.c')
    program()
    if DEBUG:
        print()
    load_file('examples/print.c')
    program()
    if DEBUG:
        print()
    load_file('examples/types.c')
    program()
