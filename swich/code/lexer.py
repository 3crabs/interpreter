from node import create_function, create_empty, create_var
from scanner import load_file, read_lexem, get_row, get_col, next_lexem, get_state, set_state
from tree import Tree

LOG_LEXER = False
LOG_TREE = False
GLOBAL_FLAG = False
RETURN_FLAG = False

main_tree: Tree
current_tree_node: Tree


def s():
    global main_tree, current_tree_node
    main_tree = None
    current_tree_node = None
    if LOG_LEXER:
        print('program')
    main_tree = Tree()
    current_tree_node = main_tree
    while True:
        if read_lexem().name == 'EOF':
            return
        if read_lexem().name == 'VOID':
            function()
        elif is_type(read_lexem().name):
            variable()
        else:
            error('ожидался тип int, _int64 или void')


def function():
    global main_tree, current_tree_node, GLOBAL_FLAG
    if LOG_LEXER:
        print('function')
    if next_lexem().name != 'VOID':
        error('ожидался void')
    lex = next_lexem()
    if lex.name != 'ID':
        error('ожидался идентификатор')
    function_name = lex.value
    if function_name == 'main':
        GLOBAL_FLAG = True
    vv = current_tree_node.find_function(function_name)
    if vv is not None and vv.node is not None and vv.node.type_object == 'FUNCTION' and vv.node.name == function_name:
        error_semantic(f'функция {function_name} уже существует')
    function_tree = create_function(function_name)
    current_tree_node = current_tree_node.add_left(function_tree)
    new_empty_tree = create_empty()
    current_tree_node = current_tree_node.add_right(new_empty_tree)
    if next_lexem().name != 'ROUND_LEFT':
        error('ожидался (')
    while is_type(read_lexem().name):
        var_type = next_lexem()
        var_name = next_lexem()
        param = {"var_type": var_type.name, "var_name": var_name.value, "value": 0}
        function_tree.params.append(param)
        new_var_tree = create_var(var_name.value, var_type.name)
        new_var_tree.value = '0'
        current_tree_node = current_tree_node.add_left(new_var_tree)
        if read_lexem().name == 'COMMA':
            next_lexem()
    if next_lexem().name != 'ROUND_RIGHT':
        error('ожидался )')
    save_i, save_col, save_row = get_state()
    function_tree.set_position(save_i, save_col, save_row)
    composite_operator()
    current_tree_node = current_tree_node.find_function(function_name)
    if function_name == 'main':
        GLOBAL_FLAG = False


def variable():
    global main_tree, current_tree_node
    if LOG_LEXER:
        print('variable')
    lex = next_lexem()
    if not is_type(lex.name):
        error('ожидался тип int или _int64')
    variable_type = lex.name
    has_variable = True
    while has_variable:
        lex = next_lexem()
        if lex.name != 'ID':
            error('ожидался идентификатор')
        variable_name = lex.value
        variable_tree = create_var(variable_name, variable_type)
        variable_tree.value = '0'
        fv = current_tree_node.find_var(variable_tree.name)
        if fv is not None and fv.node is not None and fv.node.type_object == 'VAR' and fv.node.name == variable_tree.name:
            error_semantic(f'переменная {variable_tree.name} уже существует')
        current_tree_node = current_tree_node.add_left(variable_tree)
        if read_lexem().name == 'ASSIGN':
            next_lexem()
            v = exp()
            if GLOBAL_FLAG:
                variable_tree.value = v
                variable_type = variable_tree.type_data
                variable_name = variable_tree.name
                check_types(variable_type, v)
                print(variable_type, variable_name, "=", str(v))
        has_variable = False
        if read_lexem().name == 'COMMA':
            has_variable = True
            next_lexem()
    if next_lexem().name != 'SEMICOLON':
        error('ожидался ;')


def composite_operator(switch_v=None):
    global main_tree, current_tree_node, GLOBAL_FLAG, RETURN_FLAG
    if LOG_LEXER:
        print('composite_operator')
    if next_lexem().name != 'CURLY_LEFT':
        error('ожидался {')
    save_flag = GLOBAL_FLAG
    if current_tree_node.right is not None:
        new_empty_tree = create_empty()
        current_tree_node = current_tree_node.add_left(new_empty_tree)
    new_empty_tree = create_empty()
    current_tree_node = current_tree_node.add_right(new_empty_tree)
    run = True
    while run is True and read_lexem().name != 'EOF' and read_lexem().name != 'CURLY_RIGHT':
        run = False
        if read_lexem().name == 'RETURN':
            if GLOBAL_FLAG:
                RETURN_FLAG = True
            GLOBAL_FLAG = False
            next_lexem()
            next_lexem()
            run = True
        if read_lexem().name == 'ID':
            save_i, save_col, save_row = get_state()
            next_lexem()
            if read_lexem().name == 'ROUND_LEFT':
                set_state(save_i, save_col, save_row)
                call_function()
            else:
                set_state(save_i, save_col, save_row)
                assign_var()
            run = True
        if read_lexem().name == 'SWITCH':
            next_lexem()
            if next_lexem().name != 'ROUND_LEFT':
                error('ожидался (')
            v = exp()
            if next_lexem().name != 'ROUND_RIGHT':
                error('ожидался )')
            save_f = GLOBAL_FLAG
            GLOBAL_FLAG = False
            composite_operator(v)
            GLOBAL_FLAG = save_f
            run = True
        if read_lexem().name == 'CASE':
            next_lexem()
            v = exp()
            if switch_v == v:
                GLOBAL_FLAG = True
            if next_lexem().name != 'COLON':
                error('ожидался :')
            run = True
        if read_lexem().name == 'DEFAULT':
            next_lexem()
            GLOBAL_FLAG = not GLOBAL_FLAG
            if next_lexem().name != 'COLON':
                error('ожидался :')
            run = True
        if is_type(read_lexem().name):
            variable()
            run = True
        if run is False:
            if read_lexem().name == 'CURLY_RIGHT':
                next_lexem()
            else:
                exp()
                run = True
    t = current_tree_node
    while t.node.type_object != 'EMPTY':
        t = t.up
        break
    current_tree_node = t.up
    if next_lexem().name != 'CURLY_RIGHT':
        error('ожидался }')
    GLOBAL_FLAG = save_flag


def call_function():
    if LOG_LEXER:
        print('call_function')
    lex = next_lexem()
    if lex.name != 'ID':
        error('ожидался идентификатор')
    function_tree = current_tree_node.find_function(lex.value)
    if lex.value != 'print' and function_tree.node is None:
        error_semantic(f'функция {lex.value} не найдена')
    if next_lexem().name != 'ROUND_LEFT':
        error('ожидался (')
    params = []
    if read_lexem().name != 'ROUND_RIGHT':
        v = exp()
        params.append(v)
        while read_lexem().name == 'COMMA':
            next_lexem()
            v = exp()
            params.append(v)
    if next_lexem().name != 'ROUND_RIGHT':
        error('ожидался )')
    if GLOBAL_FLAG:
        run_function(function_tree, params)
    if next_lexem().name != 'SEMICOLON':
        error('ожидался ;')


def assign_var():
    if LOG_LEXER:
        print('assign_var')
    variable_name = next_lexem().value
    next_lexem()
    v = exp()
    var = current_tree_node.find_var(variable_name)
    if var.node is None:
        error_semantic(f'переменная {variable_name} не найдена')
    if GLOBAL_FLAG:
        var.node.value = str(v)
        variable_type = var.node.type_data
        check_types(variable_type, v)
        print(variable_type, variable_name, "=", str(v))
    next_lexem()


def run_function(function_tree, params):
    global RETURN_FLAG, current_tree_node
    save_return_flag = RETURN_FLAG
    old_i, old_cal, old_row = get_state()
    function_i, function_cal, function_row = function_tree.node.get_position()
    set_state(function_i, function_cal, function_row)
    save_tree = current_tree_node
    current_tree = function_tree.right
    while current_tree.left:
        current_tree = current_tree.left

    old_params = []
    for i in range(len(function_tree.node.params)):
        name = function_tree.node.params[i]["var_name"]
        old_params.append(current_tree.find_var(name).node.value)

    for i in range(len(function_tree.node.params)):
        name = function_tree.node.params[i]["var_name"]
        current_tree.find_var(name).node.value = str(params[i])

    composite_operator()

    for i in range(len(function_tree.node.params)):
        name = function_tree.node.params[i]["var_name"]
        current_tree.find_var(name).node.value = str(old_params[i])

    set_state(old_i, old_cal, old_row)
    RETURN_FLAG = save_return_flag
    current_tree_node = save_tree


def exp():
    if LOG_LEXER:
        print('exp')
    return exp_1()


def exp_1():
    if LOG_LEXER:
        print('exp_1')
    v = exp_2()
    while read_lexem().name == 'EQ' or read_lexem().name == 'NOT_EQ':
        op = next_lexem()
        if op.name == 'EQ':
            v2 = exp_2()
            if GLOBAL_FLAG:
                v = v == v2
        else:
            v2 = exp_2()
            if GLOBAL_FLAG:
                v = v != v2
    return v


def exp_2():
    if LOG_LEXER:
        print('exp_2')
    v = exp_3()
    while read_lexem().name == 'LESS' or read_lexem().name == 'GREATER' or read_lexem().name == 'LESS_EQ' or read_lexem().name == 'GREATER_EQ':
        op = next_lexem()
        if op.name == 'LESS':
            v3 = exp_3()
            if GLOBAL_FLAG:
                v = v < v3
        if op.name == 'GREATER':
            v3 = exp_3()
            if GLOBAL_FLAG:
                v = v > v3
        if op.name == 'LESS_EQ':
            v3 = exp_3()
            if GLOBAL_FLAG:
                v = v <= v3
        if op.name == 'GREATER_EQ':
            v3 = exp_3()
            if GLOBAL_FLAG:
                v = v >= v3
    return v


def exp_3():
    if LOG_LEXER:
        print('exp_3')
    v = exp_4()
    while read_lexem().name == 'R_SHIFT' or read_lexem().name == 'L_SHIFT':
        op = next_lexem()
        if op.name == 'R_SHIFT':
            v4 = exp_4()
            if GLOBAL_FLAG:
                v >>= v4
        else:
            v4 = exp_4()
            if GLOBAL_FLAG:
                v <<= v4
    return v


def exp_4():
    if LOG_LEXER:
        print('exp_4')
    v = exp_5()
    while read_lexem().name == 'PLUS' or read_lexem().name == 'MINUS':
        op = next_lexem()
        if op.name == 'PLUS':
            v5 = exp_5()
            if GLOBAL_FLAG:
                v += v5
        else:
            v5 = exp_5()
            if GLOBAL_FLAG:
                v -= v5
    return v


def exp_5():
    if LOG_LEXER:
        print('exp_5')
    v = exp_6()
    while read_lexem().name == 'STAR' or read_lexem().name == 'SLASH' or read_lexem().name == 'PERCENT':
        op = next_lexem()
        if op.name == 'STAR':
            v6 = exp_6()
            if GLOBAL_FLAG:
                v *= v6
        elif op.name == 'SLASH':
            v6 = exp_6()
            a = v6
            if GLOBAL_FLAG:
                if a == 0:
                    error_semantic("делить на 0 нельзя")
                v /= a
        else:
            v6 = exp_6()
            if GLOBAL_FLAG:
                v %= v6
    return v


def exp_6():
    if LOG_LEXER:
        print('exp_6')
    v = 1
    while read_lexem().name == 'MINUS' or read_lexem().name == 'PLUS':
        op = next_lexem()
        if op.name == 'MINUS':
            v = -v
    return v * exp_7()


def exp_7():
    if LOG_LEXER:
        print('exp_7')
    if read_lexem().name == 'ROUND_LEFT':
        next_lexem()
        v = exp()
        if next_lexem().name != 'ROUND_RIGHT':
            error('ожидался )')
        return v
    else:
        if read_lexem().name == 'CURLY_LEFT':
            composite_operator()
        else:
            if read_lexem().name == 'DEC':
                return int(next_lexem().value)
            else:
                variable_name = read_lexem().value
                var = current_tree_node.find_var(variable_name)
                if var.node is None:
                    error_semantic(f'переменная {variable_name} не найдена')
                next_lexem()
                return int(var.node.value)


def is_type(name: str):
    return name in ['INT', 'INT64']


def check_types(t, v):
    if t == 'INT':
        if v > 2 ** 31 - 1:
            error_semantic('число слишком большое для типа int')
        if v < -2 ** 31:
            error_semantic('число слишком маленькое для типа int')
    if t == 'INT64':
        if v > 2 ** 63 - 1:
            error_semantic('число слишком большое для типа int64')
        if v < -2 ** 63:
            error_semantic('число слишком маленькое для типа int64')


def error(text: str):
    print(text, 'Найден:', read_lexem(), 'Строка:', get_row(), 'Символ:', get_col())
    exit(1)


def error_semantic(text: str):
    print(text, 'Строка:', get_row(), 'Символ:', get_col())
    exit(1)


if __name__ == '__main__':
    load_file('examples/code.c')
    s()
    if LOG_TREE and main_tree is not None:
        main_tree.get_root().print(0)
