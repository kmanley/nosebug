import os
import sys
sys.path.append("..\\..")
import nosebug
import argparse
import logging
log = logging.getLogger()

def run(test_name):
    
    generated_module = "%s_generated" % test_name
    generated_file = "%s.py" % generated_module
    
    try:
        os.unlink(generated_file)
    except:
        pass
    else:
        log.info("deleted old generated file %s" % generated_file)

    actual_file = "%s_actual.txt" % test_name
    expected_file = "%s_expected.txt" % test_name
    
    try:
        os.unlink(actual_file)
    except:
        pass
    else:
        log.info("deleted old test result file %s" % actual_file)
    
    input_files = ["%s.mustache" % test_name]
    
    # see if any partials are used by this test
    partial_file = "%s_partial.mustache" % test_name 
    if os.path.exists(partial_file):
        input_files.append(partial_file)

    log.info("generating %s" % generated_file)    
    nosebug.generate(input_files, "python", generated_file)
    
    func_mod = __import__(generated_module)
    func = getattr(func_mod, test_name)
    
    ctx_mod = __import__("%s_context" % test_name)
    ctx = getattr(ctx_mod, "ctx")
    
    with open(expected_file, "rb") as fp:
        expected = fp.read()
        
    actual = func(ctx)
    
    with open(actual_file, "wb") as fp:
        fp.write(actual)
    
    if actual == expected:
        log.info("PASS")
    else:
        log.error("ERROR (differences found)")
        os.system("tortoisemerge %s %s" % (actual_file, expected_file))

def main():
    logging.basicConfig()
    log.setLevel(logging.INFO)
    
    parser = argparse.ArgumentParser(description='run a nosebug test')
    parser.add_argument('test_name', type=str, help="test name, e.g. 'partial_template'")
    parser.add_argument('--verbose', action="store_true", help='verbose logging')
    
    args = parser.parse_args()
    if args.verbose:
        log.setLevel(logging.DEBUG)
    
    run(args.test_name)

if __name__ == "__main__":
    main()