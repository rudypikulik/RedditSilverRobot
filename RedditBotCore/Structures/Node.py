# Written by Rudy Pikulik 7/17


class Node:

    def __init__(self, data, link=None):
        self.data = data
        self.link = link

    def get_next(self):
        return self.link

    def get_data(self):
        return self.data

    def set_next(self, link):
        self.link = link

    def set_data(self, x):
        self.data = x
