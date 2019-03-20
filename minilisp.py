"""A basic scheme interpreter"""
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

def readfile(filename):
    return open(filename).read()

def lex(string):
    return (tokenize(t) for t in string.replace('(', ' ( ').replace(')', ' ) ').split())

def tokenize(t):
    if re.match(r'\d+$', t): return int(t)
    elif re.match(r'\d+\.\d+', t): return float(t)
    elif t == '#t': return True
    elif t == '#f': return False
    else: return t

def eval(env, stmt):
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
    else:
        proc = eval(env, stmt[0])
        args = [eval(env, arg) for arg in stmt[1:]]
        return proc(*args)

def parse(tokens):
    tree = []
    t = next(tokens)
    while t:
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
    global_env = {**vars(math)}
    global_env.update({
        'println': print,
        '+': lambda *x: sum(x),
        '-': lambda *x: reduce(operator.sub, x),
        '*': lambda *x: reduce(operator.mul, x),
        '/': operator.floordiv,
        '%': operator.mod,
        'eq?': lambda *x: all(operator.eq(a, b) for a, b in zip(x, x[:1])),
        'list': lambda *x: x,
        'list?': lambda x: isinstance(x, list),
        'map': lambda proc, *x: [proc(y) for y in x[0]],
        'square': lambda x: x ** 2
    })
    tokens = lex(readfile('mini.mini'))
    main_eval(global_env, parse(tokens))
    # while True:
    #     i = input('->')
    #     main_eval(global_env, parse(lex(i)))

if __name__ == "__main__":
    main()
