"""
This script generates the files debye1_generated.c and debye1_generated.h.
"""

import mpmath
from mpmath import mp


def mp_debye1(x):
    """
    Compute the Debye function D1(x).

    mp.quad is used, so it might be necessary to set mp.dps to a value
    much larger than the desired output precision.  For example, mp.dps=150
    is required to get an accurate double precision result from
    mp_debye1(1e100).
    """
    if x == 0:
        return mp.one

    def integrand(t):
        if t == 0:
            return mp.one
        return t / mp.expm1(t)

    return mp.quad(integrand, [0, x])/x


_preamble = """
// Do not edit this file!
// This file was generated by a script.
"""


def generate_polynomial_function(f, name, coeffs, scale_by_x=False,
                                 comment=None):
    print(f"static double {name}(const double x)", file=f)
    print("{", file=f)
    if comment is not None:
        lines = comment.splitlines()
        for line in lines:
            print(f'    // {line}', file=f)
    print("    const double y = ", end='', file=f)
    nterms = len(coeffs)
    if scale_by_x:
        print("(", end='', file=f)
    for i, mp_coeff in enumerate(coeffs[::-1]):
        coeff = float(mp_coeff)
        print(coeff, end='', file=f)
        if i == nterms - 1:
            print(")"*(nterms - 1), end='', file=f)
            if scale_by_x:
                print(")/x", end='', file=f)
            print(";", file=f)
        else:
            print(" + x*(", end='', file=f)
    print("    return y;", file=f)
    print("}", file=f)


def generate_code(f, intervals):
    mp.dps = 200

    print(_preamble, file=f)
    print(file=f)
    print('#define DEBYE1_ASYMP_CONST 1.6449340668482264  // pi**2/6', file=f)
    print(file=f)
    for i, (a, b, n, order, scale_by_x) in enumerate(intervals):
        edges = mpmath.linspace(a, b, n + 1)
        for k in range(n):
            x0 = edges[k]
            x1 = edges[k+1]
            if scale_by_x:
                poly, err = mp.chebyfit(lambda t: t*mp_debye1(t), [x0, x1],
                                        order, error=True)
                print(f"x0={float(x0):8.4f} x1={float(x1):8.4f} "
                      f"err={float(err/x0):8.3e}")
            else:
                poly, err = mp.chebyfit(lambda t: mp_debye1(t), [x0, x1],
                                        order, error=True)
                print(f"x0={float(x0):8.4f} x1={float(x1):8.4f} "
                      f"err={float(err):8.3e}")
            funcname = f'debye1_{i}_{k:02}'
            comment = f'Approximate debye1 on the interval [{x0}, {x1}].'
            generate_polynomial_function(f, funcname, poly, scale_by_x,
                                         comment=comment)
            print(file=f)

    print('double debye1(const double x)', file=f)
    print('{', file=f)
    print('    if (x < 0) {', file=f)
    print('        return debye1(-x) - x/2;', file=f)
    print('    }', file=f)
    for i, (a, b, n, order, scale_by_x) in enumerate(intervals):
        print(f'    if (x < {b}) {{', file=f)
        print(f'        int k = (int) ({n}*((x - {a})/{b - a}));', file=f)
        print('        switch (k) {', file=f)
        for k in range(n):
            print(f'            case {k:2}: return debye1_{i}_{k:02}(x);',
                  file=f)
        print('        }', file=f)
        print('    }', file=f)
    print(f'    // x >= {b}', file=f)
    print('    return DEBYE1_ASYMP_CONST/x;', file=f)
    print('}', file=f)


if __name__ == "__main__":

    # Each interval in this list will be subdivided into n subintervals,
    # and in each subinterval, an approximation will be generated by
    # mp.chebyfit with the given order.  If scale_by_x is True, chebyfit
    # is applied to mp_debye1(x)*x.
    intervals = [
        #  x0, x1, n, order, scale_by_x
        ( 0.0, 10.0, 50, 8, False),
        (10.0, 20.0, 50, 8, True),
        (20.0, 30.0, 10, 7, True),
        (30.0, 40.0, 10, 4, True),
    ]

    fnamebase = 'debye1_generated'
    print(f'Generating {fnamebase}.c')
    with open(fnamebase + '.c', 'w') as f:
        generate_code(f, intervals)
    print(f'Generating {fnamebase}.h')
    with open(fnamebase + '.h', 'w') as f:
        print(_preamble, file=f)
        print('#ifndef DEBYE1_GENERATED_H', file=f)
        print('#define DEBYE1_GENERATED_H', file=f)
        print(file=f)
        print('double debye1(const double);', file=f)
        print(file=f)
        print('#endif', file=f)
