from node import create_function, create_empty, create_var
from scanner import load_file, read_lex, next_lex, get_col, get_row, g, s
from tree import Tree

DEBUG_LEXER = False
DEBUG_TREE = False
GLOBAL_F = False
RET_F = False

tree: Tree
current_tree: Tree


def is_type(name: str):
    return name in ['SHORT', 'INT']


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
        GLOBAL_F = True
    fun_tree = create_function(name)
    current_tree = current_tree.add_left(fun_tree)
    new_tree = create_empty()
    current_tree = current_tree.add_right(new_tree)
    if next_lex().name != 'ROUND_LEFT':
        err(f'Ожидался (')
    while is_type(read_lex().name):
        t = next_lex()
        n = next_lex()
        js = {"var_type": t.name, "var_name": n.value, "value": 0}
        fun_tree.params.append(js)
        new_tree = create_var(n.value, t.name)
        new_tree.value = '0'
        current_tree = current_tree.add_left(new_tree)
        if read_lex().name == 'COMMA':
            next_lex()
    if next_lex().name != 'ROUND_RIGHT':
        err(f'Ожидался )')
    x, y, z = g()
    fun_tree.s(x, y, z)
    composite_operator()
    current_tree = current_tree.find_function(name)
    if name == 'main':
        GLOBAL_F = False


def check_types(vtype, v):
    if vtype == 'SHORT':
        if v > 2 ** 15 - 1:
            err_sem('Число слишком большое для типа short')
        if v < -2 ** 15:
            err_sem('Число слишком маленькое для типа short')
    if vtype == 'INT':
        if v > 2 ** 31 - 1:
            err_sem(f'Число слишком большое для типа int {v}')
        if v < -2 ** 31:
            err_sem('Число слишком маленькое для типа int')


def assign_var():
    global GLOBAL_F
    if DEBUG_LEXER:
        print('assign_var')
    vname = next_lex().value
    next_lex()
    v = expression()
    var = current_tree.find_var(vname)
    if GLOBAL_F:
        var.node.value = str(v)
        vtype = var.node.type_data
        check_types(vtype, v)
        print(vtype, vname, "=", str(v))
    next_lex()


def composite_operator():
    global tree, current_tree, GLOBAL_F, RET_F
    if DEBUG_LEXER:
        print('composite_operator')
    if next_lex().name != 'CURLY_LEFT':
        err('Ожидался {')
    save_f = GLOBAL_F
    if current_tree.right is not None:
        new_tree = create_empty()
        current_tree = current_tree.add_left(new_tree)
    new_tree = create_empty()
    current_tree = current_tree.add_right(new_tree)
    run = True
    while run is True and read_lex().name != 'EOF' and read_lex().name != 'CURLY_RIGHT':
        run = False
        if read_lex().name == 'RETURN':
            if GLOBAL_F:
                RET_F = True
            GLOBAL_F = False
            next_lex()
            next_lex()
            run = True
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
    GLOBAL_F = save_f


def run_f(f, new_l):
    global current_tree, RET_F, GLOBAL_F
    # print('s_ret_f', RET_F, GLOBAL_F)
    save_ret_f = RET_F
    old_a, old_b, old_c = g()
    a, b, c = f.node.g()
    s(a, b, c)
    save_tree = current_tree
    current_tree = f.right
    while current_tree.left:
        current_tree = current_tree.left

    old_l = []
    for i in range(len(f.node.params)):
        name = f.node.params[i]["var_name"]
        old_l.append(current_tree.find_var(name).node.value)

    for i in range(len(f.node.params)):
        name = f.node.params[i]["var_name"]
        current_tree.find_var(name).node.value = str(new_l[i])

    composite_operator()

    for i in range(len(f.node.params)):
        name = f.node.params[i]["var_name"]
        current_tree.find_var(name).node.value = str(old_l[i])

    s(old_a, old_b, old_c)
    RET_F = save_ret_f
    current_tree = save_tree
    # print('e_ret_f', RET_F, GLOBAL_F)


def call_function():
    global tree, current_tree, GLOBAL_F
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
    l = []
    if read_lex().name != 'ROUND_RIGHT':
        v = expression()
        l.append(v)
        while read_lex().name == 'COMMA':
            next_lex()
            v = expression()
            l.append(v)
    if next_lex().name != 'ROUND_RIGHT':
        err('Ожидался )')
    if GLOBAL_F:
        run_f(f, l)
    if next_lex().name != 'SEMICOLON':
        err('Ожидался ;')


def expression():
    global tree, current_tree
    if DEBUG_LEXER:
        print('expression')
    return expression_1()


def expression_1():
    global tree, current_tree, GLOBAL_F
    if DEBUG_LEXER:
        print('expression_1')
    v = expression_2()
    while read_lex().name == 'EQ' or read_lex().name == 'NOT_EQ':
        op = next_lex()
        if op.name == 'EQ':
            v2 = expression_2()
            if GLOBAL_F:
                v = v == v2
        else:
            v2 = expression_2()
            if GLOBAL_F:
                v = v != v2
    return v


def expression_2():
    global tree, current_tree, GLOBAL_F
    if DEBUG_LEXER:
        print('expression_2')
    v = expression_3()
    while read_lex().name == 'LESS' or read_lex().name == 'GREATER' or \
            read_lex().name == 'LESS_EQ' or read_lex().name == 'GREATER_EQ':
        op = next_lex()
        if op.name == 'LESS':
            v3 = expression_3()
            if GLOBAL_F:
                v = v < v3
        if op.name == 'GREATER':
            v3 = expression_3()
            if GLOBAL_F:
                v = v > v3
        if op.name == 'LESS_EQ':
            v3 = expression_3()
            if GLOBAL_F:
                v = v <= v3
        if op.name == 'GREATER_EQ':
            v3 = expression_3()
            if GLOBAL_F:
                v = v >= v3
    return v


def expression_3():
    global tree, current_tree, GLOBAL_F
    if DEBUG_LEXER:
        print('expression_3')
    v = expression_4()
    while read_lex().name == 'R_SHIFT' or read_lex().name == 'L_SHIFT':
        op = next_lex()
        if op.name == 'R_SHIFT':
            v4 = expression_4()
            if GLOBAL_F:
                v >>= v4
        else:
            v4 = expression_4()
            if GLOBAL_F:
                v <<= v4
    return v


def expression_4():
    global tree, current_tree, GLOBAL_F
    if DEBUG_LEXER:
        print('expression_4')
    v = expression_5()
    while read_lex().name == 'PLUS' or read_lex().name == 'MINUS':
        op = next_lex()
        if op.name == 'PLUS':
            v5 = expression_5()
            if GLOBAL_F:
                v += v5
        else:
            v5 = expression_5()
            if GLOBAL_F:
                v -= v5
    return v


def expression_5():
    global tree, current_tree, GLOBAL_F
    if DEBUG_LEXER:
        print('expression_5')
    v = expression_6()
    while read_lex().name == 'STAR' or read_lex().name == 'SLASH' or read_lex().name == 'PERCENT':
        op = next_lex()
        if op.name == 'STAR':
            v6 = expression_6()
            if GLOBAL_F:
                v *= v6
        elif op.name == 'SLASH':
            v6 = expression_6()
            a = v6
            if GLOBAL_F:
                if a == 0:
                    err_sem("делить на 0 нельзя")
                v /= a
        else:
            v6 = expression_6()
            if GLOBAL_F:
                v %= v6
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
        v = expression()
        if next_lex().name != 'ROUND_RIGHT':
            err('Ожидался )')
        return v
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
    type_var = lex.name
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
            if GLOBAL_F:
                var.value = v
                vtype = var.type_data
                vname = var.name
                check_types(vtype, v)
                print(vtype, vname, "=", str(v))
        f = False
        if read_lex().name == 'COMMA':
            f = True
            next_lex()
    if next_lex().name != 'SEMICOLON':
        err('Ожидался ;')


def call_if():
    global tree, current_tree, GLOBAL_F
    if DEBUG_LEXER:
        print('call_if')
    if next_lex().name != 'IF':
        err('Ожидался if')
    if next_lex().name != 'ROUND_LEFT':
        err('Ожидался (')
    v = expression()
    save_f = GLOBAL_F
    GLOBAL_F = v and save_f and not RET_F
    # print('if', GLOBAL_F)
    if next_lex().name != 'ROUND_RIGHT':
        err('Ожидался )')
    composite_operator()
    if read_lex().name == 'ELSE':
        GLOBAL_F = not v and save_f and not RET_F
        # print('else', GLOBAL_F)
        next_lex()
        composite_operator()
    GLOBAL_F = save_f and not RET_F
    # print('end', GLOBAL_F)


def err(text: str):
    print(text, 'Найден:', read_lex(), 'Строка:', get_row(), 'Символ:', get_col())
    exit(1)


def err_sem(text: str):
    print(text, 'Строка:', get_row(), 'Символ:', get_col())
    exit(1)


if __name__ == '__main__':
    load_file('examples/empty.c')
    program()
    if DEBUG_TREE and tree is not None:
        tree.get_root().print(0)
    print()
