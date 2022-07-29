"""
    Unit Test : Control Flow
"""

import yaml
import unittest
from parameterized import parameterized
from daytona import primitive, register_keywords, execute_script, ScriptError

body = """
does_nothing:
  - cf True
if-false:
  - if 0
  -     cf Does not get here
  - end
if-true:
  - cf True
  - if 1
  -     cf True
  - end
  - cf True
if-calls:
  - if 1
  -     cf True
  -     does_nothing
  -     cf True
  - end
if-true-else:
  - if 1
  -     cf True
  - else
  -     cf Does not get here
  - end
if-false-else:
  - if 0
  -     cf Does not get here
  - else
  -     cf True
  - end
if-true-elif-true:
  - if 1
  -     cf True
  - elif 1
  -     cf Does not get here
  - end
if-false-elif-true:
  - if 0
  -     cf Does not get here
  - elif 1
  -     cf True
  - end
if-false-elif-false-else:
  - if 0
  -     cf Does not get here
  - elif 0
  -     cf Does not get here
  - else
  -     cf True
  - end
if-noarg:
  - if
incomplete-if:
  - if 1
  -     cf Does get here
incomplete-elif:
  - if 1
  -     cf Does get here
  - elif 0
incomplete-else:
  - if 1
  -     cf Does get here
  - else
elif-alone:
  - elif 0
elif-after-else:
  - if 0
  -     cf Does not get here
  - else
  -     cf True
  - elif 0
elif-noarg:
  - if 0
  -     cf Does not get here
  - elif
else-arg:
  - if 0
  -     cf Does not get here
  - else 0
end-alone:
  - end
end-arg:
  - if 0
  -     cf Does not get here
  - end 0
if-else-else:
  - if 0
  -     cf Does not get here
  - else
  -     cf True
  - else
  -     cf Does not get here
  - end
if-nested-false:
  - if 0
  -     if 1
  -         cf Does not get here
  -     elif 0
  -         cf Does not get here
  -     else
  -         cf Does not get here
  -     end
  -     cf Does not get here
  - end
if-nested-true-1:
  - if 1
  -     if 1
  -         cf True
  -     elif 0
  -         cf Does not get here
  -     else
  -         cf Does not get here
  -     end
  - end
  - cf True
if-nested-true-2:
  - if 1
  -     if 0
  -         cf Does not get here
  -     elif 1
  -         cf True
  -     else
  -         cf Does not get here
  -     end
  - end
  - cf True
if-nested-true-3:
  - if 1
  -     if 0
  -         cf Does not get here
  -     elif 1
  -         cf Does not get here
  -     else
  -         cf True
  -     end
  - end
  - cf True
if-nested2-true:
  - if 1
  -     if 1
  -         if 1
  -             cf True
  -         else
  -             cf Does not get here
  -         end
  -     elif 1
  -         cf Does not get here
  -     end
  - end
  - cf True
"""

ARGS = []
CALLS = 0


@primitive('cf')
def do_output(args, context):
    global CALLS
    print(f'test_control_flow: {args} @ {context}')
    ARGS.append(args)
    CALLS += 1
    return context, None


class TestControl(unittest.TestCase):

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

    @parameterized.expand([('if-false', 0),
                           ('if-true', 3),
                           ('if-calls', 3),
                           ('if-true-else', 1),
                           ('if-false-else', 1),
                           ('if-true-elif-true', 1),
                           ('if-false-elif-true', 1),
                           ('if-false-elif-false-else', 1),
                           ('if-nested-false', 0),
                           ('if-nested-true-1', 2),
                           ('if-nested-true-2', 2),
                           ('if-nested-true-3', 2),
                           ('if-nested2-true', 2),
                           ])
    def test_control_taken(self, keyword, call_count):
        execute_script(keyword)
        self.assertEqual(CALLS, call_count)
        if call_count == 1:
            self.assertEqual(ARGS, [('True',)])

    @parameterized.expand([('if-noarg', 'if-noarg@1: "if" keyword requires one argument'),
                           ('incomplete-if', 'incomplete-if@2: Keyword ended with unterminated if statement'),
                           ('incomplete-elif', 'incomplete-elif@3: Keyword ended with unterminated if statement'),
                           ('incomplete-else', 'incomplete-else@3: Keyword ended with unterminated if statement'),
                           ('elif-alone', 'elif-alone@1: "elif" keyword in wrong state'),
                           ('elif-after-else', 'elif-after-else@5: "elif" keyword in wrong state'),
                           ('elif-noarg', 'elif-noarg@3: "elif" keyword requires one argument'),
                           ('else-arg', 'else-arg@3: "else" keyword has arguments'),
                           ('end-alone', 'end-alone@1: "end" keyword not within "if" statement'),
                           ('end-arg', 'end-arg@3: "end" keyword has arguments'),
                           ('if-else-else', 'if-else-else@5: "else" keyword is extraneous'),
                           ])
    def test_control_excepts(self, keyword, exception_str):
        excepted = False
        try:
            execute_script(keyword)
        except ScriptError as ex:
            self.assertEqual(str(ex), exception_str)
            excepted = True
        self.assertTrue(excepted)

# EOF
