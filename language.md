statically typed
whitespace sensitive
NOT pure

Types
---

Pattern = an expression with a placeholder variable name and resolves to 0 or 1 on evaluation
Number = floating point number (for now)
Tuple = ( a b c )

* Notes
 - Patterns can only be declared in specific places.
 - () is used for empty value

Function definition
---

(context pattern) def (function name)
	(argument pattern) { behavior }

Technically, all functions have 1 context and 1 argument.
We can pass and/or return multiple values using a tuple.

Calling functions
---

(context) (name)[?|!] ( arg0 arg1 ... )

> ? casts the output to bool  
> ! replaces the context with the return value  

* Notes on !
 - function call still returns the return value
 - type do not have to match (changes the type of the variable)

Pattern Matching
---

Done using a function which takes a Pattern and some value.
The function returns 1 if value fits in the pattern.

Context
---

A context is simply an initialized variable.

Sometimes, a rhs expression may be a context.
For example, a function may modify the content of a given path.
In this case, the path is a context.

Custom Types
---

A custom type can be created using `pattern` keyword.
> *pattern* Point = ( Number Number )

A constant can be declared with `pattern`.
> *pattern* PI = 3.14
