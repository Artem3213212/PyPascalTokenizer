PyPascalTokenizer
=================

Module for Python 3. It does tokenizing of Pascal code (it's planned to support full Delphi and FreePascal syntax).

API
===

Token format:
-------------

It is tuple with 4 elements:

* token - string with token text

* begin - tuple with line and symbol (start from 0) where token begin(first symbol)

* end - tuple with line and symbol (start from 0) where token end(first no token symbol)(if token end when line end
symbol num = line len)

* ended - True if it was last token

Class PasTokenizer has constructor, which needs param: list of source code lines. It has methods:

* __init__(s) - Create class, get list of strings what was tokenized

* get_next() - get next token and save end pos

* read_next() - get next token, but not save end pos

* is_ended() - check if text ended

Class PasTokenizerStack has constructor, which needs param: list of source code lines. It has methods:

* __init__(s) - Create class, get list of strings what was tokenized

* push(s) - push token to stack

* pop() - pop token from stack

* read_last() - read top token in stack

* is_ended() - check if stack ended




Author
=====
Artem Gavrilov (@Artem3213212 at Github)
