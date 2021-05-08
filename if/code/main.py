from scanner import next_lex, load_file

if __name__ == '__main__':
    load_file('examples/print.c')
    lex = next_lex()
    while lex.name != 'EOF':
        print(lex)
        lex = next_lex()
    print(lex)
