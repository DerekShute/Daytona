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
one:
  - kw one
two:
  - kw one
  - kw two
calls-another:
  - one
calls-print:
  - print something
no-keyword:
  - kw something
  - no-such-keyword
"""

ARGS = []
CALLS = 0


@primitive('kw')
def do_keyword(args, context):
    '''Keyword to track calls and arguments'''
    assert context
    global CALLS
    print(f'test_run: {args}')
    ARGS.append(args)
    CALLS += 1


class TestExecution(unittest.TestCase):
    '''Testing execution flow and basic stuff'''

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

    @parameterized.expand([('one', [('one',)]),
                           ('two', [('one',), ('two',)]),
                           ('calls-another', [('one',)]),
                           ])
    def test_simple_runs(self, keyword, call_list):
        '''Simple executions we expect to work'''
        execute_script(keyword)
        self.assertEqual(ARGS, call_list)

    @parameterized.expand([('no-such-keyword', 'No such keyword "no-such-keyword"'),
                           ('no-keyword', 'no-keyword@2: No such keyword "no-such-keyword"'),
                           ])
    def test_run_excepts(self, keyword, exception_str):
        '''Executions we expect to raise ScriptError'''
        excepted = False
        try:
            execute_script(keyword)
        except ScriptError as ex:
            self.assertEqual(str(ex), exception_str)
            excepted = True
        self.assertTrue(excepted)

    def test_calls_print(self):
        '''Uses the print primitive, just for coverage excellence'''
        execute_script('calls-print')

# EOF
