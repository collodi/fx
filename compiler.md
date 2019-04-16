Lazy evaluation
Copy-on-write
Unicode support

Should start with a repl: 1 expression = 1 input
A source file is a list of expressions.

1 global variable.
1 expression may modify the globe at the end. (with it's result)

Theory of computation
---

Variable assignment
> only thru pattern matching in function (?)

Function recursion
> defined within a function defintion

Function composition
> think of `]` as piping in linux
> f(g(x)) = x ] g ] f		x is treated like a function

> what about `[`? nah
> if function types are defined, the types are easier to read
> ex.
>   f: float -> int
>   g: int -> float
>   x: int
>
>   x ] g has type float
>   x ] g ] f has type int

enclosing a partial result with () makes the enclosed operation
a tuple, and this prioritizes this operation 

Pairing function \<a, b\>
> tuple ( a, b )
> each function takes exactly 1 input and returns 1 value
> multiple values are enclosed as a tuple

Function definition syntax
---

1. function name
1. type signature
1. call pattern
1. arguments
1. operations

Function definition using pattern matching
---

this (hopefully) lets the user to define the function is called
along with the operations in the function

ideas?

use pattern matching to name variables in the input tuple first
and the next part can give the pattern a function is called

> ex.
>     fn + (:x, :y)	naming inputs (fn is a keyword for function definition)
>     x + y		define call pattern

REPL
---

- [x] integer
- [x] float
- [x] tuple

Pattern matching + variable assignment
---

For matching and assigning, use `:<variable>`.

> \_ matches a value and discards it (no assignment)
> ... matches any number of values in a tuple and discards it (no assignment)

> :x matches a variable and puts it in x
> :x > 5 matches a value greater than 5 and puts it in x
> ..:xs matches any number of values in a tuple and puts it in tuple xs

Note: ... (or ..:) can only be placed at the beginning or the end of a tuple

> examples
>     (:x, :y, :z)
>     (:x, \_)
>     (:x, ...)
>     (:x, :y, ...)
>     (:x, :y, ..:xs)
>     (..., :x, :y)

An assignment can be used within the same tuple for pattern matching.

> ex.
>     (:x, :y > x) matches a 2-tuple where second is bigger than first

Minimum features to write in Rust
---

We will (try to) harvest Rust's move feature.


Implementing the compiler in self
---

Assuming we have an expression in a String `input`.
We first need a function to separate a token from the head of `input`.

```
token = input.takeWhile(!= " ")
input.dropWhile! (!= " ")
```
