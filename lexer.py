from operator import add
from string import ascii_letters
from string import digits
from pprint import pprint as pp


def lex(filename):
    with open(filename) as f:
        return (t for t in f.read().split() if t)

def parse(lib, scope, tokens):
    t = next(tokens)

    while t is not None:

        if t == ')':
            return None

        elif t == '(':
            func = next(tokens)
            args = []
            val = parse(lib, scope, tokens)
            while val is not None:
                args.append(val)
                val = parse(lib, scope, tokens)

            if func == 'define':
                scope[args[0]] = args[1]
            else:
                val = lib[func](*args)
                if val is not None:
                    return val

        elif t == 'define':
            name = next(tokens)
            print("name: ", name)
            val = parse(lib, scope, tokens)
            scope[name] = val

        elif t == '"':
            t = next(tokens)
            string = ''
            while t != '"':
                string += t + ' '
                t = next(tokens)
            if string[-1] == ' ':
                string = string[:-1]
            return string

        elif t in scope:
            return scope[t]

        elif all(c in digits for c in t):
            return int(t)

        else:
            return t

        try:
            t = next(tokens)
        except StopIteration:
            return


def main():
    lib = {
        'println': print,
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x // y,
        '%': lambda x, y: x % y,
    }
    tokens = lex('mini.mini')
    parse(lib, {}, tokens)


if __name__ == "__main__":
    main()
