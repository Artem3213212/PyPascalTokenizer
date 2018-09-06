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

Class PasTokenizer
------------------

* __init__(lines): params: list of source code strings
* get_next(): get next token and change end pos
* read_next(): get next token, but don't change end pos
* is_ended(): check if text ended

Class PasTokenizerStack
-----------------------

* __init__(lines, comments=True): params: list of source code strings; "comments" allows to get also comment-tokens (otherwise tokenizer skips them)
* push(s): push token to stack
* pop(): pop (get and delete) token from stack
* read_last(): read (get but don't delete) top token from stack
* is_ended(): check if stack ended

Class PasTokenizerParallelStack
-------------------------------

Descendant of PasTokenizerStack, which uses thread(s) for parsing entire file. Before destroying it you mast call stop().

* __init__(lines, comments=True, qlong=1000): additonal param: size of internal queue buffer
* stop(): call it before del object

Utils
-----

Helper functions to analyze token text.

* is_name(s): Check for valid identifier (can be reserved word too).
* is_comment(s): Check for valid comment.
* is_string(s): Check for string constant.


Author
=====
Artem Gavrilov (@Artem3213212 at Github)
