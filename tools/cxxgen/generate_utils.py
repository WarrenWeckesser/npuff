from os import path


# TODO: Complete these dictionaries

typechar_to_ctype = dict(
    f='float',
    d='double',
    g='long double',
)

typechar_to_npy_type = dict(
    f='NPY_FLOAT',
    d='NPY_DOUBLE',
    g='NPY_LONGDOUBLE',
)


def typesig_to_ext(typesig):
    """
    typesig must be a ufunc type signature, e.g. 'fff->f'.
    This function just replaces '->' with '_'.  So for input
    'fff->f', the return value is 'fff_f'.
    """
    return typesig.replace('->', '_')


def header_to_concrete_filenames(header):
    root, ext = path.splitext(header)
    ext = ext.lstrip(path.extsep)
    if ext not in ['h', 'hh', 'hpp', 'h++']:
        raise RuntimeError("unexpectd file extension for header "
                           f"file '{header}'")

    root_concrete = root + '_concrete'
    cxxfilename = root_concrete + path.extsep + 'cxx'
    cxxheader = root_concrete + path.extsep + 'h'
    return cxxheader, cxxfilename