"""
    Unit Test : Expressions
"""

import yaml
import unittest
from parameterized import parameterized
from daytona import primitive, register_keywords, execute_script, ScriptError


body = """
one:
  - ex ( ex one )
chains-return:
  - ex ( ex2 one )
unclosed:
  - ( ex one
"""

ARGS = []
CALLS = 0


@primitive('ex2')
def do_ex2_keyword(args, context):
    print(f'test_exp2: {args}')
    return context, args[0]


@primitive('ex')
def do_ex_keyword(args, context):
    global CALLS
    print(f'test_expressions: {args}')
    ARGS.append(args)
    CALLS += 1
    return context, None


class TestExecution(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        assert cls
        body_dict = yaml.safe_load(body)
        register_keywords(body_dict)

    def setUp(self):
        assert self
        global ARGS, CALLS
        ARGS = []
        CALLS = 0

    @parameterized.expand([('one', [('one',), ('None',)]),
                           ('chains-return', [('one',)]),
                           ])
    def test_simple(self, keyword, call_list):
        execute_script(keyword)
        self.assertEqual(ARGS, call_list)

    @parameterized.expand([('unclosed', 'unclosed@1: Unclosed expression'),
                           ])
    def test_excepts(self, keyword, exception_str):
        excepted = False
        try:
            execute_script(keyword)
        except ScriptError as ex:
            self.assertEqual(str(ex), exception_str)
            excepted = True
        self.assertTrue(excepted)


# EOF
