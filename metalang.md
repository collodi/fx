fx as a meta-language
---

This is a very premature concept.
It needs an extraordinary amount of thoughts/work to make it actually worth something.

Consider a programming language that is so basic to be able to do anything by itself.
However, we can define the smallest unit and possible values.
We are also able to define basic operations on them.
The definition of a unit and operations on them make up a `discipline`.

Let me elaborate what I mean with some case examples.

In our first case, the `discipline` is boolean algebra.

We define our smallest unit to be `boolean`.
All possible values of a boolean are 0 and 1.
We have defined the smallest unit and possible values.

Then, we go on to define some basic operations on boolean.

The boolean `AND` is defined like this:
```
fx AND
	[ (0, 0) 0
	[ (0, 1) 0
	[ (1, 0) 0
	[ (1, 1) 1
```

Along with definitions of other boolean operations, our boolean algebra discipline is complete.

* For now, let's assume all argument types in operations match the defined unit in the discipline.
* This may have to change when we have to define operations on more than 1 unit.
* For example, a multiplication between a vector and a scalar.
