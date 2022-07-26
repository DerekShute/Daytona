"""
    Unit Test : Base run
"""

import yaml
import unittest
from parameterized import parameterized
from daytona import primitive, register_keywords, execute_script, ScriptError, register_variables

variables = {
    'var1': 'oneVar',
    'var2': 2
    }

body = """
increment:
  - math ( ++ 1 )
  - math ( ++ $var2 )
decrement:
  - math ( -- 3 )
  - math ( -- $var2 )
adds:
  - math ( + 1 2 3 ( + 4 5 6 ) 7 8 ( ++ 9 ) $var2 )
dec-faults:
  - ( -- )
inc-faults:
  - ( ++ )
add-noargs:
  - ( + )
invalid-arg-inc:
  - ( ++ frotz )
invalid-arg-dec:
  - ( -- frotz )
invalid-add-arg:
  - ( + 1 frotz )
"""

ARGS = []
CALLS = 0


@primitive('math')
def do_math(args, **kwargs):
    global ARGS, CALLS
    print(f'test_math: {args}')
    ARGS.append(args)
    CALLS += 1


class TestMath(unittest.TestCase):

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

    @parameterized.expand([('increment', [('2',), ('3',)]),
                           ('decrement', [('2',), ('1',)]),
                           ('adds', [('48',)]),
                           ])
    def test_simple(self, keyword, call_list):
        execute_script(keyword)
        self.assertEqual(ARGS, call_list)

    @parameterized.expand([('dec-faults', 'dec-faults@1: "--" keyword is unary'),
                           ('inc-faults', 'inc-faults@1: "++" keyword is unary'),
                           ('invalid-arg-inc', 'invalid-arg-inc@1: "++" keyword accepts numbers only'),
                           ('invalid-arg-dec', 'invalid-arg-dec@1: "--" keyword accepts numbers only'),
                           ('add-noargs', 'add-noargs@1: "+" keyword requires arguments'),
                           ('invalid-add-arg', 'invalid-add-arg@1: "+" keyword accepts numbers only'),
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
