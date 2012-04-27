class BackendBase(object):
    def get_extension(self):
        raise NotImplementedError()
        
    def ON_FILE_START(self, fp, file_name):
        pass
        
    def ON_TEMPLATE_START(self, fp, func_name):
        pass
        
    def ON_STRING(self, fp, path, level):
        raise NotImplementedError()
    
    def ON_TAG_SECTION_START(self, fp, path, level):
        raise NotImplementedError()
    
    def ON_TAG_INV_SECTION_START(self, fp, path, level):
        raise NotImplementedError()
    
    def ON_TAG_SECTION_END(self, fp, path, level):
        raise NotImplementedError()
    
    def ON_TAG_COMMENT(self, fp, comment, level):
        pass
    
    def ON_TAG_PARTIAL(self, fp, name, level):
        raise NotImplementedError()
    
    def ON_TAG_VAR_UNESCAPED(self, fp, path, level):
        raise NotImplementedError()
    
    def ON_TAG_VAR_ESCAPED(self, fp, path, level):
        raise NotImplementedError()
    
    def ON_TEMPLATE_END(self, fp, func_name):
        pass

    def ON_FILE_END(self, fp, file_name):
        pass