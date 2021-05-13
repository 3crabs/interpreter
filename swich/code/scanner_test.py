from scanner import next_lex, load_file


def test(path: str):
    load_file(path)
    lex = next_lex()
    while lex.name != 'EOF' and lex.name != 'ERROR':
        print(lex)
        lex = next_lex()
    print(lex)
    print()


if __name__ == '__main__':
    test('../../swich/code/examples/empty.c')
    test('../../swich/code/examples/hex.c')
    test('examples/swich.c')
    test('../../swich/code/examples/math.c')
    test('../../swich/code/examples/print.c')
    test('../../swich/code/examples/types.c')
    test('../../swich/code/examples/error.c')
