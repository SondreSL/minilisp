from operator import add
from string import ascii_letters
from string import digits
from pprint import pprint as pp


def lex(filename):
    with open(filename) as f:
        return list(map(tokenize, [t for t in f.read().split() if t != '' or ';' not in t]))


def tokenize(s):
    if s[0] in '()"':
        return ('symbol', s)
    if s[0] in ascii_letters and all(c in ascii_letters + digits + '_' for c in s):
        return ('name', s)
    elif s[0] in '+-*/%':
        return ('operator', s)
    elif all(c in digits for c in s):
        return ('number', int(s))
    else:
        raise ValueError("Not a valid token! -> " + s)


def parse(scope, tokens):
    pass


def mini_eval(tokens):
    pass


def main():
    scope = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x // y,
        '%': lambda x, y: x % y,
    }
    tokens = lex('mini.mini')
    parse(scope, tokens)
    pp(tokens)


if __name__ == "__main__":
    main()
