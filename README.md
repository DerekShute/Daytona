# Daytona

Dumb scripting language written in Python based on Python which the world never asked for and does not need

## Use

* See 'run_something.py' for an example

* Register keywords, variables as dictionaries

* Register 'primitive' (Python-implemented) keywords using the 'primitive' decorator
  * Probably not a good idea but I was learning how to do these things

* I've been loading from YAML file or translating from a YAML-formatted string

## Language Schema (am I using that word correctly?)

BODY := STATEMENT [[ + STATEMENT ]]

STATEMENT := IF_STATEMENT

STATEMENT := KEYWORD_STATEMENT

KEYWORD_STATEMENT := KEYWORD [[ + EXPRESSION ]]

IF_STATEMENT := 'if' + EXPRESSION + BODY [[ + 'elif' + EXPRESSION + BODY ]] [ + 'else' + BODY ] + 'end'

EXPRESSION := '(' + EXPRESSION + ')'

EXPRESSION := KEYWORD_STATEMENT

EXPRESSION := string

EXPRESSION := integer

( I think I've defined that correctly.  Expressions use prefix notation and operators are just keywords.  Keywords return values that are picked up for the evaluation of the expression)

KEYWORD := string

## Variables

* Shell script format: $string

* Arguments to keyword: $number starting from 0 ($0 is not the original keyword, note)

* '$?' indicates last return value

## Implemented Keywords

* "if/elif/else/end"
  * Where 'expression' is zero-false, nonzero-true

```
if <expression>
    statement
    statement
elif <expression>
    statement
    statement
else
    statement
    statement
end
```

* A few operators
  * '+'
  * '++' : increment
  * '--' : decrement


* 'set'
  * Set variable to value

## To Do

* Loops
  * with 'break' keyword

```
while <expression>
   statement
   statement
   statement
end
```

* 'return' keyword
  * Sets return value for statement block and ends statement block


* Exceptions
  * Where the variable gets set with the string value

```
try <variable>
   statement
   raise <string>
end
```
