from node import create_function, create_empty, create_var
from scanner import load_file, read_lex, next_lex, get_col, get_row, g, s
from tree import Tree

DEBUG_LEXER = False
DEBUG_TREE = False
GLOBAL_F = False
LOCAL_F = True

tree: Tree
current_tree: Tree


def is_type(name: str):
    return name in ['SHORT', 'INT', 'LONG']


def program():
    global tree, current_tree
    tree = None
    current_tree = None
    if DEBUG_LEXER:
        print('program')
    tree = Tree()
    current_tree = tree
    while True:
        if read_lex().name == 'EOF':
            return
        if read_lex().name == 'VOID':
            function()
        elif is_type(read_lex().name):
            variable()
        else:
            err('Ожидался тип (short, int, long) или void')


def function():
    global tree, current_tree, GLOBAL_F
    if DEBUG_LEXER:
        print('function')
    if next_lex().name != 'VOID':
        err('Ожидался void')
    lex = next_lex()
    if lex.name != 'ID':
        err(f'Ожидался идентификатор')
    name = lex.value
    if name == 'main':
        GLOBAL_F = tree
    fun_tree = create_function(name)
    current_tree = current_tree.add_left(fun_tree)
    new_tree = create_empty()
    current_tree = current_tree.add_right(new_tree)
    if next_lex().name != 'ROUND_LEFT':
        err(f'Ожидался (')
    while is_type(read_lex().name):
        t = next_lex()
        n = next_lex()
        fun_tree.params.append({"var_type": t.name, "var_name": n.value})
        new_tree = create_var(n.value, t.value)
        new_tree.value = '0'
        current_tree = current_tree.add_left(new_tree)
        if read_lex().name == 'COMMA':
            next_lex()
    if next_lex().name != 'ROUND_RIGHT':
        err(f'Ожидался )')
    x, y, z = g()
    fun_tree.s(x, y, z)
    composite_operator()
    t = current_tree
    while t.node.type_object != 'EMPTY':
        t = t.up
        break
    current_tree = t.up
    if name == 'main':
        GLOBAL_F = False


def assign_var():
    if DEBUG_LEXER:
        print('assign_var')
    name = next_lex().value
    next_lex()
    v = expression()
    var = current_tree.find_var(name)
    if GLOBAL_F and LOCAL_F:
        var.node.value = str(v)
    next_lex()


def composite_operator():
    global tree, current_tree
    if DEBUG_LEXER:
        print('composite_operator')
    if next_lex().name != 'CURLY_LEFT':
        err('Ожидался {')
    if current_tree.right is not None:
        new_tree = create_empty()
        current_tree = current_tree.add_left(new_tree)
    new_tree = create_empty()
    current_tree = current_tree.add_right(new_tree)
    run = True
    while run is True and read_lex().name != 'EOF' and read_lex().name != 'CURLY_RIGHT':
        run = False
        if read_lex().name == 'ID':
            a, b, c = g()
            next_lex()
            if read_lex().name == 'ROUND_LEFT':
                s(a, b, c)
                call_function()
            else:
                s(a, b, c)
                assign_var()
            run = True
        if is_type(read_lex().name):
            variable()
            run = True
        if read_lex().name == 'IF':
            call_if()
            run = True
        if run is False:
            expression()
            run = True
    t = current_tree
    while t.node.type_object != 'EMPTY':
        t = t.up
        break
    current_tree = t.up
    if next_lex().name != 'CURLY_RIGHT':
        err('Ожидался }')


def call_function():
    global tree, current_tree
    if DEBUG_LEXER:
        print('call_function')
    lex = next_lex()
    if lex.name != 'ID':
        err('Ожидался идентификатор')
    f = current_tree.find_function(lex.value)
    if lex.value != 'print' and f.node is None:
        err_sem(f'Функция {lex.value} не найдена')
    if next_lex().name != 'ROUND_LEFT':
        err('Ожидался (')
    v = expression()
    if lex.value == 'print':
        if GLOBAL_F and LOCAL_F:
            print(v)
    else:
        if GLOBAL_F and LOCAL_F:
            a, b, c = g()
            x, y, z = f.node.g()
            s(x, y, z)
            vname = f.node.params[0]["var_name"]
            var = current_tree.find_var(vname)
            var.node.value = str(v)
            composite_operator()
            s(a, b, c)
    while read_lex().name == 'COMMA':
        next_lex()
        expression()
    if next_lex().name != 'ROUND_RIGHT':
        err('Ожидался )')
    if next_lex().name != 'SEMICOLON':
        err('Ожидался ;')


def expression():
    global tree, current_tree
    if DEBUG_LEXER:
        print('expression')
    return expression_1()


def expression_1():
    global tree, current_tree
    if DEBUG_LEXER:
        print('expression_1')
    v = expression_2()
    while read_lex().name == 'EQ' or read_lex().name == 'NOT_EQ':
        op = next_lex()
        if op.name == 'EQ':
            v = v == expression_2()
        else:
            v = v != expression_2()
    return v


def expression_2():
    global tree, current_tree
    if DEBUG_LEXER:
        print('expression_2')
    v = expression_3()
    while read_lex().name == 'LESS' or read_lex().name == 'GREATER' or \
            read_lex().name == 'LESS_EQ' or read_lex().name == 'GREATER_EQ':
        op = next_lex()
        if op.name == 'LESS':
            v = v < expression_3()
        if op.name == 'GREATER':
            v = v > expression_3()
        if op.name == 'LESS_EQ':
            v = v <= expression_3()
        if op.name == 'GREATER_EQ':
            v = v >= expression_3()
    return v


def expression_3():
    global tree, current_tree
    if DEBUG_LEXER:
        print('expression_3')
    v = expression_4()
    while read_lex().name == 'R_SHIFT' or read_lex().name == 'L_SHIFT':
        op = next_lex()
        if op.name == 'R_SHIFT':
            v >>= expression_4()
        else:
            v <<= expression_4()
    return v


def expression_4():
    global tree, current_tree
    if DEBUG_LEXER:
        print('expression_4')
    v = expression_5()
    while read_lex().name == 'PLUS' or read_lex().name == 'MINUS':
        op = next_lex()
        if op.name == 'PLUS':
            v += expression_5()
        else:
            v -= expression_5()
    return v


def expression_5():
    global tree, current_tree
    if DEBUG_LEXER:
        print('expression_5')
    v = expression_6()
    while read_lex().name == 'STAR' or read_lex().name == 'SLASH' or read_lex().name == 'PERCENT':
        op = next_lex()
        if op.name == 'STAR':
            v *= expression_6()
        elif op.name == 'SLASH':
            a = expression_6()
            if a == 0:
                err_sem("делить на 0 нельзя")
            v /= a
        else:
            v %= expression_6()
    return v


def expression_6():
    global tree, current_tree
    if DEBUG_LEXER:
        print('expression_6')
    v = 1
    while read_lex().name == 'MINUS' or read_lex().name == 'PLUS':
        op = next_lex()
        if op.name == 'MINUS':
            v = -v
    return v * expression_7()


def expression_7():
    global tree, current_tree
    if DEBUG_LEXER:
        print('expression_7')
    if read_lex().name == 'ROUND_LEFT':
        next_lex()
        expression()
        if next_lex().name != 'ROUND_RIGHT':
            err('Ожидался )')
    else:
        if read_lex().name == 'CURLY_LEFT':
            composite_operator()
        else:
            if read_lex().name == 'DEC':
                return int(next_lex().value)
            else:
                vname = read_lex().value
                var = current_tree.find_var(vname)
                if var.node is None:
                    err_sem(f'переменная {vname} не найдена')
                next_lex()
                return int(var.node.value)


def variable():
    global tree, current_tree
    if DEBUG_LEXER:
        print('variable')
    lex = next_lex()
    if not is_type(lex.name):
        err('Ожидался тип (short, int, long)')
    type_var = lex.value
    f = True
    while f:
        lex = next_lex()
        if lex.name != 'ID':
            err('Ожидался идентификатор')
        var = create_var(lex.value, type_var)
        var.value = '0'
        fv = current_tree.find_var(var.name)
        if fv is not None and fv.node is not None and fv.node.type_object == 'VAR' and fv.node.name == var.name:
            err_sem(f'Переменная {var.name} уже существует')
        current_tree = current_tree.add_left(var)
        if read_lex().name == 'ASSIGN':
            next_lex()
            v = expression()
            var.value = v
        f = False
        if read_lex().name == 'COMMA':
            f = True
            next_lex()
    if next_lex().name != 'SEMICOLON':
        err('Ожидался ;')


def call_if():
    global tree, current_tree, LOCAL_F
    if DEBUG_LEXER:
        print('call_if')
    if next_lex().name != 'IF':
        err('Ожидался if')
    if next_lex().name != 'ROUND_LEFT':
        err('Ожидался (')
    v = expression()
    save_f = LOCAL_F
    LOCAL_F = v
    if next_lex().name != 'ROUND_RIGHT':
        err('Ожидался )')
    composite_operator()
    if read_lex().name == 'ELSE':
        LOCAL_F = not LOCAL_F
        next_lex()
        composite_operator()
    LOCAL_F = save_f


def err(text: str):
    print(text, 'Найден:', read_lex(), 'Строка:', get_row(), 'Символ:', get_col())
    exit(1)


def err_sem(text: str):
    print(text, 'Строка:', get_row(), 'Символ:', get_col())
    exit(1)


if __name__ == '__main__':
    # load_file('examples/empty.c')
    # program()
    # if DEBUG_TREE and tree is not None:
    #     tree.get_root().print(0)
    # print()
    #
    # load_file('examples/hex.c')
    # program()
    # if DEBUG_TREE and tree is not None:
    #     tree.get_root().print(0)
    # if DEBUG_LEXER:
    #     print()
    # print()

    # load_file('examples/if.c')
    # program()
    # if DEBUG_TREE and tree is not None:
    #     tree.get_root().print(0)
    # print()

    # load_file('examples/math.c')
    # program()
    # if DEBUG_TREE and tree is not None:
    #     tree.get_root().print(0)
    # print()

    # load_file('examples/recur.c')
    # program()
    # if DEBUG_TREE and tree is not None:
    #     tree.get_root().print(0)
    # print()

    # load_file('examples/descr.c')
    # program()
    # if DEBUG_TREE and tree is not None:
    #     tree.get_root().print(0)
    # print()

    load_file('examples/print.c')
    program()
    if DEBUG_TREE and tree is not None:
        tree.get_root().print(0)
    print()

    # load_file('examples/types.c')
    # program()
    # if DEBUG_TREE and tree is not None:
    #     tree.get_root().print(0)

    # load_file('examples/test.c')
    # program()
    # if DEBUG_TREE and tree is not None:
    #     tree.get_root().print(0)
    # print(current_tree.node)
