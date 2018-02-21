# Written by Rudy Pikulik 7/17


from Structures.Node import Node


class Stack:

    def __init__(self):
        self.size = 0
        self.front = None

    def push(self, x):
        new_node = Node(x)
        if self.front is not None:
            new_node.set_next(self.front)
        self.front = new_node
        self.size += 1

    def pop(self):
        temp = self.front
        self.front = self.front.get_next()
        self.size -= 1
        return temp.get_data()

    def peek(self):
        return self.front.get_data()

    def get_size(self):
        return self.size

    def contains(self, x):
        node = self.front
        while node is not None:
            if node.get_data() == x:
                return True
            node = node.get_next()
        return False
