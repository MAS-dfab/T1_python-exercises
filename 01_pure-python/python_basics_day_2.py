#===============================================================================
#
# sequence types
# lists ( tuples, dictionaries)
#
#===============================================================================

# lists are a list of values
# constructed with square brackets, separating items with commas
# these items can have any types, e.g.

number_list = [1, 3, 4, 6, 8, 11, 13]
string_list = ["hello", "goodbye", "no more ideas", "etc."]
mixed_list = ["strings", 5, 6, 6.7, True, "etc."] # this is NOT a good way of using list and should be avoided!!!!

# arithmetic progressions in lists, range() function
print range(1,100)
print range(1,100,5)
print range(100, -10, -20)

# basic list operations
# len(), + (concatenation), * (repetition), in (membership)

print len(string_list)
print string_list + number_list
print string_list*3
print "hello" in string_list
print "houdini" in string_list

# basic list methods
# access values in list
print string_list[0], ", string_list element 1"
print string_list[1], ", string_list element 2"

# slicing
print string_list[2:4]
print string_list[1:3]
print string_list[-1]

# append, extend, insert, pop, remove

# initialize empty list
my_list = []

# append object to the end of the list, list.append(obj)
my_list.append(1)
print my_list
my_list.append(10)
print my_list
my_list.append(100)
print my_list

# extend objects to the end of the list, list.extend([obj, obj, obj])
my_list.extend([5]*10)
print my_list

# inserts an object into a list at specific index
my_list.insert(0, "start")
print my_list
my_list.insert(len(my_list), "end")
print my_list

# removes and returns last object from list
obj = my_list.pop()
print my_list
print obj

# removes object from list

my_list.remove(10)
#my_list.remove(10)
print my_list


# reverse, sort

# reverses objects of list in place

my_list.reverse()
print my_list

# sorts objects of list, use compare func if given

my_list.sort()
print my_list

# other list options
# count, index, etc.


# tuples
# tuple is a sequence of immutable Python objects.
# tuples cannot be changed unlike lists

my_tuple_1 = (1, 2, 3)
my_tuple_2 = ("hello", "goodbye")
print my_tuple_1
print my_tuple_1 + my_tuple_2

# value access similar to lists
# basic operations: len(), concatenation, repetition, membership, iteration

# simple dictionaries
# a list of keys - each key is pointing to a value
# keys have to be immutable data type, values can be of any type

# example
my_dict = {"Name" : "David", "Age" : 21, "Profession" : "Architect"}
print "my_dict['Name']: ", my_dict['Name']
print "my_dict['Age']: ", my_dict['Age']

my_dict['Age'] = 28; # update existing entry
my_dict['Programme'] = "MAS DFAB"; # add new entry

print "my_dict['Name']: ", my_dict['Name']
print "my_dict['Programme']: ", my_dict['Programme']


#===============================================================================
#
# loops (for, while, nested loops, etc.)
#
#===============================================================================

# while loop
# repeats statement(s) while a condition is TRUE
# make sure to ALWAYS have an exit condition

break_condition = 0
while break_condition < 10:
    break_condition = break_condition + 1
    print break_condition
else:
    print "out of while loop"

# for loop
# iterating over items of a sequence (usually a list)

pets = ["dog", "cat", "horse", "rabbit", "snake"]
for pet in pets:
    print pet

numbers = range(5)
for n in numbers:
    print n / 5.0 + 100

for letter in "Python":
    print "current letter: ", letter

# iterating over sequence index
for index in range(len(pets)):
    print index, pets[index]

for i,pet in enumerate(pets):
    print i, pet


# nested loops
points = []
x_size = 10
y_size = 6

for i in range(x_size):
    for j in range(y_size):
        print i, j
else:
    print x_size * y_size, "points have been generated"

# break (terminates and steps to the statement immediately following the loop)
# continue (skip remainder of body and immediately retest its condition prior to
# reiterating)
# pass (no command or statement)
