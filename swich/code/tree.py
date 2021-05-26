from node import Node


class Tree:

    def __init__(self, left=None, right=None, up=None, node: Node = None):
        self.left = left
        self.right = right
        self.up = up
        self.node = node

    def add_left(self, node: Node):
        self.left = Tree(None, None, self, node)
        return self.left

    def add_right(self, node: Node):
        self.right = Tree(None, None, self, node)
        return self.right

    def find_function(self, name: str):
        return self.find_node(name, 'FUNCTION')

    def find_var(self, name: str):
        return self.find_node(name, 'VAR')

    def find_node(self, name: str, type_object: str):
        t = self
        while t is not None and t.node is not None and not (t.node.name == name and t.node.type_object == type_object):
            t = t.up
        return t

    def print(self, n: int):
        if n == -1:
            print(f'this=({self.node})', end='')
            if self.up is not None:
                print(f'  up=({self.up.node})', end='')
            if self.left is not None:
                print(f'  left=({self.left.node})', end='')
            if self.right is not None:
                print(f'  right=({self.right.node})', end='')
            print()
            return

        for i in range(n):
            print(end='\t')

        print(f'this=({self.node})', end='')
        # if self.up is not None:
        #     print(f'  up=({self.up.node})', end='')
        # if self.left is not None:
        #     print(f'  left=({self.left.node})', end='')
        # if self.right is not None:
        #     print(f'  right=({self.right.node})', end='')
        print()

        if self.right is not None:
            self.right.print(n + 1)

        if self.left is not None:
            self.left.print(n)

    def get_root(self):
        t = self
        root_t = t.up
        while root_t is not None:
            t = t.up
            root_t = t.up
        return t
