import numpy as np
import parser
import func_timeout
from sympy.parsing.sympy_parser import parse_expr
from sympy import *
import csv

OPERATORS = ["+", "-", "*", "/", "**"]
FUNCTIONS = ["sin", "cos", "tan"]

N_TERMS = 4


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


def Operations(a, b, op):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        return a / b


DEPTH = 3


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.depth = None
        self.children = []
        self.parent = None
        self.operator = None

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

        print(prefix + self.data + " (" + str(self.operator) + ")")
        if self.children:
            for child in self.children:
                child.print_tree()

    def print_equation(self, ):
        string = ''
        for i, child in enumerate(self.children):
            if i == 0:
                string += '('
            string += child.data

            if child.data in FUNCTIONS:
                string += child.print_equation()

            if i == len(self.children) - 1:
                string += ")"
            else:
                string += str(child.operator)

        return string

    def create_tree(self):
        if self.get_level() < DEPTH:
            n = np.random.randint(1, N_TERMS)
            for i in range(n):
                if self.data in FUNCTIONS or self.data == '':
                    if self.depth > 1:
                        selection = np.random.choice(["fn", "x", "n"], p=[0.5, 0.25, 0.25])
                        if selection == "fn":
                            child = TreeNode(np.random.choice(FUNCTIONS))
                        elif selection == "n":
                            child = TreeNode(str(np.random.randint(0, 10)))
                        else:
                            child = TreeNode(selection)
                    else:
                        selection = np.random.choice(["x", "n"])
                        if selection == "n":
                            child = TreeNode(str(np.random.randint(0, 10)))
                        else:
                            child = TreeNode(selection)
                    child.depth = self.depth - 1
                    if i < n - 1:
                        child.operator = np.random.choice(OPERATORS)
                    self.add_child(child)
            for ch in self.children:
                ch.create_tree()

    def calculate(self, var):
        calc = True
        oper = None
        for child in self.children:
            if child.data in FUNCTIONS:
                calc = False
        if calc == True:
            for child in self.children:
                if child.data == "x":
                    n = var
                else:
                    n = float(child.data)
                if oper != None:
                    print(str(old_n) + str(oper) + (str(n)))
                if child.operator != None:
                    oper = child.operator
                    print(oper)
                old_n = n

        for child in self.children:
            child.calculate(var)


CHOICES = ["fn", "x", "n"]

eqs = []
quantity = 100

Eq = TreeNode('')
Eq.depth = DEPTH
Eq.create_tree()
Eq.print_tree()
formula = Eq.print_equation()

while len(eqs) < quantity:
    Eq = TreeNode('')
    Eq.depth = DEPTH
    Eq.create_tree()
    equation = Eq.print_equation()

    if [equation] not in eqs:
        eqs.append([equation])

with open('innovators100.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(eqs)



def evaluation(c):
    return eval(c)


steps = 100
data = []
for eq in eqs:
    ex =  parse_expr(eq[0])
    x = Symbol('x')



    x1 = []
    x2 = []
    y = eq[0]
    print(y)
    for i in range(steps):
        x = np.random.randint(-10_000, 10_000)
        x1.append(x)
        try:
            sol = ex.evalf(subs={x: x})
            x2.append(sol)
        except:
            x2.append("-")
            break

    data.append([x1, x2, y])
    print(len(data))
print(data[100])
