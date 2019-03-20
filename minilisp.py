from sys import argv
import math
import re
import operator
from functools import partial
from functools import reduce

Symbol = str
Number = (int, float)
Atom   = (Symbol, Number)
List   = list
Exp    = (Atom, List)

DEBUG = False

def readfile(filename):
    return open(filename).read()

def lex(string):
    return (tokenize(t) for t in string.replace('(', ' ( ').replace(')', ' ) ').split())

def tokenize(t):
    if   re.match(r'\d+$', t):      return int(t)
    elif re.match(r'\d+\.\d+', t):  return float(t)
    else:                           return t

def eval(env, stmt):
    if DEBUG:
        print('Stmt:', stmt)
    if stmt in ('#t', '#f'):
        return stmt == '#t'
    if isinstance(stmt, Symbol):        # Variable name
        if stmt[0] == '"': return stmt[1:-1]
        return env[stmt]
    if isinstance(stmt, Number):      # Int or float
        return stmt
    if stmt[0] == 'if':
        _, test, cons, alt = stmt
        return eval(env, cons) if eval(env, test) else eval(env, alt)
    if stmt[0] == 'let':              # Variable definitions
        _, symbol, exp = stmt
        env[symbol] = eval(env, exp)
    elif stmt[0] == 'fn':
        return lambda *xs: eval({**env, **{x: y for x, y in zip([x for x in stmt[1]], xs)}}, stmt[2])
    elif stmt[0] == 'begin':
        if DEBUG:
            print("Inside begin")
            print(stmt)
        for s in stmt[1:]:
            eval(env, s)
    else:
        proc = eval(env, stmt[0])
        args = [eval(env, arg) for arg in stmt[1:]]
        return proc(*args)

def parse(tokens):
    tree = []
    t = next(tokens)
    while True:
        if t == '(': tree.append(parse(tokens))
        elif t == ')': return tree
        elif isinstance(t, str) and t[0] == '"':
            string = [t]
            while True:
                if t[-1] == '"':
                    break
                t = next(tokens)
                string.append(t)
            tree.append(' '.join(string))
        else: tree.append(t)

        try:
            t = next(tokens)
        except:
            return tree

def main_eval(env, stmts):
    for stmt in stmts:
        eval(env, stmt)

def main():
    filename = argv[1]
    global_env = {**vars(math)}
    global_env.update({
        'println': lambda x: print(x),
        'print': lambda x: print(x, end=' '),
        '+': operator.add,
        '-': lambda *x: reduce(operator.sub, x),
        '*': lambda *x: reduce(operator.mul, x),
        '/': operator.floordiv,
        '%': operator.mod,
        'eq?': operator.eq,
        'list?': lambda x: isinstance(x, list),
    })
    tokens = lex(readfile(filename))
    main_eval(global_env, parse(tokens))

if __name__ == "__main__":
    main()
