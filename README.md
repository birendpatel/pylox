# pylox
Python implementation of the Lox programming language created by Bob Nystrom.

This implementation contains a few additions not found in the standard Lox
language. For instance, a lightweight preprocessor is included. The original
JLox implementation by Nystrom is located at https://github.com/munificent

```
#pragma env_debug on

print "this is the lox language!"

var x = 10;
var y = 15;

if (x == y) {
        print "pass";
} else {
        print "fail";
}
```
