# Written by Rudy Pikulik 07/17


from Structures.Stack import Stack


class Queue:

    def __init__(self):
        self.item_out = Stack()
        self.item_in = Stack()

    def enqueue(self, x):
        self.item_in.push(x)

    def dequeue(self):
        if self.item_out.get_size() == 0:
            while self.item_in.get_size() > 0:
                self.item_out.push(self.item_in.pop())
        return self.item_out.pop()

    def __len__(self):
        return self.item_out.get_size() + self.item_in.get_size()

    def contains(self, x):
        if self.item_out.contains(x) or self.item_in.contains(x):
            return True
        return False

    def peek(self):
        if self.item_out.get_size() == 0:
            while self.item_in.get_size() > 0:
                self.item_out.push(self.item_in.pop())
        return self.item_out.peek()
