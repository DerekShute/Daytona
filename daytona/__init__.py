'''
Daytona import module
'''

from dataclasses import dataclass, field
from functools import wraps
from typing import Dict, Any, List


KEYWORDS: Dict[str, Any] = {}
VARIABLES: Dict[str, Any] = {}
CONTROL_KEYWORDS = ('if', 'else', 'elif', 'end')  # There must be a better way


# ===== ScriptError Exception =====

class ScriptError(Exception):
    '''Generalized grammar error'''
    def __init__(self, context=None, msg=None):
        self.context = context
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        if self.context:
            return f'{self.context.parent_keyword}@{self.context.line_no}: {self.msg}'
        return f'{self.msg}'


# ===== Context =====

class InterpreterState:
    '''Bucket type for interpreter state machine'''
    STATE_NONE = 0
    STATE_IF_RUN = 1
    STATE_IF_PASS = 2
    STATE_IF_DONE = 3
    STATE_ELSE = 4


@dataclass
class Context:
    '''Execution context w/r/t control sequences'''
    skipping: bool = False
    parent_keyword: str = ''  # The keyword this is executing from
    line_no: int = 1
    state = InterpreterState.STATE_NONE
    retval: str = 'None'


@dataclass
class Expression:
    parent: Any = None
    words: List = field(default_factory=list)
    depth: int = 0


# ===== Service Routines =====

def execute_keyword(context, keyword, *args):
    '''Execute a keyword, breaking it down to a statement body'''
    kw_val = KEYWORDS.get(keyword)
    if not kw_val:
        raise ScriptError(context, f'No such keyword "{keyword}"')
    # print(f'{context} : "{keyword}" with {args}')
    if callable(kw_val):
        ret = kw_val(args, context=context)  # TODO: reverse this
    else:
        ret = execute_statements(keyword, kw_val, args)
    return ret if ret else 'None'


def evaluate_expression(context, words):
    '''evaluate subexpressions and apply arguments to operator'''
    expr = Expression()
    for word in words:
        if word == '(':  # Start expression
            nexpr = Expression(parent=expr)
            nexpr.parent = expr
            nexpr.depth = expr.depth + 1
            expr = nexpr
        elif word == ')':  # End expression
            context.retval = execute_keyword(context, expr.words[0], *expr.words[1:])
            expr = expr.parent
            expr.words.append(context.retval)
        else:  # Something in the middle of the expression
            expr.words.append(word)
    context.retval = execute_keyword(context, expr.words[0], *expr.words[1:])
    if expr.depth > 0:
        raise ScriptError(context, 'Unclosed expression')
    return context.retval


def parse_line(context, line, args):
    '''Parse a line of text and resolve variables in it'''
    words = line.split()
    if context.skipping and words[0] not in CONTROL_KEYWORDS:
        return None
    for index, word in enumerate(words):  # Note includes keyword
        if word == '$?':   # Return value of last expression
            words[index] = context.retval
        elif word[0] == '$':
            if word[1:].isdigit():
                argno = int(word[1:])
                if not args or argno >= len(args):
                    raise ScriptError(context, f'No such arg {argno}')
                # print(f'  {word} ==> argument {argno} {args[argno]}')
                words[index] = args[argno]
            elif VARIABLES.get(word[1:]):
                # print(f'  {word} ==> {VARIABLES[word[1:]]}')
                words[index] = VARIABLES[word[1:]]
            else:
                raise ScriptError(context, f'No variable {word}')
    return words


def execute_statements(keyword, body, args=None):
    '''Execute a body of statements (a list of strings)'''
    context = Context(parent_keyword=keyword)
    for line in body:
        # print(f'{context}: Executing line "{line}" args {args}')
        words = parse_line(context, line, args)
        if words:
            context.retval = evaluate_expression(context, words)
        context.line_no += 1
    if context.state != InterpreterState.STATE_NONE:
        context.line_no = len(body)  # more intuitive to point to last line
        raise ScriptError(context, 'Keyword ended with unterminated if statement')
    return context.retval


#
# ===== API Routines =====
#

def register_primitive(name, func):
    KEYWORDS[name] = func


def primitive(name):
    '''Keyword implemented in Python directly'''
    def decorate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)  # NOTE: unit test coverage misses this line it is a mystery
        register_primitive(name, function)
        return wrapper
    return decorate


def register_keywords(keyword_dict):
    # Note will squash existing keys
    KEYWORDS.update(keyword_dict)


def register_variables(variables_dict):
    # Note will squash existing keys
    VARIABLES.update(variables_dict)


def execute_script(start_keyword, *args):
    '''Start executing at the following keyword (generally 'main')'''
    if not KEYWORDS.get(start_keyword):  # More intuitive error output
        raise ScriptError(None, f'No such keyword "{start_keyword}"')
    context = Context(parent_keyword=start_keyword)
    # print(f'{context} execute_script {start_keyword} with {args}')
    return execute_keyword(context, start_keyword, *args)


# ===== KEYWORDS =========

# ===== Control Flow =====

@primitive('if')
def do_if_keyword(args, context=None):
    '''If keyword'''
    if not args or len(args) != 1:
        raise ScriptError(context, '"if" keyword requires one argument')
    print('IF')
    if args[0] == '0':  # TODO Hey so much more to do here
        print('IF skip')
        context.state = InterpreterState.STATE_IF_PASS
        context.skipping = True
    else:
        print('IF run')
        context.state = InterpreterState.STATE_IF_RUN
        context.skipping = False


@primitive('elif')
def do_elif_keyword(args, context=None):
    '''elif keyword'''
    if not args or len(args) != 1:
        raise ScriptError(context, '"elif" keyword requires one argument')
    if context.state == InterpreterState.STATE_IF_RUN:
        context.state = InterpreterState.STATE_IF_DONE
        context.skipping = True
    elif context.state == InterpreterState.STATE_IF_PASS:
        if args[0] != '0':  # TODO Hey so muc more to do here
            context.state = InterpreterState.STATE_IF_RUN
            context.skipping = False
    else:
        raise ScriptError(context, '"elif" keyword in wrong state')


@primitive('else')
def do_else_keyword(args, context=None):
    '''Else keyword'''
    if args and len(args) > 0:
        raise ScriptError(context, '"else" keyword has arguments')
    if context.state == InterpreterState.STATE_ELSE:
        raise ScriptError(context, '"else" keyword is extraneous')
    if context.state == InterpreterState.STATE_IF_PASS:
        context.state = InterpreterState.STATE_ELSE
        context.skipping = False
    if context.state in (InterpreterState.STATE_IF_RUN, InterpreterState.STATE_IF_DONE):
        context.state = InterpreterState.STATE_ELSE
        context.skipping = True


@primitive('end')
def do_end_keyword(args, context=None):
    '''End of control block'''
    safe_end = (InterpreterState.STATE_IF_RUN,
                InterpreterState.STATE_IF_PASS,
                InterpreterState.STATE_ELSE,
                InterpreterState.STATE_IF_DONE)
    if args and len(args) > 0:
        raise ScriptError(context, '"end" keyword has arguments')
    if context.state not in safe_end:
        raise ScriptError(context, '"end" keyword not within "if" statement')
    context.state = InterpreterState.STATE_NONE
    context.skipping = False


# ===== Base keywords =====

@primitive('print')
def do_print(args, context):
    assert context
    print(' '.join([str(i) for i in args]))


@primitive('set')
def do_set(args, context):
    '''Set variable keyword'''
    assert context
    if not args or len(args) != 2:
        raise ScriptError(context, '"set" keyword requires two arguments')
    VARIABLES[args[0]] = str(args[1])


# TODO: sleep, exit, return

# ===== Arithmetic/logic keywords =====

# TODO: decorator such that it ensures arg count and type

@primitive('++')
def do_increment(args, context):
    '''Unary increment'''
    assert context
    if not args or len(args) != 1:
        raise ScriptError(context, '"++" keyword is unary')
    val = None
    try:
        val = int(args[0])
    except ValueError as ex:
        raise ScriptError(context, '"++" keyword accepts numbers only') from ex
    return str(val + 1)


@primitive('--')
def do_decrement(args, context):
    '''Unary decrement'''
    assert context
    if not args or len(args) != 1:
        raise ScriptError(context, '"--" keyword is unary')
    try:
        val = int(args[0])
    except ValueError as ex:
        raise ScriptError(context, '"--" keyword accepts numbers only') from ex
    return str(val - 1)


@primitive('+')
def do_add(args, context):
    '''Addition'''
    assert context
    if not args or len(args) == 0:
        raise ScriptError(context, '"+" keyword requires arguments')
    sum_val = 0
    for arg in args:
        try:
            sum_val += int(arg)
        except ValueError as ex:
            raise ScriptError(context, '"+" keyword accepts numbers only') from ex
    print(f'sum is {sum_val}')
    return str(sum_val)

# TODO: subtract, multiply, divide, boolean logic

# EOF
