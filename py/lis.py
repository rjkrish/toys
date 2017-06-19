# This is a version fo lis.py at http://norvig.com/lispy.html
# Trace output has been added to study the workings of the program

import math
import operator as op

Symbol = str

List = list

Number = (int, float)

def Atom(token):
    "Numbers become numbers; every other token is a symbol"
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args): 
        return eval(self.body, Env(self.parms, args, self.env))

class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer
    def find(self, var):
        "Find the innermost Env where var appears."
        return self if (var in self) else self.outer.find(var)

def standard_env():
    "An environment with some Scheme standard procedures."
    env = Env()
    env.update(vars(math)) # sin, cos, sqrt, pi, ...
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.div, 
        '^': op.pow, '%': op.mod, '|': op.xor, 
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, 
        '=': op.eq, 
        'abs':     abs,
        'append':  op.add,  
        'apply':   apply,
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: list(x), 
        'list?':   lambda x: isinstance(x,list), 
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),   
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

global_env = standard_env()

def tokenize(chars):
    "Convert a string of characters into a list of tokens."
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(program):
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def read_from_tokens(tokens, depth=0):
    "Read an expression from a sequence of tokens."
    if depth == 0: print "--- READ --- "
    print_call( tokens, depth )
    if len(tokens) == 0:
        raise SyntaxError('empty sequence')
    token = tokens.pop(0);
    if '(' == token:
        L = []
        while tokens[0] != ')':
            t = read_from_tokens(tokens, depth + 1)
            L.append(t)
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return Atom(token)
 
def eval(x, env=global_env, depth=0):
    "Evaluate an expression in an environment."
    if depth == 0: print "--- EVAL --- "
    print_call(x, depth)
    if isinstance(x, Symbol):       # variable reference
        return env.find(x)[x]
    elif not isinstance(x, List):   # constant literal
        return x
    elif x[0] == 'quote':           # quotation
        (_, exp) = x
        return exp
    elif x[0] == 'if':              # conditional
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env, depth + 1) else alt)
        return eval(exp, env, depth + 1)
    elif x[0] == 'define':          # definition
        (_, var, exp) = x
        env[var] = eval(exp, env, depth + 1)
    elif x[0] == 'set!':            # assignment
        (_, var, exp) = x
        env.find(var)[var] = eval(exp, env, depth + 1)
    elif x[0] == 'lambda':          # procedure call
        (_, parms, body) = x
        return Procedure(parms, body, env)
    else:                           # procedure call
        proc = eval(x[0], env, depth +1)
        args = [eval(arg, env, depth + 1) for arg in x[1:]]
        return proc(*args)
    

def repl(prompt='lis.py> '):
    "A prompt-read-eval-print loop."
    while True:
        val = eval(parse(raw_input(prompt)))
        if val is not None: 
            print(schemestr(val))

def schemestr(exp):
    "Convert a Python object back into a Scheme-readable string."
    if isinstance(exp, List):
        return '(' + ' '.join(map(schemestr, exp)) + ')' 
    else:
        return str(exp)

def print_call(x, i=0):
    print str(i) + ": ",
    print '    ' * i,
    print x

    
