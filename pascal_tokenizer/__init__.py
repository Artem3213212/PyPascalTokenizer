#
# PyPascalTokenizer
# Author: Artem Gavrilov (@Artem3213212)
# License: MPL 2.0
#

SYMS1 = ['(',')','[',']','/','|','\\','@','#','=','>','<',':',';',',','.','$','+','-','*']
SYMS2 = ['>=','<=','<>',':=','..','-=','+=','/=','*=']
SPACES = ['\f','\n','\r','\t','\v',' ']
NO_NAME_SYMS = SYMS1 + SPACES + ['{','}']

def is_comment(s):
    return (s[0]=='{' and s[-1]=='}') or (s[:2]=='(*' and s[-2:]=='*)') or s[:2]=='//'

def is_name(s):
    if not(s[0] in '&abcdefghijklmnopqrstuvwxyz_'):
        return False
    for i in s[1:].lower():
        if not (i in 'abcdefghijklmnopqrstuvwxyz0123456789_'):
            return False
    return True

def is_string(s):
    return s[0]=="'" and s[-1]=="'"

class PasTokenizer():
    def __init__(self, s):
        self.s, self.x, self.y, self.ended = s, 0, 0, False
        self._do_readable_()
        self._skip_spaces_()

    def _do_readable_(self):
        if self._is_readable_:
            if self.x+1 == len(self.s):
                self.ended = True
            else:
                self.x+=1
                self.y=0
                while not self.s[self.x]:
                    if self.x+1 == len(self.s):
                        self.ended = True
                        break
                    self.x+=1

    def _is_readable_(self):
        return len(self.s[self.x])<=self.y

    def _next_readable_(self):
        self.y=+1
        if self._is_readable_():
            if self.x+1 == len(self.s):
                self.ended = True
            else:
                self.x+=1
                self.y=0
                while not self.s[self.x]:
                    if self.x+1 == len(self.s):
                        self.ended = True
                        break
                    self.x+=1
            return True
        else:
            return False

    def _skip_spaces_(self):
        while self.s[self.x][self.y] in SPACES:
            self._next_readable_()

    def _getpos_(self):
        return self.x, self.y

    def _setpos_(self, i0, i1):
        self.x, self.y, self.ended = i0, i1, False
        self._do_readable_()

    def get_next(self):
        begin_pos = self._getpos_()
        ml, ss, f = '', '', True
        str_changed = False
        while f:
            line = self.s[self.x]
            now_sym = line[self.y]
            l = len(line)
            if self.y+1 != l:
                next_sym = line[self.y+1]
            else:
                next_sym = ''
            if ml == '':
                if now_sym == '/':
                    if next_sym == '/':
                        ss = line[self.y:]
                        self.y = l
                        break
                elif now_sym == '{':
                    ml = '}'
                    ss=[str_changed]
                    last_i0 = self.x
                elif now_sym == '(':
                    if next_sym == '*':
                        ml = ')'
                        self.y+=1
                        last_i0 = self.x
                        ss = [now_sym+next_sym]
                    else:
                        ss = '('
                        self.y+=1
                        break
                else:
                    if now_sym in SYMS1:
                        ss = now_sym
                        if now_sym + next_sym in SYMS2:
                            self.y+=2
                            ss = ss + next_sym
                        break
                    elif now_sym=="'":
                        ss="'"
                        self.y+=1
                        if next_sym!='':
                            ss = ss + next_sym
                            while line[self.y]!="'":
                                self.y+=1
                                if not self._is_readable_():
                                    break
                                ss = ss + line[self.y]
                        break
                    else:
                        while not(line[self.y] in NO_NAME_SYMS):
                            ss=ss+line[self.y]
                            self.y+=1
                            if not self._is_readable_():
                                break
                        break
            else:
                while last_i0!=self.x:
                    ss.append('')
                ss[-1] = ss[-1] + now_sym
                if now_sym==ml:
                    if ml=='}':
                        ml=''
                    elif self.y!=0:
                        if line[self.y-1]=='*':
                            ml=''
            self._next_readable_()
        if len(ss)==1:
            ss=ss[0]
        ss=(ss,begin_pos,self._getpos_(),self.ended)
        self._do_readable_()
        self._skip_spaces_()
        return ss

    def read_next(self):
        i0, i1 = self._getpos_()
        z = self.get_next()
        self._setpos_(i0, i1)
        return z

    def is_ended(self):
        return self.ended

class PasTokenizerStack():
    def __init__(self, s, comments=True):
        self.main = PasTokenizer(s)
        self.stack = []
        if comments:
            self._pop_ = self._get_with_comments_
        else:
            self._pop_ = self._get_without_comments_

    def _get_with_comments_(self):
        return self.main.get_next()

    def _get_without_comments_(self):
        s=(0,'//')
        while is_comment(s[1]):
            return self.main

    def push(self, s):
        self.stack.append(s)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        else:
            return self._pop_()

    def read_last(self):
        if not self.stack:
            self.stack.append(self._pop_())
        return self.stack[-1]

    def is_ended(self):
        return self.stack or self.main.is_ended()

