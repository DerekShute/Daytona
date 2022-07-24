"""
    Unit Test : Base run
"""

import yaml
import unittest
from parameterized import parameterized
from daytona import primitive, register_keywords, execute_script, register_primitive, ScriptError, register_variables

variables = {
    'var1': 'oneVar',
    'var2': 2
    }

body = """
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
def do_output(args, **kwargs):
    global ARGS, CALLS
    print(f'test_run: {args}')
    ARGS.append(args)
    CALLS += 1


class TestExecution(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        assert cls
        body_dict = yaml.safe_load(body)
        register_keywords(body_dict)
        register_variables(variables)

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
        execute_script(keyword)
        self.assertEqual(ARGS, call_list)

    @parameterized.expand([('no-such-keyword', 'No such keyword "no-such-keyword"'),
                           ('no-keyword', 'no-keyword@2: No such keyword "no-such-keyword"'),
                           ])
    def test_run_excepts(self, keyword, exception_str):
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
