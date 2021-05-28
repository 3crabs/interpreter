class Node:

    def __init__(self, name: str, type_object: str, type_data: str, value: str):
        self.name = name

        # VAR
        # FUNCTION
        # EMPTY
        self.type_object = type_object

        # INT
        # INT 64
        self.type_data = type_data

        self.value = value

        self.params = []

        self.a = 0
        self.b = 0
        self.c = 0

    def get_int(self):
        return int(self.value)

    def set_position(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def get_position(self):
        return self.a, self.b, self.c

    def __str__(self):
        s = self.type_object

        if self.type_object == 'VAR':
            return s + ' ' + self.name + ' value=' + str(self.value)

        if self.type_object == 'FUNCTION':
            return s + ' ' + self.name + ' params=' + str(self.params)

        return s


def create_var(name: str, type_data: str):
    return Node(name, 'VAR', type_data, '')


def create_function(name: str):
    return Node(name, 'FUNCTION', 'VOID', '')


def create_empty():
    return Node('', 'EMPTY', 'UNKNOWN', '')
