#
# PyPascalTokenizer
# Author: Artem Gavrilov (@Artem3213212)
# License: MPL 2.0
#

import queue, threading

SYMS1 = ['(',')','[',']','/','|','\\','@','=','>','<',':',';',',','.','+','-','*','^']
SYMS2 = ['>=','<=','<>',':=','..','-=','+=','/=','*=','**','><','(.','.)','<<','>>']
SPACES = ['\f','\n','\r','\t','\v',' ']
NO_NAME_SYMS = SYMS1 + SPACES + ['{','}']
CHARS_ID0 = '&abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
CHARS_ID = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'

def is_comment(s):
    if type(s) is list:
        return True
    else:
        return s.startswith('{') or s.startswith('(*') or s.startswith('//')

def is_name(s):
    if len(s)<=0:
        return False
    if s=='&':
        return False
    if not (s[0] in CHARS_ID0):
        return False
    for i in s[1:]:
        if not (i in CHARS_ID):
            return False
    return True

def is_string(s):
    return s.startswith("'")

class PasTokenizer():
    def __init__(self, s):
        self.s, self.y, self.x, self.ended = s, 0, 0, False
        self._skip_spaces()

    def _do_readable(self):
        if not self._is_readable():
            if self.y+1 == len(self.s):
                self.ended = True
            else:
                self.y+=1
                self.x=0
                while not self.s[self.y]:
                    if self.y+1 == len(self.s):
                        self.ended = True
                        break
                    self.y+=1
            return True
        else:
            return False

    def _is_readable(self):
        return len(self.s[self.y])>self.x

    def _next_readable(self):
        self.x+=1
        return self._do_readable()

    def _skip_spaces(self):
        self._do_readable()
        if not self.ended:
            while self.s[self.y][self.x] in SPACES:
                self._next_readable()
                if self.ended:
                    break

    def _get_pos(self):
        return self.y, self.x

    def _set_pos(self, i0, i1):
        self.y, self.x, self.ended = i0, i1, False
        self._do_readable()

    def get_next(self):
        begin_pos = self._get_pos()
        ml, ss, f = '', '', True
        str_changed = False
        while f and not self.ended:
            line = self.s[self.y]
            now_sym = line[self.x]
            l = len(line)
            if self.x+1 != l:
                next_sym = line[self.x+1]
            else:
                next_sym = ''
            if ml == '':
                if now_sym == '/':
                    if next_sym == '/':
                        ss = line[self.x:]
                        self.x = l
                        break
                elif now_sym == '{':
                    ml = '}'
                    ss=[now_sym]
                    last_i0 = self.y
                elif now_sym == '(':
                    if next_sym == '*':
                        ml = ')'
                        self.x+=1
                        last_i0 = self.y
                        ss = [now_sym+next_sym]
                    else:
                        ss = '('
                        self.x+=1
                        break
                else:
                    if now_sym in SYMS1:
                        ss = now_sym
                        self.x+=1
                        if now_sym + next_sym in SYMS2:
                            self.x+=1
                            ss = ss + next_sym
                        break
                    elif now_sym=="'":
                        ss="'"
                        self.x+=1
                        if next_sym!='':
                            ss = ss + next_sym
                            while line[self.x]!="'":
                                self.x+=1
                                if not self._is_readable():
                                    self.x-=1
                                    break
                                ss = ss + line[self.x]
                            self.x+=1
                        break
                    else:
                        while not(line[self.x] in NO_NAME_SYMS):
                            ss=ss+line[self.x]
                            self.x+=1
                            if not self._is_readable():
                                break
                        break
            else:
                while last_i0!=self.y:
                    ss.append('')
                    last_i0+=1
                ss[-1] = ss[-1] + now_sym
                if now_sym==ml:
                    if ml=='}':
                        self.x+=1
                        break
                    elif self.x!=0:
                        if line[self.x-1]=='*':
                            self.x+=1
                            break
            self._next_readable()
        if len(ss)==1:
            ss=ss[0]
        ss=(ss,begin_pos,self._get_pos(),self.ended)
        self._skip_spaces()
        return ss

    def read_next(self):
        i0, i1 = self._get_pos()
        z = self.get_next()
        self._set_pos(i0, i1)
        return z

    def is_ended(self):
        return self.ended

class PasTokenizerStack():
    def __init__(self, s, comments=True):
        self.main = PasTokenizer(s)
        self.stack = []
        if comments:
            self._pop = self._get_with_comments
        else:
            self._pop = self._get_without_comments

    def _get_with_comments(self):
        return self.main.get_next()

    def _get_without_comments(self):
        while True:
            s = self.main.get_next()
            if not is_comment(s[0]):
                return s
            if s[3]:
                return ('',(0,0),(0,0),True)

    def push(self, s):
        self.stack.append(s)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        else:
            return self._pop()

    def read_last(self):
        if not self.stack:
            self.stack.append(self._pop())
        return self.stack[-1]

    def is_ended(self):
        return self.stack and self.main.is_ended()

class PasTokenizerParallelStack(PasTokenizerStack):
    def __init__(self, s, comments = True, qlong = 1000):
        super(PasTokenizerParallelStack,self).__init__(s, comments)
        self.queue = queue.Queue(qlong)
        th = threading.Thread(target = self._work, args = (self,))
        th.start()

    def _get_with_comments(self):
        s = self.queue.get()
        return s

    def _get_without_comments(self):
        while True:
            s = self.queue.get()
            if not is_comment(s[0]):
                return s
            if s[3]:
                return ('',(0,0),(0,0),True)

    def _work(self,s):
        while not self.main.is_ended():
            self.queue.put(self.main.get_next())
        self.queue.put(('',(0,0),(0,0),True))

    def is_ended(self):
        return self.stack and self.main.is_ended()and self.queue.empty()

    def stop(self):
        self.main.ended = True
        try:
            while not self.queue.get_nowait()[3]:
                pass
        except:
            pass
