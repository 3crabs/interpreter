class Node:

    def __init__(self, name: str, type_object: str, type_data: str, value: str):
        # имя узла (имя переменной, имя функции, ничего у констант и пустых узлов)
        self.name = name

        # тип объекта (функция, переменная, константа)
        # VAR
        # FUNCTION
        # EMPTY
        self.type_object = type_object

        # тип данных (тип переменной, тип константы)
        # SHORT
        # INTEGER
        # LONG
        # UNKNOWN
        self.type_data = type_data

        # значение (значение переменной, значение константы)
        self.value = value

        # параметры функции
        self.params = []

    def get_int(self):
        return int(self.value)

    def __str__(self):
        s = self.type_object

        if self.type_object == 'VAR':
            return s + ' ' + self.name + ' value=' + self.value

        if self.type_object == 'FUNCTION':
            return s + ' ' + self.name + ' params=' + str(self.params)

        return s


def create_var(name: str, type_data: str):
    return Node(name, 'VAR', type_data, '')


def create_function(name: str):
    return Node(name, 'FUNCTION', 'VOID', '')


def create_empty():
    return Node('', 'EMPTY', 'UNKNOWN', '')
