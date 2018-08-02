PyPascalTokenizer
=================

Module for Python 3. It does tokenizing of Pascal code (it's planned to support full Delphi and FreePascal syntax).

API
===

Token struct
------------

Token is saved as 4-tuple (text, begin, end, final):

* text: string with token text
* begin: position of token start, tuple (y, x), where y - 0-based line index and x - 0-based character index in line
* end: position after token end, tuple (y, x)
* final: bool, True if it was last token

Class PasTokenizer methods
--------------------------

* __init__(lines): param of constructor is list of strings with Pascal code
* get_next(): get next token and change end pos
* read_next(): get next token, but don't change end pos
* is_ended(): check if text ended

Class PasTokenizerStack methods
-------------------------------
 
* __init__(lines) - param of constructor is list of strings with Pascal code
* push(s): push token to stack
* pop(): pop (get and delete) token from stack 
* read_last(): read (get but don't delete) top token from stack
* is_ended(): check if stack ended

Author
=====
Artem Gavrilov (@Artem3213212 at Github)
