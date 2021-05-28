class Lexem:

    def __init__(self, name: str = '', value: str = ''):
        self.name = name
        self.value = value

    def __str__(self) -> str:
        if self.value == '':
            return f'{self.name}'
        else:
            return f'{self.name}: {self.value}'
