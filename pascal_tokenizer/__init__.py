#
# PyPascalTokenizer
# Author: Artem Gavrilov (@Artem3213212)
# License: MPL 2.0
#

SYMS1 = ['(',')','[',']','/','|','\\','@','#','=','>','<',':',';',',','.','$','+','-','*']
SYMS2 = ['>=','<=','<>',':=','..']
SPACES = ['\f','\n','\r','\t','\v',' ']
NO_NAME_SYMS = SYMS1 + SPACES + ['{','}']

class PasTokenizer():
    def __init__(self, s):
        self.s, self.i0, self.i1, self.ended = s, 0, 0, False
        self.__do_readable__()
        self.last_data = ('',self.getpos(),self.getpos(),self.ended)

    def __do_readable__(self):
        if self.__is_readable__:
            if self.i0+1 == len(self.s):
                self.ended = True
            else:
                self.i0+=1
                self.i1=0
                while not self.s[self.i0]:
                    if self.i0+1 == len(self.s):
                        self.ended = True
                        break
                    self.i0+=1

    def __is_readable__(self):
        return len(self.s[self.i0])<=self.i1

    def __next_readable__(self):
        self.i1=+1
        if self.__is_readable__():
            if self.i0+1 == len(self.s):
                self.ended = True
            else:
                self.i0+=1
                self.i1=0
                while not self.s[self.i0]:
                    if self.i0+1 == len(self.s):
                        self.ended = True
                        break
                    self.i0+=1
            return True
        else:
            return False

    def __skip_spaces__(self):
        while self.s[self.i0][self.i1] in SPACES:
            self.__next_readable__()

    def get_next(self):
        self.__skip_spaces__()
        begin_pos = self.getpos()
        ml, ss, f = '', '', True
        str_changed = False
        while f:
            line = self.s[self.i0]
            now_sym = line[self.i1]
            l = len(line)
            if self.i1+1 != l:
                next_sym = line[self.i1+1]
            else:
                next_sym = ''
            if ml == '':
                if now_sym == '/':
                    if next_sym == '/':
                        ss = line[self.i1:]
                        self.i1 = l
                        break
                elif now_sym == '{':
                    ml = '}'
                    ss=[str_changed]
                    last_i0 = self.i0
                elif now_sym == '(':
                    if next_sym == '*':
                        ml = ')'
                        self.i1+=1
                        last_i0 = self.i0
                        ss = [now_sym+next_sym]
                    else:
                        ss = '('
                        self.i1+=1
                        break
                else:
                    if now_sym in SYMS1:
                        ss = now_sym
                        if now_sym + next_sym in SYMS2:
                            self.i1+=2
                            ss = ss + next_sym
                        break
                    elif now_sym=="'":
                        ss="'"
                        self.i1+=1
                        if next_sym!='':
                            ss = ss + next_sym
                            while line[self.i1]!="'":
                                self.i1+=1
                                if not self.__is_readable__():
                                    break
                                ss = ss + line[self.i1]
                        break
                    else:
                        while not(line[self.i1] in NO_NAME_SYMS):
                            ss=ss+line[self.i1]
                            self.i1+=1
                            if not self.__is_readable__():
                                break
                        break
            else:
                while last_i0!=self.i0:
                    ss.append('')
                ss[-1] = ss[-1] + now_sym
                if now_sym==ml:
                    if ml=='}':
                        ml=''
                    elif self.i1!=0:
                        if line[self.i1-1]=='*':
                            ml=''
            self.__next_readable__()
        if len(ss)==1:
            ss=ss[0]
        self.last_data=(ss,begin_pos,self.getpos(),self.ended)
        self.__do_readable__()
        return ss

    def read_next(self):
        i0, i1 = self.getpos()
        z = self.get_next()
        self.setpos(i0, i1)
        return z

    def getpos(self):
        return self.i0, self.i1

    def setpos(self, i0, i1):
        self.i0, self.i1, self.ended = i0, i1, False
        self.__do_readable__()

    def is_ended(self):
        return self.ended

    def get_last_data(self):
        return self.last_data
