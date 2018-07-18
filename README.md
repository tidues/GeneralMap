# What is Generalized Map Function (generalmap)
This is a generalized map function in python, which can lift basic function over various data structures and user defined objects. It implements the idea borrowed from functional programming language, that is to define a simple function first to tackle a small piece of problem, then reuse this function to apply to complicated data structures (sometimes called function lifting).

An simple example, given `lst=[1, 2, 3]` and function `f = lambda x: x+1`, this functin only focuses on solving the problem for one element in the list, but `map(f, lst)` will apply `f` to a list, which is a more complicated structure. In a nutshell, the map function let you focus on the atom part or essential part of the problem, then reuse the function in a very smart and cheap way.

However, the default map function provided by python is very restrictive:
* it can only apply to iteratable
* it can cross only **one level** of the structure
* it is not easy to apply to user defined objects

and these are what generalmap package can do.

# Basic Usage
Some examples below like applying function to nonhomogeneous data structure are **not good coding styles**, they are simply used to demonstrate what this pacakge can do.

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

Example for two level mixed nonhomogeneous structure:
```python
sMixed = [(1, 2), [3, 4, 5], {6: 6, 7: 7}, range(3), slice(None, 10, 2)]

def foo x:
    return x+1

mp = GMap()

print(mp.gMap(foo, sMixed))
```
with output as:
```python
[(2, 3), [4, 5, 6], {6: 7, 7: 8}, range(1, 4), slice(1, 11, 2)]
```
notice different structures have their own unique lifting behaviors predefined.


In defualt, the gMap will not crossing string to apply function on each character, but this can be changed:
```python
sStr1 = '123'

foo = lambda x: str(int(x)+1)

mp = GMap(intoStr=True)  # change default behavior

print(mp.gMap(foo, sStr1))
```
with output:
```python
234
```

## Lift function by specifying depth
With depth specified, gMap will apply `f` to the desinged level without caring about the input type, with depth 1 as one level structure (behavior of map function in python).

A example:
```python
sMixed = [[(1, 2, 4), (4, 5)], [(6, 7, 8), '91011']]

foo = lambda x: x[0]

mp = GMap(recDepth=2)  #  specify depth

print(mp.gMap(foo, sMixed))
```
with output:
```python
[[1, 4], [6, '9']]
```
The `sMixed` has a three-level strucure, but we force gMap only apply to the second level, so the function will take tuples and string as input. Notice we don't need to specify the `intoStr` here, for we don't lift function into the string structure.

## Current supported strucutres
The basic (bottom) types including:

`int, float, string`

the structure types including:

`list, tuple, map, range, slice`

if with `intoStr` set as `True`, then `string` is a structure type instead of basic.

# Advanced Usage: Apply to User Defined Objects
There are two more things user can do with this package:
1. Register new basic types.
1. Register new structure types 

## Register new basic types

This can be accompalished by the method `mp.regBasicType(cls)` where `cls` is the class. For instance, suppose there is a new data type `double` defined, and we want it to be a bottom type, so that when we apply gMap automatically, it'll stop and apply `f` on the data of this type. 

Notice, if register a new basic type that is already in the structure types, it will be **removed from** the structure type.

## Register new structure types

The method `mp.regStructType(cls, clsRule)` can register a new structure type, where `cls` is a class and `clsRule` is a rule description function. Same as before, registering an existing basic type to structure type will remove it from the baic type list. 

With new structure type defined, it can be mixed with other structure types to build complicated data structure. And gMap can be used on these objects the way same as before.

Below is a new data type called MSet (multiset).
```python
# a self defined container (multiset)
class MSet:
    def __init__(self, lst):
        self.elems = lst

    def __repr__(self):
        return('MSet' + str(self.elems) + '')

    def __getitem__(self, idx):
        if type(idx) is int:
            return self.elems[idx]
        else:
            return MSet(self.elems[idx])

    def toList(self):
        return self.elems
```

then we need to define a map rule function for this class

```python
# define the function that describe the map rule
# each term will be explained in the next section
def msetMapRule(mset):
    isBottom = False
    const = MSet
    paramList = mset.toList()
    paramMapIdx = range(len(paramList))
    ifExpand = False
    projFunc = lambda x: x
    liftFunc = lambda x, res: res
    return (isBottom, const, paramList, paramMapIdx, ifExpand, projFunc, liftFunc)
```

with both class and rules are defined, we can apply gMap as same as before:

```python
mp = gMap()  # create gMap object
mp.regStructType(MSet, msetMapRule) # register new structure type with rule

# define functions and data
# a two level MSet
mset0 = MSet([1,2])
mset1 = MSet([3,4])
mset = MSet([mset0, mset1])

# a tuple of MSets
mtuple = (MSet([1,2]), MSet([3,4]))

# function to apply
foo = lambda x: x+1

# apply and show results
print(mp.gMap(foo, mset))
print(mp.gMap(foo, mtuple))
```
the output is
```python
MSet[MSet[2, 3], MSet[4, 5]]
(MSet[2, 3], MSet[4, 5])
```
