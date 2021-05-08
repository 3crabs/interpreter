from scanner import next_lex

if __name__ == '__main__':
    lex = next_lex()
    while lex.name != 'EOF':
        print(lex)
        lex = next_lex()
    print(lex)
