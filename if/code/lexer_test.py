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
        err('Ожидался тип (short, int, long) или void')


def function():
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
    lex = next_lex()
    if lex.name != 'CURLY_LEFT':
        err('Ожидался {')
    lex = read_lex()
    if lex.name == 'ID':
        call_function()
    lex = next_lex()
    if lex.name != 'CURLY_RIGHT':
        err('Ожидался }')


def call_function():
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
    lex = next_lex()


def variable():
    lex = next_lex()
    if is_type(lex.name):
        err('Ожидался тип (short, int, long)')
    #  TODO


def err(text: str):
    print(text)
    exit(1)


if __name__ == '__main__':
    load_file('examples/print.c')
    program()
