# What is Generalized Map Function (generalmap)
This is an generalized map function in python, which can lift basic function over various data structures and user defined objects. It implements the idea borrowed from functional programming language, that is to define a simple function first to tackle a small piece of problem, then reuse this function to apply to complicated data structures. This process is called lifting.

An simple example, given `lst=[1, 2, 3]` and function `f = lambda x: x+1`, this functin only focuses on solving the problem for one element in the list, but `map(f, lst)` will apply `f` to a list, which is a more complicated structure. In a nutshell, the map function let you focus on the atom part or essential part of the problem, then reuse the function in a very smart and cheap way.

However, the default map function provided by python is very restrictive:
* it can only apply to iteratable
* it can only cross one level of the structure
* it is not easy to apply to user defined objects

and these are what generalmap package can do.

# Basic Usage
## Lift function automatically
This is the default behavior, the gMap function will cross all predefined structures then apply `f` to the atom data types like `int, float, string` (defaultly) or `int, float` (if set `intoStr=True`). One caveat is that `f` will always apply to the same level of structure.

An one level example:
```python
# define different structures
sList = [1, 2, 3]
sTuple = (1, 2, 3)
sDict = {1: 2, 2: 3, 3: 4}

# create function
foo = lambda x: x+1

# create default gMap object
mp = GMap()

# apply f and print the results
print(mp.gMap(foo, sList))
print(mp.gMap(foo, sTuple))
print(mp.gMap(foo, sDict))
```
with output as:
```python
[2, 3, 4]
(2, 3, 4)
{1: 3, 2: 4, 3: 5}
```
