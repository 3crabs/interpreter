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
    # test('examples/empty.c')
    # test('examples/hex.c')
    # test('examples/math.c')
    # test('examples/print.c')
    test('examples/switch.c')
    # test('examples/types.c')
