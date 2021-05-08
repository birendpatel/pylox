# pylox
Python implementation of the Lox programming language created by Bob Nystrom.

This implementation contains a few additions not found in the standard Lox
language. For instance, a lightweight preprocessor is included. The original
JLox implementation by Nystrom is located at https://github.com/munificent

```
#pragma tok_debug on
#pragma parse_debug on
#pragma env_debug on

var x = 2;
var y = 3;
var z = 5;

print (x + y) * z;
```
