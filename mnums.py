import string
from lark import Lark, Token, Transformer, v_args
import inspect

GRAMMAR_PROTO = """start: expression
?expression: MBR | {productions}
_monoarg{{x}}: x "(" expression ")"
_biarg{{x}}: x "(" expression "," expression ")"
MBR: {mbr} | NUMBER
%import common.NUMBER
%ignore " "
"""
MBR_PROTO = 'abc'

def get_transformer_productions(transformer):
    for method_name, method in inspect.getmembers(transformer, inspect.ismethod):
        if "_" not in method_name and method_name != 'transform':
            param_len = len(inspect.signature(method).parameters)
            if param_len == 1:
                yield method_name, True
            elif param_len >= 2:
                yield method_name, False


def generate_productions_from(obj):
    return " | ".join((f'_monoarg{{"{name}"i}}' if is_mono else f'_biarg{{"{name}"i}}')+f' -> {name}' for name, is_mono in get_transformer_productions(obj))

def mbr_from_alphabet(alphabet):
    return '("' + '" | "'.join(alphabet) + '")+'

class MBRParser():
    def __init__(self, alphabet='abc', transformer=None):
        self.transformer = transformer
        self.set_alphabet(alphabet)
        return

    def parse(self, input_string):
        parse_tree = self.parser.parse(input_string)
        return parse_tree.children[0]


    def set_alphabet(self, alphabet):
        self.transformer.set_alphabet(alphabet)
        productions = generate_productions_from(self.transformer)
        mbr = mbr_from_alphabet(alphabet)
        grammar = GRAMMAR_PROTO.format(productions=productions, mbr=mbr)
        print(grammar)
        self.parser = Lark(grammar, parser='lalr', transformer=self.transformer)


@v_args(inline=True)
class MBRTransformer(Transformer):
    def set_alphabet(self, alphabet):
        self.alphabet = alphabet
        self.val = {t: i for i, t in enumerate(alphabet)}
        return

    def _dual(self, x):
        assert len(x) == 1
        return self.alphabet[-(self.val[x]+1)]

    def delta(self, x_char, y_char):
        assert len(x_char) == 1 and len(y_char) == 1
        return abs(self.val[x_char] - self.val[y_char])

    def defect(self, x):
        return self.val[self.right(x)] - self.val[self.left(x)]

    def len(self, x):
        return sum((-1)**(i+1) * self.delta(x[i], x[i+1]) for i in range(len(x) - 1))

    def lens(self, x):
        return (self.len(x) - self.defect(x))/2

    def lenp(self, x):
        return (self.len(x) - self.defect(x))/2

    def alpha(self):
        return self.alphabet[0]

    def omega(self):
        return self.alphabet[-1]

    def left(self, x):
        return x[0]

    def right(self, x):
        return x[-1]

    def leftd(self, x):
        return self._dual(self.left(x))

    def rightd(self, x):
        return self._dual(self.right(x))

    def zip(self, x):
        done = False
        while not done:
            if len(x)<4:
                return x
            if len(x)==4:
                if self.delta(x[0],x[3]) == (self.delta(x[0],x[1]) - self.delta(x[1],x[2]) + self.delta(x[2],x[3])):
                    return x[0]+x[3]
                else:
                    return x
            i = 0
            while i < len(x):
                if (i+3) < len(x):
                  ad = self.delta(x[i], x[i+3])
                  sve = self.delta(x[i],x[i+1]) - self.delta(x[i+1],x[i+2])+self.delta(x[i+2],x[i+3])
                else:
                    return x
                if ad == sve:
                    ispred = x[0:i+1]
                    iza = x[i+3:]
                    x = ispred + iza
                    i += 1
                    break
                else:
                    i += 1
                    if i >= len(x):
                        done = True
                        break
        return x


    def d(self, x):
        return "".join(map(self._dual, x))

    def q(self, x):
        return self.left(x) + self.right(x)

    def e(self, x):
        return x[::-1]

    def i(self, x):
        return self.left(x)+x+self.right(x)

    def k(self, x):
        return self.leftd(x) + x + self.rightd(x)

    def f(self, x):
        return self.d(self.e(x))

    def g(self, x):
        return self.right(x) + x + self.left(x)

    def h(self, x):
        return self.rightd(x) + x + self.leftd(x)

    def io(self, x):
        return self.e(self.g(x))

    def js(self, x):
        return self.omega() + self.alpha() + x + self.omega() + self.alpha()

    def jp(self, x):
        return self.alpha() + self.omega() + x + self.alpha() + self.omega()

    def qs(self, x):
        self.left(x) + min(self.left(x), self.right(x)) + max(self.left(x), self.right(x)) + self.right(x)

    def qp(self, x):
        self.left(x) + max(self.left(x), self.right(x)) + min(self.left(x), self.right(x)) + self.right(x)

    #def is(self, x):
    #    if self.left(x)<=self.right(x):
    #        return self.left(x)+x+self.right(x)+self.left(x)*2 + self.right(x)*2
    #    else:
    #        return self.left(x)+self.right(x)*2+x+self.right(x)

    def ip(self, x):
        if self.left(x)<=self.right(x):
            return self.left(x)+self.right(x)*2+x+self.right(x)
        else:
            return self.left(x)+x+self.right(x)+self.left(x)*2+self.right(x)*2

    def es(self, x):
        return self.g(self.i(x)) if self.left(x) <= self.right(x) else self.i(self.g(x))

    def ep(self, x):
        return self.i(self.g(x)) if self.left(x) <= self.right(x) else self.g(self.i(x)) 

    def ds(self, x):
        return self.d(self.e(self.es(x)))

    def dp(self, x):
        return self.d(self.e(self.ep(x)))

    def ks(self, x):
        return self.omega() + x + self.omega()

    def kp(self, x):
        return self.alpha() + x + self.alpha()

    def ps(self, x, y):
        return max(self.left(x), self.left(y))*2 + x + min(self.right(x), self.left(y)) + max(self.right(x), self.left(y)) + y + min(self.right(x), self.right(y))*2

    def ss(self, x, y):
        return min(self.left(x), self.left(y))*2 + x + max(self.right(x), self.left(y)) + min(self.right(x), self.left(y)) + y + max(self.right(x), self.right(y))*2

    def po(self, x, y):
        return self.ps(x, self.ip(y)) 

    def pm(self, x, n, rez=''):
        print('x', x), print('n', n)
        n = int(n)
        rez = x if rez == "" else rez
        if n in [1, -1]:
            return rez
        elif n < 0:
            rez = self.ps(rez, self.ip(x))
            return self.pm(x, n+1, rez)
        else:
            rez = self.ps(rez, x)
            return self.pm(x, n-1, rez)

    #def sm(self, x, n, rez=''):
    #    n = int(n)
    #    rez = x if rez == '' else rez
    #    if n in [-1, 1]:
    #        return rez
    #    elif n < 0:
    #        rez = self.ss(rez, self.is(x))
    #        return self.sm(n+1, x, rez)
    #    else:
    #        rez = self.ss(rez, x)
    #        return self.sm(n-1, x, rez)

    def si(self, x, y):
        return self.ss(self.k(x), y)

    def pi(self, x, y):
        return self.ps(self.k(x), y)

    def se(self, x, y):
        return self.ps(self.si(x, y), self.si(y, x))

    def pe(self, x, y):
        return self.ss(self.pi(x, y), self.pi(y, x))
