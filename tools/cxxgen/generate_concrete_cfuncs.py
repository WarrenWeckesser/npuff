
import os
from os import path

from generate_utils import (typechar_to_ctype, typesig_to_ext,
                            header_to_concrete_filenames)


_concrete_preamble = """
// Do not edit this file!
// This file was generated automatically.
// It contains the{header_qualifier} concrete instantiations of the
// templated functions in {header}.
// These are the functions that will be called in the ufunc loops.

#ifndef GENERATED_{HEADER}_H_
#define GENERATED_{HEADER}_H_

#include "../{header}"

extern "C" {{
"""


def generate_concrete_cfuncs(cxxgenpath, header, funcs, destdir):
    """
    Generate C++ files that contain functions that are the C implementations
    of the templated functions in the file `header`.  These are the functions
    that will be called from within the ufunc loops generated in the extension
    module.

    `funcs` must be a sequence of `ufunc_config_types.Func` objects
    (see ufunclab/tools/cxxgen/ufunc_config_types.py).

    The output files are written to the directory `destdir`.
    """
    # Generate filenames for the concrete instantiations, e.g. if header is
    # 'foo.h', cxxheader will be 'foo_concrete.h' and cxxfilename will be
    # 'foo_concrete.cxx'.
    cxxheader, cxxfilename = header_to_concrete_filenames(header)

    # gendir = path.join(cxxgenpath, 'generated')
    # if not path.exists(gendir):
    #     os.mkdir(gendir)
    cxxheader_fullpath = path.join(destdir, cxxheader)
    cxxfilename_fullpath = path.join(destdir, cxxfilename)

    for filename in [cxxfilename_fullpath, cxxheader_fullpath]:
        if filename.endswith('.h'):
            header_qualifier = ' function prototypes for the'
        else:
            header_qualifier = ''
        with open(filename, 'w') as f:
            header_upper = header.split('.')[0].upper()
            print(_concrete_preamble.format(header=header,
                                            header_qualifier=header_qualifier,
                                            HEADER=header_upper),
                  file=f)
            for func in funcs:
                for typesig in func.types:
                    in_types, out_type = typesig.split('->')
                    assert len(out_type) == 1
                    in_ctypes = [typechar_to_ctype[c] for c in in_types]
                    out_ctype = typechar_to_ctype[out_type]
                    funcname_ext = typesig_to_ext(typesig)
                    argnames = [f'x{k}' for k in range(len(in_types))]
                    print(f'{out_ctype}', file=f)
                    print(f'{func.ufuncname}_{funcname_ext}(', end='', file=f)
                    pairs = zip(in_ctypes, argnames)
                    print(', '.join([f'{ctype} {argname}'
                                     for ctype, argname in pairs]),
                          end='', file=f)
                    print(')', end='', file=f)
                    if filename.endswith('.h'):
                        print(';', file=f)
                    else:
                        print(file=f)
                        print('{', file=f)
                        argstr = ", ".join(argnames)
                        print(f'    return {func.cxxname}({argstr});',
                              file=f)
                        print('}', file=f)
                    print(file=f)
            print('}  // extern "C"', file=f)
            print(file=f)
            print('#endif', file=f)
