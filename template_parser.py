"""
TODO: compare hogan, dust performance. Dust has a cool javascript based test platform I could leverage
TODO: handle inverted sections
TODO: make sure Unicode works
TODO: implement these backends: Python, Cython, Ruby, Javascript
TODO: benchmark http://akdubya.github.com/dustjs/benchmark/index.html
TOREAD: http://engineering.linkedin.com/frontend/client-side-templating-throwdown-mustache-handlebars-dustjs-and-more
http://www.civilwar.org/education/history/biographies/ambrose-burnside.html
"""
import re
from ply import lex, yacc
import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG) # TODO: set on command line

DEFAULT_DELIM_START = r"\{\{"
DEFAULT_DELIM_END = r"\}\}"

def tagdata(t):
    return t.lexer.lexmatch.groupdict()["id"]

class NosebugParser(object):
    
    def __init__(self, 
                 delim_start=None, 
                 delim_end=None,
                 preserve_whitespace=False,
                 ):
        self._stack = []
        
        if delim_start:
            # escape in case delims are re chars
            delim_start = "".join(["\\" + x for x in list(delim_start)])
            
        if delim_end:
            delim_end = "".join(["\\" + x for x in list(delim_end)]) 
        
        self.delim_start = delim_start or DEFAULT_DELIM_START
        self.delim_end = delim_end or DEFAULT_DELIM_END
        
        if not preserve_whitespace:
            # consume and discard any whitespace at the end of delimiters if nothing but whitespace follows till end of line
            # TODO: not quite right--results in extra leading spaces in complex test, and breaks partial_recursion
            self.delim_end = r"((%s\s*\n)|(%s))" % (self.delim_end, self.delim_end)
        
        self.path_regex = r"(\.|(\.\.\/)*[a-zA-Z_][a-zA-Z_0-9\/]*)"
    
    tokens = ['STRING',
              'TAG_SECTION_START',
              'TAG_INV_SECTION_START',
              'TAG_SECTION_END',
              'TAG_COMMENT',
              'TAG_PARTIAL',
              'TAG_VAR_UNESCAPED',
              'TAG_VAR_ESCAPED',
              ]
    
    def t_STRING(self, t):
        r'[^(%(delim_start)s)]+'
        return t

    def t_TAG_SECTION_START(self, t):
        r'(%(delim_start)s\#(?P<id>%(path)s))%(delim_end)s'
        t.value = tagdata(t)
        self._stack.append(t.value)
        return t

    def t_TAG_INV_SECTION_START(self, t):
        r'(%(delim_start)s\^(?P<id>%(path)s))%(delim_end)s'
        raise NotImplementedError("TODO")
        return t

    def t_TAG_SECTION_END(self, t):
        r'(%(delim_start)s\/(?P<id>%(path)s))%(delim_end)s'
        var = tagdata(t)
        try:
            expected = self._stack.pop()
        except IndexError:
            raise SyntaxError("got end section '%s' without corresponding start section" % var)
        else:
            if expected != var:
                raise SyntaxError("mismatched section start/end (got '%s', expected '%s')" % (var, expected)) 
        t.value = var
        return t

    def t_TAG_COMMENT(self, t):
        r'(%(delim_start)s\!(?P<id>.*))%(delim_end)s'
        t.value = tagdata(t)
        return t

    def t_TAG_PARTIAL(self, t):
        r'(%(delim_start)s\>(?P<id>%(path)s))%(delim_end)s'
        t.value = tagdata(t)
        return t

    def t_TAG_VAR_UNESCAPED(self, t):
        r'(%(delim_start)s\&(?P<id>%(path)s))%(delim_end)s'
        t.value = tagdata(t)
        return t
    
    def t_TAG_VAR_ESCAPED(self, t):
        r'(%(delim_start)s(?P<id>%(path)s))%(delim_end)s'
        t.value = tagdata(t) 
        return t
    
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    
    def t_error(self, t):
        raise TypeError("Syntax error (line %d): %s" % (t.lexer.lineno+1, t.value))

    def build(self, **kwargs):
        macros = {"delim_start" : self.delim_start, "path" : self.path_regex, "delim_end" : self.delim_end}
        for name, value in self.__class__.__dict__.items():
            if name.startswith("t_") and callable(value):
                if value.__doc__:
                    value.__doc__ = value.__doc__ % macros
                    print name, value.__doc__
        #self.lexer = lex.lex(module=self, reflags=re.UNICODE | re.MULTILINE, **kwargs)
        self.lexer = lex.lex(module=self, reflags=re.UNICODE, **kwargs)
        return self.lexer
    
    def iterparse(self, text):
        self.build()
        self.lexer.input(text)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print tok
            yield tok, len(self._stack)
        self._ensure_empty_stack()
    
    def _ensure_empty_stack(self):
        if self._stack:
            raise SyntaxError("missing section end for %s" % ", ".join(self._stack))
        
if __name__ == "__main__":    
    unittest_lexer() # TODO:
    #unittest_parser()