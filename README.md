# Daytona

Dumb scripting language written in Python based on Python which the world never asked for and does not need

## Use

* See 'run_something.py' for an example

* Register keywords, variables as dictionaries

* Register 'primitive' (Python-implemented) keywords using the 'primitive' decorator
  * Probably not a good idea but I was learning how to do these things

* I've been loading from YAML file or translating from a YAML-formatted string

* See the 'Containers' section for building this beast

## Language Grammar

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

* You could probably do '$thing.field' as a convention

## Implemented Keywords

* "if/elif/else/end"
  * Where 'expression' is zero-false, nonzero-true
  * Indentation is a convention but keywords appear on their own line
  * Nesting is allowed but don't put the keywords in an expression that will almost certainly not work
    * TODO: test for this

```
if <expression>
    statement
    statement
    if <expression>
        ...
    end
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
<variable holds string and no change otherwise>
```


* String literals
  * "string" keyword to create a string return value


* Example 'run_something' script and give that a better name


## Containers

* "make image" creates the local daytona-builder image with a "make" entrypoint
* the d.sh script invokes it, passing command line arguments along
  * So, "./d.sh test" invokes the "test" makefile target
* Yes I know this is crude but I'm still figuring out the best approach
