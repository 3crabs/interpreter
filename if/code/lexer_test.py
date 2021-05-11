from scanner import load_file, read_lex, next_lex


def is_type(name: str):
    return name in ['SHORT', 'INT', 'LONG']


def program():
    lex = read_lex()
    if lex.name == 'VOID':
        function()
    elif is_type(lex.name):
        variable()
    else:
        print('Ожидался тип (short, int, long) или void')


def function():
    lex = next_lex()
    if lex.name != 'VOID':
        print('Ожидался void')
    lex = next_lex()
    if lex.name != 'ID':
        raise Exception(f'Ожидался идентификатор {lex}')
    function_name = lex.value
    lex = next_lex()
    if lex.name != 'ROUND_LEFT':
        raise Exception(f'Ожидался ( {lex}')
    lex = next_lex()
    if lex.name != 'ROUND_RIGHT':
        raise Exception(f'Ожидался ) {lex}')
    composite_operator()


def composite_operator():
    lex = next_lex()
    if lex.name != 'CURLY_LEFT':
        print('Ожидался {')
    #  TODO
    if lex.name != 'CURLY_RIGHT':
        print('Ожидался }')


def variable():
    lex = next_lex()
    if is_type(lex.name):
        print('Ожидался тип (short, int, long)')
    #  TODO

if __name__ == '__main__':
    load_file('examples/print.c')
    program()
