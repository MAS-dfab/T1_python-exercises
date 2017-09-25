'''
. . . . . . . . . . . . . . . . . . . . .
.                                       .
.    <<      ><      ><       >< <<     .
.    < ><   ><<     ><<<    ><    ><<   .
.    << >< > ><    ><  ><     ><        .
.    <<  ><  ><   ><<<<<><      ><      .
.    <<      >< ><<     ><< ><    ><<   .
.    <<      ><><<       ><<  >< <<     .
.                                       .
.             DFAB 2016/17              .
. . . . . . . . . . . . . . . . . . . . .

Created on 14.09.2016

@author: jennyd
'''


#===============================================================================
# Python Basics
#
# contents
#
# strings and comments, basic syntax
# variables and basic types ( int, float, string, etc.)
# operators (+ , -, /, *, //, **, %, etc.)
# boolean expressions (True, False, ==, !=)
# conditionals ( if, elif, else, while)
# lists ( tuples, dictionaries)
# loops (for, while, nested loops, etc.)
# definitions, functions (functions, nested functions, recursive functions)
# classes, objects (global and local variables)
#
#===============================================================================

#===============================================================================
#
# strings and comments, basic syntax
#
#===============================================================================

# this is a commment

# this is a multiline
# comment

# this is a multiline
# multi-paragraph comment
#
# paragraphs are separated
# by one single #


"This is a string"
'This is also a string'

"This is a string with 'another string' inside"

"""This is a multiline string.

It is usually used as documentation string a.k.a. docstring.
"""

#==============================================================================
#
# variables and basic types ( int, float, string, etc.)
#
#==============================================================================

# print function
print "Hello World."

# variables
# strings

a = "Hello World"
print a
#del(a)

# integers and floats
a = 10
b = a
a = a + 1
a += 10
c = 5.5
d = c + a

print a
print b
print c
print d

# types
print type(a)
print type(b)
print type(c)
print type(d)

# other ways of defining types
# floats
my_float = float(5)
print type(my_float)
print my_float

b = 100 / 10.0
print type(b)
print my_float

#integers
my_int = int(50.0)
print type(my_int)
print my_int

# strings
my_string_1 = str(5)
my_string_2 = "10"
print my_string_1
print my_string_2
print my_string_1 + my_string_2

#===============================================================================
#
# operators
#
#===============================================================================

# arithmetic operators
# +, -, *, / (addition, subtraction, multiplication, division)
# ** (exponent)
# % (modulus, divides left hand operand by right hand operand and returns
# remainder)
# // (floor division, division of operands where the result is the quotient
# in which the digits after the decimal point are removed.)

a = 10
b = 5
c = a + b
print c

d = c / 10 + b * 5
print d

d_square = d**2
print d_square

print d_square % 2
print d_square % 3
print d_square % 4
print d_square % 14

print 2 % 2

print 8 // 3
print -8 // 3

# assignment operators
# =, += Add AND, -= Subtract AND, *= Multiply AND, /= Divide AND, %= Modulus AND, **= Exponent AND, //= Floor Division
# usually used in loops, except =
#
# comparison operators
# ==, != or <>, >, <, >=, <=
# usually used for conditional statements
#
# membership operators, identity operators
# in, not in, is, is not
# usually used for conditional statements

#===============================================================================
#
# boolean expressions (True, False, ==, !=)
# conditionals ( if, elif, else)
#
#===============================================================================

# single conditional statement, if-statement
var_1 = 57
if var_1 == 57:
    print "The value of this variable is 57"

# two-conditional statement, if-else-statement
var_2 = 100
if var_2 == 57:
    print "The value of this variable is 57"
else:
    print "The value of this variable is not 57. It is " + str(var_2)

# multi-conditional statement, if-elif-else-statement
var_3 = 30

if var_3 < 20:
    print "The value of this variable is smaller than 20"
elif var_3 >= 20 and var_3 <= 60:
    print "The value of this variable is greater than or equal to 20 but smaller than or equal to 60"
else:
    print "The value of this variable is bigger than 60"

# True or False, == or !=
print True or False
print True and False
print 10 == 10
print 50 <= 60
print not True

# There are only two Boolean constants, True and False.
# They must be capitalized as shown.
# The following constants also evaluate to False:
# None 0 0L 0.0 '' [] () {} set([])
# All other values are treated like True in logical expressions.
