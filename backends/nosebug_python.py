# TODO: proper unicode handling...
import os
from nosebug_base import BackendBase

class INDENT : pass
class DEDENT : pass

FILE_HEADER = """\
# auto-generated by nosebug (https://github.com/kmanley/nosebug.git)
import cgi
import StringIO
html_escape = cgi.escape
    
def get_ctx_value(stack, path):
    # current context is at stack[-1]
    print "stack: %s" % repr(stack) # TODO:
    print "path: %s" % repr(path) # TODO:
    parts = path.split("/")
    idx = -1
    curr = stack[idx]
    for part in parts:
        # Note: the parser ensures the path is well-formed
        if part == "..":
            idx -= 1
            curr = stack[idx]
        else:
            curr = curr.get(part)
    return curr

def start_section(stack, path):
    temp = get_ctx_value(stack, path) or []
    if type(temp) not in (list, tuple):
        temp = [temp]
    return temp
 
"""

TEMPLATE_END = """
def %(func_name)s(d): 
    o = StringIO.StringIO()
    for chunk in iter_%(func_name)s(d):
        o.write(chunk)
    return o.getvalue()
"""

class Backend(BackendBase):
    
    def __init__(self, *args, **kwargs):
        BackendBase.__init__(self, *args, **kwargs)
        self._indent = ""
        
    def get_extension(self):
        return "py"

    def write(self, fp, *args):
        for item in args:
            if item == INDENT:
                self._indent += (" " * 4)
            elif item == DEDENT:
                self._indent = self._indent[:-4]
            else:
                fp.write("%s%s\n" % (self._indent, item))
        
    def ON_FILE_START(self, fp, file_name):
        fp.write(FILE_HEADER)

    def ON_TEMPLATE_START(self, fp, file_name):
        func_name = os.path.splitext(os.path.split(file_name)[-1])[0]
        self.write(fp, "def iter_%s(d):" % func_name,  
                       "    stack = [d]", INDENT)
    
    def ON_STRING(self, fp, s, level):
        self.write(fp, "yield %s" % repr(s))
    
    def ON_TAG_SECTION_START(self, fp, path, level):
        self.write(fp, "l%d = start_section(stack, %s)" % (level, repr(path)),
                       "if type(l%d) == dict:" % level,
                       "    stack.append(l%d)" % level,
                       "for ll%d in l%d:" % (level, level),
                       "    if type(ll%d) == dict:" % level, 
                       "        stack.append(ll%d)" % level, INDENT)

    def ON_TAG_INV_SECTION_START(self, fp, path, level):
        pass
    
    def ON_TAG_SECTION_END(self, fp, path, level):
        self.write(fp, "if type(ll%d) == dict:" % (level+1),
                       "    stack.pop()", DEDENT,
                       "if type(l%d) == dict:" % (level+1),
                       "    stack.pop()")
    
    def ON_TAG_PARTIAL(self, fp, name, level):
        pass
    
    def ON_TAG_VAR_UNESCAPED(self, fp, path, level):
        self.write(fp, "yield unicode(get_ctx_value(stack, %s))" % repr(path))
    
    def ON_TAG_VAR_ESCAPED(self, fp, path, level):
        # TODO: actually do the escaping
        self.write(fp, "yield html_escape(unicode(get_ctx_value(stack, %s)))" % repr(path))
    
    def ON_TEMPLATE_END(self, fp, file_name):
        func_name = os.path.splitext(os.path.split(file_name)[-1])[0]
        self.write(fp, TEMPLATE_END % dict(func_name=func_name), DEDENT)
    
    def ON_FILE_END(self, fp, file_name):
        pass 
        
    