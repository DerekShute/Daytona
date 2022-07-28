"""
    Unit Test : Base run
"""

import unittest
import yaml
from parameterized import parameterized
from daytona import primitive, register_keywords, execute_script, ScriptError, register_variables

VARIABLES = {
    'var1': 'oneVar',
    'var2': 2
    }

BODY = """
one-arg:
  - var $0
two-args:
  - var $0 $1
variable:
  - var $var1
novariable:
  - var $nosuch
set-noarg:
  - set
set-works:
  - set FROTZ foobar
  - var $FROTZ
no-retval:
  - var $?
rets-retval:
  - voo
  - var $?
"""

ARGS = []
CALLS = 0


@primitive('voo')
def do_voo(args, context):
    '''boring keyword that returns a value'''
    assert context
    print(f'voo: {args}')
    return '1'


@primitive('var')
def do_output(args, context):
    '''check of expected argument value'''
    assert context
    global CALLS
    print(f'test_variables: {args}')
    ARGS.append(args)
    CALLS += 1


class TestVariables(unittest.TestCase):
    '''Test variable evaluation'''

    @classmethod
    def setUpClass(cls):
        assert cls
        body_dict = yaml.safe_load(BODY)
        register_keywords(body_dict)
        register_variables(VARIABLES)

    def setUp(self):
        assert self
        global ARGS, CALLS
        ARGS = []
        CALLS = 0

    @parameterized.expand([('variable', 'None', [('oneVar',)]),
                           ('set-works', 'None', [('foobar',)]),
                           ('no-retval', 'None', [('None', )]),
                           ('rets-retval', 'None', [('1', )]),
                           ])
    def test_simple_noargs(self, keyword, retval, call_list):
        '''Simple things that work without arguments'''
        returned = execute_script(keyword)
        self.assertEqual(retval, returned)
        self.assertEqual(ARGS, call_list)

    @parameterized.expand([('one-arg', ('three',), [('three',)]),
                           ])
    def test_simple_args(self, keyword, args, call_list):
        '''Simple things that work with arguments'''
        execute_script(keyword, *args)
        self.assertEqual(ARGS, call_list)

    @parameterized.expand([('one-arg', 'one-arg@1: No such arg 0'),
                           ('novariable', 'novariable@1: No variable $nosuch'),
                           ('set-noarg', 'set-noarg@1: "set" keyword requires two arguments'),
                           ])
    def test_run_excepts(self, keyword, exception_str):
        '''Things we expect to throw ScriptError'''
        excepted = False
        try:
            execute_script(keyword)
        except ScriptError as ex:
            self.assertEqual(str(ex), exception_str)
            excepted = True
        self.assertTrue(excepted)

    @parameterized.expand([('two-args', ('one',), 'two-args@1: No such arg 1'),
                           ])
    def test_run_excepts_args(self, keyword, args, exception_str):
        '''Things we expect to throw ScriptError, with arguments'''
        excepted = False
        try:
            execute_script(keyword, *args)
        except ScriptError as ex:
            self.assertEqual(str(ex), exception_str)
            excepted = True
        self.assertTrue(excepted)

# EOF
