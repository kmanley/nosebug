# TODO: proper unicode handling...
import os
from nosebug_base import BackendBase

class INDENT : pass
class DEDENT : pass

FILE_HEADER = """\
// auto-generated by nosebug (https://github.com/kmanley/nosebug.git)
function get_ctx_value(stack, path) {
    // current context is at stack[stack.length-1]
    var parts = path.split("/");
    var idx = stack.length - 1;
    var curr = stack[idx];
    for (var idx in parts) {
        var part = parts[idx];
        if (part == "..") {
            idx -= 1;
            curr = stack[idx];
        } else {
            curr = curr[part] || "";
        }
    }
    return curr;
}    

function start_section(stack, path) {
    var temp = get_ctx_value(stack, path) || [];
    if (! (temp instanceof Array)) { 
        temp = [temp];
    }
    return temp;
} 

function html_escape(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

"""

# TODO: add an option to use yield instead of res.push, in case we're running in an 
# environment that support yield
class Backend(BackendBase):
    def __init__(self, *args, **kwargs):
        BackendBase.__init__(self, *args, **kwargs)
        self._indent = ""
    
    def get_extension(self):
        return "js"
    
    def get_ctx_value(self, path):
        if "/" in path:
            return "get_ctx_value(stack, %s)" % repr(path)
        else:
            return "stack[stack.length-1][%s] || ''" % repr(path)

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

    def ON_TEMPLATE_START(self, fp, func_name):
        self.write(fp, "function %s(d){" % func_name,
                       "    var res = [];",   
                       "    var stack = [d]", INDENT)
    
    def ON_STRING(self, fp, s, level):
        self.write(fp, "res.push(%s);" % repr(s))
    
    def ON_TAG_SECTION_START(self, fp, path, level):
        self.write(fp, "var l%d = start_section(stack, %s);" % (level, repr(path)),
                       "if (l%d instanceof Object) {" % level,
                       "    stack.push(l%d);" % level,
                       "}",
                       "for (var ill%d in l%d) {" % (level, level),
                       "    var ll%d = l%d[ill%d];" % (level, level, level),
                       "    if (ll%d instanceof Object) {" % level, 
                       "        stack.push(ll%d);" % level, 
                       "    }", INDENT)

    def ON_TAG_INV_SECTION_START(self, fp, path, level):
        pass
    
    def ON_TAG_SECTION_END(self, fp, path, level):
        self.write(fp, "if (ll%d instanceof Object) {" % (level+1),
                       "    stack.pop();", 
                       "}", DEDENT,
                       "}",
                       "if (l%d instanceof Object) {" % (level+1),
                       "    stack.pop();",
                       "}",)
    
    def ON_TAG_PARTIAL(self, fp, name, level):
        self.write(fp, "res.push.apply(res, %s(stack[stack.length-1]))" % name)
    
    def ON_TAG_VAR_UNESCAPED(self, fp, path, level):
        self.write(fp, "res.push((%s).toString());" % self.get_ctx_value(path))
    
    def ON_TAG_VAR_ESCAPED(self, fp, path, level):
        # TODO: actually do the escaping
        self.write(fp, "res.push(html_escape((%s).toString()));" % self.get_ctx_value(path))
    
    def ON_TEMPLATE_END(self, fp, func_name):
        self.write(fp, "return res.join('');", DEDENT, "}");
        pass
    
    def ON_FILE_END(self, fp, file_name):
        pass 
        
    
