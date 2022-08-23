from Equation import Expression
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, sympify, S
from sympy.parsing.sympy_parser import parse_expr
from sympy.calculus.util import continuous_domain
OPERATORS = ["+", "-", "*", "/", "^"]
FUNCTIONS = ["Sin", "Cos", "Tan", "Log"]

N_TERMS = 5


def create_row():
    str_row = "("
    cs = np.random.randint(2, N_TERMS)
    for i in range(cs):
        ch = np.random.choice(OPERATORS)
        n = np.random.randint(0, 2)
        app = "x"
        if n == 1:
            app = str(np.random.randint(0, 999999))
        if i < cs - 1:
            str_row += app + ch
        else:
            str_row += app

    str_row += ")"
    return str_row

DEPTH = 3


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.depth = None
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + '|__' if self.parent else ""

        print(prefix + self.data)
        if self.children:
            for child in self.children:
                child.print_tree()

    def print_equation(self, ):
        string = ''
        for i, child in enumerate(self.children):
            if i == 0:
                string += '['
            if child.data == "fn":
                string += np.random.choice(FUNCTIONS)
            elif child.data == "n":
                string += str(np.random.randint(0,1000))
            else:
                string += child.data

            if child.data == "fn":
                string += child.print_equation()

            if i == len(self.children) - 1:
                string += "]"
            else:
                string += np.random.choice(OPERATORS)

        return string

    def create_tree(self):
        if self.get_level() < DEPTH:
            n = np.random.randint(1, N_TERMS)
            for i in range(n):
                if self.data not in ["x", "n"]:
                    if self.depth > 1:
                        child = TreeNode(np.random.choice(["fn", "x", "n"], p=[0.5, 0.25, 0.25]))
                    else:
                        child = TreeNode(np.random.choice(["x", "n"]))
                    child.depth = self.depth - 1
                    self.add_child(child)
            for ch in self.children:
                ch.create_tree()


CHOICES = ["fn", "x", "n"]


eqs = []
while len(eqs) < 10_000:
    Eq = TreeNode('')
    Eq.depth = DEPTH
    Eq.create_tree()
    equation = Eq.print_equation()

    if equation not in eqs:
        eqs.append(equation)

idxs = np.random.randint(0,10_000, 5)
print(np.array(eqs)[idxs])
for i, form in enumerate(np.array(eqs)[idxs]):
    form = form[:-1]
    form =form[1:]

    print(form)

    print("--------------")