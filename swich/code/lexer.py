from scanner import load_file, read_lexem, get_row, get_col
from tree import Tree

LOG_LEXER = False
LOG_TREE = False
GLOBAL_FLAG = False
RETURN_FLAG = False

new_tree: Tree
current_tree_node: Tree


def p():
    global new_tree, current_tree_node
    new_tree = None
    current_tree_node = None
    if LOG_LEXER:
        print('program')
    new_tree = Tree()
    current_tree_node = new_tree
    while True:
        if read_lexem().name == 'EOF':
            return
        if read_lexem().name == 'VOID':
            function()
        elif is_type(read_lexem().name):
            variable()
        else:
            error('Ожидался тип int, _int64 или void')


def function():
    pass


def variable():
    pass


def is_type(name: str):
    return name in ['INT', 'INT64']


def error(text: str):
    print(text, 'Найден:', read_lexem(), 'Строка:', get_row(), 'Символ:', get_col())
    exit(1)


def error_semantic(text: str):
    print(text, 'Строка:', get_row(), 'Символ:', get_col())
    exit(1)


if __name__ == '__main__':
    load_file('examples/code.c')
    p()
    if LOG_TREE and new_tree is not None:
        new_tree.get_root().print(0)
