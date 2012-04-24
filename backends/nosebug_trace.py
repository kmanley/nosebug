import logging
log = logging.getLogger()

class Backend(object):
    def get_extension(self):
        return "trace"
    
    def write(self, fp, func, *args, **kwargs):
        msg = "%s(%s, %s)" % (func, repr(args), repr(kwargs))
        log.info(msg)
        fp.write(msg + "\n")
        
    def ON_FILE_START(self, fp, *args, **kwargs):
        self.write(fp, "ON_FILE_START", *args, **kwargs)
        
    def ON_TEMPLATE_START(self, fp, *args, **kwargs):
        self.write(fp, "ON_TEMPLATE_START", *args, **kwargs)
        
    def ON_STRING(self, fp, *args, **kwargs):
        self.write(fp, "ON_STRING", *args, **kwargs)
    
    def ON_TAG_SECTION_START(self, fp, *args, **kwargs):
        self.write(fp, "ON_TAG_SECTION_START", *args, **kwargs)
    
    def ON_TAG_INV_SECTION_START(self, fp, *args, **kwargs):
        self.write(fp, "ON_TAG_INV_SECTION_START", *args, **kwargs)
    
    def ON_TAG_SECTION_END(self, fp, *args, **kwargs):
        self.write(fp, "ON_TAG_SECTION_END", *args, **kwargs)
    
    def ON_TAG_COMMENT(self, fp, *args, **kwargs):
        self.write(fp, "ON_TAG_COMMENT", *args, **kwargs)
    
    def ON_TAG_PARTIAL(self, fp, *args, **kwargs):
        self.write(fp, "ON_TAG_PARTIAL", *args, **kwargs)
    
    def ON_TAG_VAR_UNESCAPED(self, fp, *args, **kwargs):
        self.write(fp, "ON_TAG_VAR_UNESCAPED", *args, **kwargs)
    
    def ON_TAG_VAR_ESCAPED(self, fp, *args, **kwargs):
        self.write(fp, "ON_TAG_VAR_ESCAPED", *args, **kwargs)
    
    def ON_TEMPLATE_END(self, fp, *args, **kwargs):
        self.write(fp, "ON_TEMPLATE_END", *args, **kwargs)

    def ON_FILE_END(self, fp, *args, **kwargs):
        self.write(fp, "ON_FILE_END", *args, **kwargs)
