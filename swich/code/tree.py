from node import Node


class Tree:

    def __init__(self, left=None, right=None, up=None, node: Node = None):
        self.left = left
        self.right = right
        self.up = up
        self.node = node

    def add_left(self, node: Node):
        self.left = Tree(None, None, self, node)

    def add_right(self, node: Node):
        self.right = (None, None, self, node)

    def find_function(self, name: str):
        return self.find_node(name, 'FUNCTION')

    def find_var(self, name: str):
        return self.find_node(name, 'VAR')

    def find_node(self, name: str, type_object: str):
        t = self
        while t is not None and not (t.node.name == name and t.node.type_object == type_object):
            t = t.up
        return t

    def print(self, n: int):
        for i in range(n):
            print(end='\t')

        print(self.node)

        if self.right is not None:
            self.right.print(n + 1)

        if self.left is not None:
            self.left.print(n)
