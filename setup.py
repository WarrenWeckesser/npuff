import sys
import os
from os.path import join


def get_version():
    """
    Find the value assigned to __version__ in ufunclab/__init__.py.

    This function assumes that there is a line of the form

        __version__ = "version-string"

    in __init__.py.  It returns the string version-string, or None if such a
    line is not found.
    """
    with open(join("ufunclab", "__init__.py"), "r") as f:
        for line in f:
            s = [w.strip() for w in line.split("=", 1)]
            if len(s) == 2 and s[0] == "__version__":
                return s[1][1:-1]


def generate_ufunkify_code():
    import subprocess

    cwd = os.getcwd()
    os.chdir(join(cwd, 'src', 'ufunkify'))
    subprocess.run([sys.executable, '_generate_files.py'])
    os.chdir(cwd)


def generate_cxxgen_code(dirnames):
    import subprocess

    cwd = os.getcwd()
    os.chdir(join(cwd, 'tools', 'cxxgen'))

    for dirname in dirnames:
        srcpath = join(cwd, 'src', dirname)
        cmd = [sys.executable, 'generate_ufuncs.py', srcpath]
        subprocess.run(cmd)

    os.chdir(cwd)


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_info

    compile_args = ['-std=c99', '-Werror']
    config = Configuration(None, parent_package, top_path)
    config.add_subpackage('ufunclab')
    config.add_subpackage('ufunclab/tests')
    config.add_extension('ufunclab._logfact',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'logfactorial',
                                       'logfactorial.c'),
                                  join('src', 'logfactorial',
                                       'logfactorial_ufunc.c')])
    config.add_extension('ufunclab._issnan',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'issnan',
                                       'issnan_ufunc.c.src')])
    config.add_extension('ufunclab._expint1',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'expint1',
                                       'expint1_ufunc.c.src')])

    _le_srcs = ['log_expit_concrete.cxx', '_log_expitmodule.cxx']
    config.add_extension('ufunclab._log_expit',
                         extra_compile_args=['-std=c++11', '-Werror'],
                         sources=[join('src', 'log_expit', 'generated', name)
                                  for name in _le_srcs])

    _yj_srcs = ['yeo_johnson_concrete.cxx', '_yeo_johnsonmodule.cxx']
    config.add_extension('ufunclab._yeo_johnson',
                         extra_compile_args=['-std=c++11', '-Werror'],
                         sources=[join('src', 'yeo_johnson', 'generated', name)
                                  for name in _yj_srcs])

    config.add_extension('ufunclab._cross',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'cross',
                                       'cross_gufunc.c.src')],
                         include_dirs=[join('src', 'util')])
    config.add_extension('ufunclab._peaktopeak',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'peaktopeak',
                                       'peaktopeak_gufunc.c.src')],
                         include_dirs=[join('src', 'util')])
    config.add_extension('ufunclab._first',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'first',
                                       'first_gufunc.c.src')],
                         include_dirs=[join('src', 'util')])
    config.add_extension('ufunclab._searchsorted',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'searchsorted',
                                       'searchsorted_gufunc.c.src')],
                         **get_info("npymath"))
    config.add_extension('ufunclab._minmax',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'minmax',
                                       'minmax_gufunc.c.src')],
                         include_dirs=[join('src', 'util')])
    config.add_extension('ufunclab._means',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'means', 'means_gufunc.c.src')],
                         include_dirs=[join('src', 'util')])
    config.add_extension('ufunclab._meanvar',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'meanvar',
                                       'meanvar_gufunc.c.src')],
                         include_dirs=[join('src', 'util')])
    config.add_extension('ufunclab._mad',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'mad', 'mad_gufunc.c.src')])
    config.add_extension('ufunclab._vnorm',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'vnorm',
                                       'vnorm_gufunc.c.src')],
                         include_dirs=[join('src', 'util')])
    config.add_extension('ufunclab._backlash',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'backlash',
                                       'backlash_gufunc.c.src')],
                         include_dirs=[join('src', 'util')])

    _dz_srcs = ['deadzone_concrete.cxx', '_deadzonemodule.cxx']
    config.add_extension('ufunclab._deadzone',
                         extra_compile_args=['-std=c++11', '-Werror'],
                         sources=[join('src', 'deadzone', 'generated', name)
                                  for name in _dz_srcs])

    _tp_srcs = ['trapezoid_pulse_concrete.cxx', '_trapezoid_pulsemodule.cxx']
    config.add_extension('ufunclab._trapezoid_pulse',
                         extra_compile_args=['-std=c++11', '-Werror'],
                         sources=[join('src', 'trapezoid_pulse', 'generated', name)
                                  for name in _tp_srcs])

    config.add_extension('ufunclab._hysteresis_relay',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'hysteresis_relay',
                                       'hysteresis_relay_gufunc.c.src')],
                         include_dirs=[join('src', 'util')])
    config.add_extension('ufunclab._all_same',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'all_same',
                                       'all_same_gufunc.c.src')],
                         include_dirs=[join('src', 'util')])

    _step_srcs = ['step_funcs_concrete.cxx', '_stepmodule.cxx']
    config.add_extension('ufunclab._step',
                         extra_compile_args=['-std=c++11', '-Werror'],
                         sources=[join('src', 'step', 'generated', name)
                                  for name in _step_srcs])

    config.add_extension('ufunclab._gendot',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'gendot',
                                       'gendotmodule.c')])
    config.add_extension('ufunclab._ufunc_inspector',
                         extra_compile_args=compile_args,
                         sources=[join('src', 'ufunc-inspector',
                                       'ufunc_inspector.c')])
    config.add_extension('ufunclab._ufunkify',
                         extra_compile_args=['-std=c99'],
                         sources=[join('src', 'ufunkify',
                                       '_ufunkify_opcodes.c'),
                                  join('src', 'ufunkify',
                                       '_ufunkify_c_function_wrappers.c'),
                                  join('src', 'ufunkify', '_ufunkify.c')])
    return config


if __name__ == "__main__":
    from numpy.distutils.core import setup

    # This is probably *not* the best way to do this...
    generate_ufunkify_code()

    generate_cxxgen_code(['deadzone', 'log_expit', 'yeo_johnson', 'step',
                          'trapezoid_pulse'])

    setup(name='ufunclab',
          version=get_version(),
          configuration=configuration)
