"""
TODO: differences with mustache as described in spec here: http://mustache.github.com/mustache.5.html
- no support for triple-mustache {{{name}}}, since the same thing is achievable via {{& name}}
- we support path syntax ../foo/bar for accessing values in context

TODO: add debug logging

"""

import os
import sys
import glob
import template_parser
import argparse
import logging
log = logging.getLogger()

def import_from_string(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def generate(file_list,
             backend_name, 
             single_file=None, 
             output_dir=None,
             delim_start = None,
             delim_end = None):
    """
    backend: string name of backend, e.g. "python"
    file_list: list of template files to process
    single_file: if None, generate a file for each template.
                 Otherwise, generate all functions into named file
    output_dir: directory for output files 
    """
    
    if type(file_list) in (str, unicode):
        file_list = [file_list]
    
    parser = template_parser.NosebugParser(delim_start=delim_start, delim_end=delim_end)
    
    module_name = "backends.nosebug_%s" % backend_name
    log.info("loading backend %s" % module_name)
    mod = import_from_string(module_name)
    backend = getattr(mod, "Backend")()
    
    if single_file:
        if output_dir:
            outfile_name = os.path.join(output_dir, single_file)
        else:
            outfile_name = single_file
        outfile = open(outfile_name, "wb")
        backend.ON_FILE_START(outfile, outfile_name)
        
    for file_name in file_list:
        with open(file_name) as infile:
            if not single_file:
                if not output_dir:
                    output_dir = os.path.dirname(os.path.abspath(file_name))
                outfile_name = os.path.join(output_dir, "%s.%s" % (os.path.splitext(os.path.split(file_name)[-1])[0], backend.get_extension()))
                outfile = open(outfile_name, "wb")
                backend.ON_FILE_START(outfile, outfile_name) 

            backend.ON_TEMPLATE_START(outfile, file_name)
            
            for tok, level in parser.iterparse(infile.read()):
                getattr(backend, "ON_%s" % tok.type)(outfile, tok.value, level)

            backend.ON_TEMPLATE_END(outfile, file_name)
            
            if not single_file:
                backend.ON_FILE_END(outfile, outfile_name)
                log.info("wrote %s" % outfile_name)
                outfile.close()
        
    if single_file:
        backend.ON_FILE_END(outfile, outfile_name)
        log.info("wrote %s" % outfile_name)
        outfile.close()

#def unittest():
#    generate("trace", [r"c:\data\personal\code\nosebug\test\test.txt",
#                       r"c:\data\personal\code\nosebug\test\test2.txt"],
#             single_file="monkey.trace")


def main():
    logging.basicConfig()
    log.setLevel(logging.INFO)
    
    parser = argparse.ArgumentParser(description='compile mustache templates into native language functions')
    parser.add_argument('filespec', type=str, help='template filename or glob pattern')
    parser.add_argument('backend', type=str, help='backend to use (e.g. python)')
    parser.add_argument('--single-file', type=str, help='name of single output file to use for all generated functions')
    parser.add_argument('--output-dir', type=str, help='output directory for generated files')
    parser.add_argument('--delim-start', type=str, help='tag start delimiter override (default {{)')
    parser.add_argument('--delim-end', type=str, help='tag end delimiter override (default }})')
    parser.add_argument('--verbose', action="store_true", help='verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        log.setLevel(logging.DEBUG)
    
    generate(glob.glob(args.filespec), args.backend, args.single_file, args.output_dir, args.delim_start, args.delim_end)

if __name__ == "__main__":
    main()