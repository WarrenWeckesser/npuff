ufunclab
========

Some NumPy `ufuncs`, and some related tools.

The test suite is run with Python versions 3.8 to 3.11, with several
recent releases of NumPy, and with the NumPy main development branch.
`ufunclab` might work with older Python and NumPy versions, but they
are not regularly tested.

To build `ufunclab`, a C99-compatible C compiler and a C++11-compatible C++ compiler
are required.

The unit tests require [pytest](https://docs.pytest.org/).

Links to reference material related to NumPy's C API for ufuncs
and gufuncs are given [below](#resources).

What's in ufunclab?
-------------------

*Element-wise ufuncs*

Most of the element-wise ufuncs are implemented by writing the core
calculation as a templated C++ function, and using some Python code to
automate the generation of all the necessary boilerplate and wrappers
that implement a ufunc around the core calculation.  The exceptions
are `logfactorial`, `issnan`, and `cabssq`, which are implemented in C,
with all boilerplate code written "by hand" in the C file.

| Function                                      | Description                                                   |
| --------                                      | -----------                                                   |
| [`logfactorial`](#logfactorial)               | Log of the factorial of integers                              |
| [`issnan`](#issnan)                           | Like `isnan`, but for signaling nans only.                    |
| [`next_less`](#next_less)                     | Equivalent to `np.nextafter(x, -inf)`                         |
| [`next_greater`](#next_greater)               | Equivalent to `np.nextafter(x, inf)`                          |
| [`abs_squared`](#abs_squared)                 | Squared absolute value                                        |
| [`cabssq`](#cabssq)                           | Squared absolute value for complex input only                 |
| [`deadzone`](#deadzone)                       | Deadzone function                                             |
| [`step`](#step)                               | Step function                                                 |
| [`linearstep`](#linearstep)                   | Piecewise linear step function                                |
| [`smoothstep3`](#smoothstep3)                 | Smooth step using a cubic polynomial                          |
| [`invsmoothstep3`](#invsmoothstep3)           | Inverse of `smoothstep3`                                      |
| [`smoothstep5`](#smoothstep5)                 | Smooth step using a degree 5 polynomial                       |
| [`trapezoid_pulse`](#trapezoid_pulse)         | Trapezoid pulse function                                      |
| [`expint1`](#expint1)                         | Exponential integral E₁ for real inputs                       |
| [`logexpint1`](#logexpint1)                   | Logarithm of the exponential integral E₁                      |
| [`logistic`](#logistic)                       | The standard logistic sigmoid function                        |
| [`logistic_deriv`](#logistic_deriv)           | Derivative of the standard logistic sigmoid function          |
| [`log_logistic`](#log_logistic)               | Logarithm of the standard logistic sigmoid function           |
| [`swish`](#swish)                             | The 'swish' function--a smoothed ramp                         |
| [`hyperbolic_ramp`](#hyperbolic_ramp)         | A smoothed ramp whose graph is a hyperbola                    |
| [`exponential_ramp`](#exponential_ramp)       | A smoothed ramp with exponential convergence to asymptotes    |
| [`yeo_johnson`](#yeo_johnson)                 | Yeo-Johnson transformation                                    |
| [`inv_yeo_johnson`](#inv_yeo_johnson)         | Inverse of the Yeo-Johnson transformation                     |
| [`erfcx`](#erfcx)                             | Scaled complementary error function                           |
| [`normal_cdf`](#normal_cdf)                   | CDF of the standard normal distribution                       |
| [`normal_logcdf`](#normal_logcdf)             | Logarithm of the CDF of the std. normal distribution          |
| [`normal_sf`](#normal_sf)                     | Survival function of the std. normal distribution             |
| [`normal_logsf`](#normal_logsf)               | Log of the survival function of the std. normal distribution  |
| [`semivar_exponential`](#semivar_exponential) | Exponential semivariogram (from kriging interpolation)        |
| [`semivar_linear`](#semivar_linear)           | Linear variogram (from kriging interpolation)                 |
| [`semivar_spherical`](#semivar_spherical)     | Spherical variogram (from kriging interpolation)              |

*Generalized ufuncs*

Note, for anyone looking at the source code: some of these implementations
are in C and use NumPy templating (look for filenames that end in `.src`);
others use templated C++ functions combined with code generation tools
that can be found in `tools/cxxgen`.

| Function                                      | Description                                           |
| --------                                      | -----------                                           |
| [`first`](#first)                             | First value that matches a target comparison          |
| [`argfirst`](#argfirst)                       | Index of the first occurrence of a target comparison  |
| [`argmin`](#argmin)                           | Like `numpy.argmin`, but a gufunc                     |
| [`argmax`](#argmax)                           | Like `numpy.argmax`, but a gufunc                     |
| [`minmax`](#minmax)                           | Minimum and maximum                                   |
| [`argminmax`](#argminmax)                     | Indices of the min and the max                        |
| [`min_argmin`](#min_argmin)                   | Minimum value and its index                           |
| [`max_argmax`](#max_argmax)                   | Maximum value and its index                           |
| [`searchsortedl`](#searchsortedl)             | Find position for given element in sorted seq.        |
| [`searchsortedr`](#searchsortedr)             | Find position for given element in sorted seq.        |
| [`peaktopeak`](#peaktopeak)                   | Alternative to `numpy.ptp`                            |
| [`all_same`](#all_same)                       | Check all values are the same                         |
| [`gmean`](#gmean)                             | Geometric mean                                        |
| [`hmean`](#hmean)                             | Harmonic mean                                         |
| [`meanvar`](#meanvar)                         | Mean and variance                                     |
| [`mad`](#mad)                                 | Mean absolute difference (MAD)                        |
| [`rmad`](#rmad)                               | Relative mean absolute difference (RMAD)              |
| [`gini`](#gini)                               | Gini coefficient                                      |
| [`rms`](#rms)                                 | Root-mean-square for real and complex inputs          |
| [`vnorm`](#vnorm)                             | Vector norm                                           |
| [`vdot`](#vdot)                               | Vector dot product for real floating point arrays     |
| [`pearson_corr`](#pearson_corr)               | Pearson's product-moment correlation coefficient      |
| [`cross2`](#cross2)                           | 2-d vector cross product (returns scalar)             |
| [`cross3`](#cross3)                           | 3-d vector cross product                              |
| [`tri_area`](#tri_area)                       | Area of triangles in n-dimensional space              |
| [`fillnan1d`](#fillnan1d)                     | Replace `nan` using linear interpolation              |
| [`backlash`](#backlash)                       | Backlash operator                                     |
| [`hysteresis_relay`](#hysteresis_relay)       | Relay with hysteresis (Schmitt trigger)               |
| [`sosfilter`](#sosfilter)                     | SOS (second order sections) linear filter             |
| [`sosfilter_ic`](#sosfilter_ic)               | SOS linear filter with initial condition              |
| [`sosfilter_ic_contig`](#sosfilter_ic_contig) | SOS linear filter with contiguous array inputs        |

*Other tools*

| Function                                | Description                                           |
| --------                                | -----------                                           |
| [`gendot`](#gendot)                     | Create a new gufunc that composes two ufuncs          |
| [`ufunc_inspector`](#ufunc_inspector)   | Display ufunc information                             |

-----

### `logfactorial`

`logfactorial` is a ufunc that computes the natural logarithm of the
factorial of the nonnegative integer x.  (`nan` is returned for negative
input.)

For example,
```
>>> from ufunclab import logfactorial

>>> logfactorial([1, 10, 100, 1000])
array([   0.        ,   15.10441257,  363.73937556, 5912.12817849])
```

### `issnan`

`issnan` is an element-wise ufunc with a single input that acts like
the standard `isnan` function, but it returns True only for
[*signaling* nans](https://en.wikipedia.org/wiki/NaN#Signaling_NaN).

The current implementation only handles the floating point types `np.float16`,
`np.float32` and `np.float64`.

```
>>> import numpy as np
>>> from ufunclab import issnan
>>> x = np.array([12.5, 0.0, np.inf, 999.0, np.nan], dtype=np.float32)
```
Put a signaling nan in `x[1]`. (The nan in `x[4]` is a quiet nan, and
we'll leave it that way.)
```
>>> v = x.view(np.uint32)
>>> v[1] = 0b0111_1111_1000_0000_0000_0000_0000_0011
>>> x
array([ 12.5,   nan,   inf, 999. ,   nan], dtype=float32)
>>> np.isnan(x)
array([False,  True, False, False,  True])
```
Note that NumPy displays both quiet and signaling nans as just `nan`,
and `np.isnan(x)` returns True for both quiet and signaling nans (as
it should).

`issnan(x)` indicates which values are signaling nans:
```
>>> issnan(x)
array([False,  True, False, False, False])
```

### `next_less`

`next_less` is an element-wise ufunc with a single input that
is equivalent to `np.nextafter` with the second argument set to `-inf`.

```
>>> import numpy as np
>>> from ufunclab import next_less
>>> next_less(np.array([-12.5, 0, 1, 1000], dtype=np.float32))
array([-1.2500001e+01, -1.4012985e-45,  9.9999994e-01,  9.9999994e+02],
      dtype=float32)
```

### `next_greater`

`next_greater` is an element-wise ufunc with a single input that
is equivalent to `np.nextafter` with the second argument set to `inf`.

```
>>> import numpy as np
>>> from ufunclab import next_greater
>>> next_greater(np.array([-12.5, 0, 1, 1000], dtype=np.float32))
array([-1.24999990e+01,  1.40129846e-45,  1.00000012e+00,  1.00000006e+03],
      dtype=float32)
```

### `abs_squared`

`abs_squared(z)` computes the squared absolute value of `z`.
This is an element-wise ufunc with types `'f->f'`, `'d->d'`,
`'g->g'`, `'F->f'`, `'D->d'`, and `'G->g'`.  For real input,
the result is just `z**2`.  For complex input, it is
`z.real**2 + z.imag**2`.

```
>>> import numpy as np
>>> from ufunclab import abs_squared

>>> abs_squared.types
['f->f', 'd->d', 'g->g', 'F->f', 'D->d', 'G->g']

>>> x = np.array([-1.5, 3.0, 9.0, -10.0], dtype=np.float32)
>>> abs_squared(x)
array([  2.25,   9.  ,  81.  , 100.  ], dtype=float32)

>>> z = np.array([-3+4j, -1, 1j, 13, 0.5-1.5j])
>>> abs_squared(z)
array([ 25. ,   1. ,   1. , 169. ,   2.5])
```

### `cabssq`

`cabssq(z)` computes the squared absolute value of `z` for complex input only.
This is the same calculation as `abs_squared`, but the implementation is
different.  `cabssq` is implemented in C with the inner loop functions
implemented "by hand", with no C++ or NumPy templating.  `cabssq` is generally
faster than `abs_squared`, because it avoids some of the overhead that occurs
in the code generated in the implementation of `abs_squared`, and it allows
the compiler to optimize the code more effectively.

### `deadzone`

`deadzone(x, low, high)` is a ufunc with three inputs and one output.
It computes the "deadzone" response of a signal:

           { 0         if low <= x <= high
    f(x) = { x - low   if x < low
           { x - high  if x > high

The function is similar to the
[deadzone block](https://www.mathworks.com/help/simulink/slref/deadzone.html)
of Matlab's Simulink library.  The function is also known as
a *soft threshold*.

Here's a plot of `deadzone(x, -0.25, 0.5)`:

![Deadzone plot1](https://github.com/WarrenWeckesser/ufunclab/blob/main/examples/deadzone_demo1.png)

The script `deadzone_demo2.py` in the `examples` directory generates
the plot

![Deadzone plot2](https://github.com/WarrenWeckesser/ufunclab/blob/main/examples/deadzone_demo2.png)

### `step`

The ufunc `step(x, a, flow, fa, fhigh)` returns `flow` for
`x < a`, `fhigh` for `x > a`, and `fa` for `x = a`.

The Heaviside function can be implemented as `step(x, 0, 0, 0.5, 1)`.

The script `step_demo.py` in the `examples` directory generates
the plot

![step plot](https://github.com/WarrenWeckesser/ufunclab/blob/main/examples/step_demo.png)


### `linearstep`

The ufunc `linearstep(x, a, b, fa, fb)` returns `fa` for
`x <= a`, `fb` for `x >= b`, and uses linear interpolation
from `fa` to `fb` in the interval `a < x < b`.

The script `linearstep_demo.py` in the `examples` directory generates
the plot

![linearstep plot](https://github.com/WarrenWeckesser/ufunclab/blob/main/examples/linearstep_demo.png)

### `smoothstep3`

The ufunc `smoothstep3(x, a, b, fa, fb)` returns `fa` for
`x <= a`, `fb` for `x >= b`, and uses a cubic polynomial in
the interval `a < x < b` to smoothly transition from `fa` to `fb`.

The script `smoothstep3_demo.py` in the `examples` directory generates
the plot

![smoothstep3 plot](https://github.com/WarrenWeckesser/ufunclab/blob/main/examples/smoothstep3_demo.png)

### `invsmoothstep3`

The ufunc `invsmoothstep3(y, a, b, fa, fb)` is the inverse of
`smoothstep3(x, a, b, fa, fb)`.

The script `invsmoothstep3_demo.py` in the `examples` directory generates
the plot

![invsmoothstep3 plot](https://github.com/WarrenWeckesser/ufunclab/blob/main/examples/invsmoothstep3_demo.png)


### `smoothstep5`

The function `smoothstep5(x, a, b, fa, fb)` returns `fa` for
`x <= a`, `fb` for `x >= b`, and uses a degree 5 polynomial in
the interval `a < x < b` to smoothly transition from `fa` to `fb`.

The script `smoothstep5_demo.py` in the `examples` directory generates
the plot

![smoothstep5 plot](https://github.com/WarrenWeckesser/ufunclab/blob/main/examples/smoothstep5_demo.png)

### `trapezoid_pulse`

`trapezoid_pulse(x, a, b, c, d, amp)` is a ufunc that computes
a trapezoid pulse.  The function is 0 for `x` <= `a` or `x` >= `d`,
`amp` for `b` <= `x` <= `c`, and a linear ramp in the intervals
`[a, b]` and `[c, d]`.

Here's a plot of `trapezoid_pulse(x, 1, 3, 4, 5, 2)` (generated by
the script `trapezoid_pulse_demo.py` in the `examples` directory):

![trapezoid_pulse plot1](https://github.com/WarrenWeckesser/ufunclab/blob/main/examples/trapezoid_pulse_demo.png)


### `expint1`

`expint1(x)` computes the exponential integral E₁ for the real input x.

```
>>> from ufunclab import expint1
>>> expint1([0.25, 2.5, 25])
array([1.04428263e+00, 2.49149179e-02, 5.34889976e-13])
```

### `logexpint1`

`logexpint1(x)` computes the logarithm of the exponential integral E₁ for the real input x.

`expint1(x)` underflows to 0 for sufficiently large x:

```
>>> from ufunclab import expint1, logexpint1
>>> expint1([650, 700, 750, 800])
array([7.85247922e-286, 1.40651877e-307, 0.00000000e+000, 0.00000000e+000])
```

`logexpint1` avoids the underflow by computing the logarithm of the value:

```
>>> logexpint1([650, 700, 750, 800])
array([-656.47850729, -706.55250586, -756.62140388, -806.68585939])
```


### `logistic`

`logistic(x)` computes the standard logistic sigmoid function.

The script `logistic_demo.py` in the `examples` directory generates
this plot:

![logistic plot](https://github.com/WarrenWeckesser/ufunclab/blob/main/examples/logistic_demo.png)


### `logistic_deriv`

`logistic_deriv(x)` computes the derivative of the standard logistic sigmoid
function.

See `logistic` (above) for a plot.


### `log_logistic`

`log_logistic(x)` computes the logarithm of the standard logistic sigmoid
function.

```
>>> import numpy as np
>>> from ufunclab import log_logistic

>>> x = np.array([-800, -500, -0.5, 10, 250, 500])
>>> log_logistic(x)
array([-8.00000000e+002, -5.00000000e+002, -9.74076984e-001,
       -4.53988992e-005, -2.66919022e-109, -7.12457641e-218])
```

Compare that to the output of `log(expit(x))`, which triggers a warning
and loses all precision for inputs with large magnitudes:

```
>>> from scipy.special import expit
>>> np.log(expit(x))
<stdin>:1: RuntimeWarning: divide by zero encountered in log
array([           -inf, -5.00000000e+02, -9.74076984e-01,
       -4.53988992e-05,  0.00000000e+00,  0.00000000e+00])
```


### `swish`

`swish(x, beta)` computes `x * logistic(beta*x)`, where `logistic(x)`
is the standard logistic sigmoid function.  The function is a type
of smoothed ramp.

![swish plot](https://github.com/WarrenWeckesser/ufunclab/blob/main/examples/swish_demo.png)


### `hyperbolic_ramp`

`hyperbolic_ramp(x, a)` computes the function

    hyperbolic_ramp(x, a) = (x + sqrt(x*x + 4*a*a))/2

It is a smoothed ramp function.  The scaling of the parameters is chosen
so that `hyperbolic_ramp(0, a)` is `a`.

![hyperbolic_ramp plot](https://github.com/WarrenWeckesser/ufunclab/blob/main/examples/hyperbolic_ramp_demo.png)


### `exponential_ramp`

`exponential_ramp(x, a)` computes the function

    exponential_ramp(x, a) = a*log_2(1 + 2**(x/a))

It is a smoothed ramp function that converges exponentially fast to
the asymptotes.  The scaling of the parameters is chosen so that
`exponential_ramp(0, a)` is `a`.

The function is also known as the "softplus" function.

![exponential_ramp plot](https://github.com/WarrenWeckesser/ufunclab/blob/main/examples/exponential_ramp_demo.png)


### `yeo_johnson`

`yeo_johnson` computes the Yeo-Johnson transform.

```
>>> import numpy as np
>>> from ufunclab import yeo_johnson

>>> yeo_johnson([-1.5, -0.5, 2.8, 7, 7.1], 2.3)
array([-0.80114069, -0.38177502,  8.93596922, 51.4905317 , 52.99552905])

>>> yeo_johnson.outer([-1.5, -0.5, 2.8, 7, 7.1], [-2.5, 0.1, 2.3, 3])
array([[-13.50294123,  -2.47514321,  -0.80114069,  -0.6       ],
       [ -1.15561576,  -0.61083954,  -0.38177502,  -0.33333333],
       [  0.38578977,   1.42821388,   8.93596922,  17.95733333],
       [  0.39779029,   2.31144413,  51.4905317 , 170.33333333],
       [  0.39785786,   2.32674755,  52.99552905, 176.81366667]])
```

### `inv_yeo_johnson`

`inv_yeo_johnson` computes the inverse of the Yeo-Johnson transform.

```
>>> import numpy as np
>>> from ufunclab import inv_yeo_johnson, yeo_johnson

>>> x = inv_yeo_johnson([-1.5, -0.5, 2.8, 7, 7.1], 2.5)
>>> x
array([-15.        ,  -0.77777778,   1.29739671,   2.21268904,
         2.22998502])
>>> yeo_johnson(x, 2.5)
array([-1.5, -0.5,  2.8,  7. ,  7.1])
```

### `erfcx`

`erfcx(x)` computes the scaled complementary error function,
`exp(x**2) * erfc(x)`.  The function is implemented for NumPy types
`float32`, `float64` and `longdouble` (also known as `float128`):

```
>>> from ufunclab import erfcx
>>> erfcx.types
['f->f', 'd->d', 'g->g']
```

This example is run on a platform where the `longdouble` type
corresponds to a `float128` with 80 bits of precision:

```
>>> import numpy as np
>>> b = np.longdouble('1.25e2000')
>>> x = np.array([-40, -1.0, 0, 2.5, 3000.0, b])
>>> x
array([-4.00e+0001, -1.00e+0000,  0.00e+0000,  1.00e+0003,  1.25e+2000],
      dtype=float128)
>>> erfcx(x)
array([1.48662366e+0695, 5.00898008e+0000, 1.00000000e+0000,
       5.64189301e-0004, 4.51351667e-2001], dtype=float128)
```

### `normal_cdf`

`normal_cdf(x)` computes the cumulative distribution function of the standard
normal distribution.


### `normal_logcdf`

`normal_logcdf(x)` computes the natural logarithm of the CDF of the standard
normal distribution.


### `normal_sf`

`normal_sf(x)` computes the survival function of the standard normal distribution.
This function is also known as the complementary CDF, and is often abbreviated
as `ccdf`.


### `normal_logsf`

`normal_logsf(x)` computes the natural logarithm of the survival function of the
standard normal distribution.


### `semivar_exponential`

`semivar_exponential(h, nugget, sill, rng)` computes the exponential semivariogram.


### `semivar_linear`

`semivar_linear(h, nugget, sill, rng)` computes the linear semivariogram.


### `semivar_spherical`

`semivar_spherical(h, nugget, sill, rng)` computes the spherical semivariogram.


### `first`

`first` is a gufunc with signature `(i),(),(),()->()` that returns the first
value that matches a given comparison.  The function signature is
`first(x, op, target, otherwise)`, where `op` is one of the values in
`ufunclab.op` that specifies the comparison to be made. `otherwise` is the
value to be returned if no value in `x` satisfies the given relation with
`target`.

Find the first nonzero value in `a`:

```
>>> import numpy as np
>>> from ufunclab import first, op

>>> a = np.array([0, 0, 0, 0, 0, -0.5, 0, 1, 0.1])
>>> first(a, op.NE, 0.0, 0.0)
-0.5
```

Find the first value in each row of `b` that is less than 0.
If there is no such value, return 0:

```
>>> b = np.array([[10, 23, -10, 0, -9],
...               [18, 28, 42, 33, 71],
...               [17, 29, 16, 14, -7]], dtype=np.int8)
...
>>> first(b, op.LT, 0, 0)
array([-10,   0,  -7], dtype=int8)
```

### `argfirst`

`argfirst` is a gufunc (signature `(i),(),()->()`) that finds the index of
the first true value of a comparison of an array with a target value.  If no
value is found, -1 is return.  Some examples follow.

```
>>> import numpy as np
>>> from ufunclab import argfirst, op
```

Find the index of the first occurrence of 0 in `x`:

```
>>> x = np.array([10, 35, 19, 0, -1, 24, 0])
>>> argfirst(x, op.EQ, 0)
3
```

Find the index of the first nonzero value in `a`:

```
>>> a = np.array([0, 0, 0, 0, 0, -0.5, 0, 1, 0.1])
>>> argfirst(a, op.NE, 0.0)
5
```

`argfirst` is a gufunc, so it can handle higher-dimensional
array arguments, and among its gufunc-related parameters is
`axis`.  By default, the gufunc operates along the last axis.
For example, here we find the location of the first nonzero
element in each row of `b`:

```
>>> b = np.array([[0, 8, 0, 0], [0, 0, 0, 0], [0, 0, 9, 2]],
...              dtype=np.uint8)
>>> b
array([[0, 8, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 9, 2]])
>>> argfirst(b, op.NE, np.uint8(0))
array([ 1, -1,  2])
```

If we give the argument `axis=0`, we tell `argfirst` to
operate along the first axis, which in this case is the
columns:

```
>>> argfirst(b, op.NE, np.uint8(0), axis=0)
array([-1,  0,  2,  2])
```

### `argmin`

`argmin` is a `gufunc` with signature `(i)->()` that is similar to `numpy.argmin`.

```
>>> from ufunclab import argmin
>>> x = np.array([[11, 10, 10, 23, 31],
...               [19, 20, 21, 22, 22],
...               [16, 15, 16, 14, 14]])
>>> argmin(x, axis=1)  # same as argmin(x)
array([1, 0, 3])
>>> argmin(x, axis=0)
array([0, 0, 0, 2, 2])
```

### `argmax`

`argmax` is a `gufunc` with signature `(i)->()` that is similar to `numpy.argmax`.

```
>>> from ufunclab import argmax
>>> x = np.array([[11, 10, 10, 23, 31],
...               [19, 20, 21, 22, 22],
...               [16, 15, 16, 14, 14]])
>>> argmax(x, axis=1)  # same as argmax(x)
array([4, 3, 0])
>>> argmax(x, axis=0)
array([1, 1, 1, 0, 0])
```

### `minmax`

`minmax` is a `gufunc` (signature `(i)->(2)`) that simultaneously computes
the minimum and maximum of a NumPy array.

The function handles the standard integer and floating point types, and
object arrays. The function will not accept complex arrays, nor arrays with
the data types `datetime64` or `timedelta64`.  Also, the function does not
implement any special handling of `nan`, so the behavior of this function
with arrays containing `nan` is *undefined*.

For an input with more than one dimension, `minmax` is applied to the
last axis.  For example, if `a` has shape (L, M, N), then `minmax(a)` has
shape (L, M, 2).

```
>>> x = np.array([5, -10, -25, 99, 100, 10], dtype=np.int8)
>>> minmax(x)
array([-25, 100], dtype=int8)

>>> np.random.seed(12345)
>>> y = np.random.randint(-1000, 1000, size=(3, 3, 5)).astype(np.float32)
>>> y
array([[[-518.,  509.,  309., -871.,  444.],
        [ 449., -618.,  381., -454.,  565.],
        [-231.,  142.,  393.,  339., -346.]],

       [[-895.,  115., -241.,  398.,  232.],
        [-118., -287., -733.,  101.,  674.],
        [-919.,  746., -834., -737., -957.]],

       [[-769., -977.,   53.,  -48.,  463.],
        [ 311., -299., -647.,  883., -145.],
        [-964., -424., -613., -236.,  148.]]], dtype=float32)

>>> mm = minmax(y)
>>> mm
array([[[-871.,  509.],
        [-618.,  565.],
        [-346.,  393.]],

       [[-895.,  398.],
        [-733.,  674.],
        [-957.,  746.]],

       [[-977.,  463.],
        [-647.,  883.],
        [-964.,  148.]]], dtype=float32)

>>> mm.shape
(3, 3, 2)

>>> z = np.array(['foo', 'xyz', 'bar', 'abc', 'def'], dtype=object)
>>> minmax(z)
array(['abc', 'xyz'], dtype=object)

>>> from fractions import Fraction
>>> f = np.array([Fraction(1, 3), Fraction(3, 5),
...               Fraction(22, 7), Fraction(5, 2)], dtype=object)
>>> minmax(f)
array([Fraction(1, 3), Fraction(22, 7)], dtype=object)

```

### `argminmax`

`argminmax` is a `gufunc` (signature `(i)->(2)`) that simultaneously
computes the `argmin` and `argmax` of a NumPy array.

```
>>> y = np.array([[-518,  509,  309, -871,  444,  449, -618,  381],
...               [-454,  565, -231,  142,  393,  339, -346, -895],
...               [ 115, -241,  398,  232, -118, -287, -733,  101]],
...              dtype=np.float32)
>>> argminmax(y)
array([[3, 1],
       [7, 1],
       [6, 2]])
>>> argminmax(y, axes=[0, 0])
array([[0, 2, 1, 0, 2, 2, 2, 1],
       [2, 1, 2, 2, 0, 0, 1, 0]])
```

### `min_argmin`

`min_argmin` is a gufunc (signature `(i)->(),()`) that returns both
the extreme value and the index of the extreme value.

```
>>> x = np.array([[ 1, 10, 18, 17, 11],
...               [15, 11,  0,  4,  8],
...               [10, 10, 12, 11, 11]])
>>> min_argmin(x, axis=1)
(array([ 1,  0, 10]), array([0, 2, 0]))
```

### `max_argmax`

`max_argmax` is a gufunc (signature `(i)->(),()`) that returns both
the extreme value and the index of the extreme value.

```
>>> x = np.array([[ 1, 10, 18, 17, 11],
...               [15, 11,  0,  4,  8],
...               [10, 10, 12, 11, 11]])
>>> max_argmax(x, axis=1)
(array([18, 15, 12]), array([2, 0, 2]))

>>> from fractions import Fraction as F
>>> y = np.array([F(2, 3), F(3, 4), F(2, 7), F(2, 5)])
>>> max_argmax(y)
(Fraction(3, 4), 1)
```

### `searchsortedl`

`searchsortedl` is a gufunc with signature `(i),()->()`.  The function
is equivalent to `numpy.searchsorted` with `side='left'`, but as a gufunc,
it supports broadcasting of its arguments.  (Note that `searchsortedl`
does not provide the `sorter` parameter.)

```
>>> import numpy as np
>>> from ufunclab import searchsortedl
>>> searchsortedl([1, 1, 2, 3, 5, 8, 13, 21], [1, 4, 15, 99])
array([0, 4, 7, 8])
>>> arr = np.array([[1, 1, 2, 3, 5, 8, 13, 21],
...                 [1, 1, 1, 1, 2, 2, 10, 10]])
>>> searchsortedl(arr, [7, 8])
array([5, 6])
>>> searchsortedl(arr, [[2], [5]])
array([[2, 4],
       [4, 6]])
```

### `searchsortedr`

`searchsortedr` is a gufunc with signature `(i),()->()`.  The function
is equivalent to `numpy.searchsorted` with `side='right'`, but as a gufunc,
it supports broadcasting of its arguments.  (Note that `searchsortedr`
does not provide the `sorter` parameter.)

```
>>> import numpy as np
>>> from ufunclab import searchsortedr
>>> searchsortedr([1, 1, 2, 3, 5, 8, 13, 21], [1, 4, 15, 99])
array([2, 4, 7, 8])
>>> arr = np.array([[1, 1, 2, 3, 5, 8, 13, 21],
...                 [1, 1, 1, 1, 2, 2, 10, 10]])
>>> searchsortedr(arr, [7, 8])
array([5, 6])
>>> searchsortedr(arr, [[2], [5]])
array([[3, 6],
       [5, 6]])
```


### `peaktopeak`

`peaktopeak` is a `gufunc` (signature `(i)->()`) that computes the
peak-to-peak range of a NumPy array.  It is like the `ptp` method
of a NumPy array, but when the input is signed integers, the output
is an unsigned integer with the same bit width.

The function handles the standard integer and floating point types,
`datetime64`, `timedelta64`, and object arrays. The function does not
accept complex arrays.  Also, the function does not implement any special
handling of `nan`, so the behavior of this function with arrays containing
`nan` is undefined (i.e. it might not do what you want, and the behavior
might change in the next update of the software).

```
>>> x = np.array([85, 125, 0, -75, -50], dtype=np.int8)
>>> p = peaktopeak(x)
>>> p
200
>>> type(p)
numpy.uint8
```

Compare that to the `ptp` method, which returns a value with the
same data type as the input:

```
>>> q = x.ptp()
>>> q
-56
>>> type(q)
numpy.int8

```

`f` is an object array of `Fraction`s and has shape (2, 4).

```
>>> from fractions import Fraction
>>> f = np.array([[Fraction(1, 3), Fraction(3, 5),
...                Fraction(22, 7), Fraction(5, 2)],
...               [Fraction(-2, 9), Fraction(1, 3),
...                Fraction(2, 3), Fraction(5, 9)]], dtype=object)
>>> peaktopeak(x)
array([Fraction(59, 21), Fraction(8, 9)], dtype=object)

```

`dates` is an array of `datetime64`.

```
>>> dates = np.array([np.datetime64('2015-11-02T12:34:50'),
...                   np.datetime64('2016-03-01T16:00:00'),
...                   np.datetime64('2015-07-02T21:20:19'),
...                   np.datetime64('2016-05-01T19:25:00')])

>>> dates
array(['2015-11-02T12:34:50', '2016-03-01T16:00:00',
       '2015-07-02T21:20:19', '2016-05-01T19:25:00'],
      dtype='datetime64[s]')
>>> timespan = peaktopeak(dates)
>>> timespan
numpy.timedelta64(26258681,'s')
>>> timespan / np.timedelta64(1, 'D')  # Convert to number of days.
303.9199189814815
```

Casting works when the `out` argument is an array with dtype `timedelta64`.
For example,

```
>>> out = np.empty((), dtype='timedelta64[D]')
>>> peaktopeak(dates, out=out)
array(303, dtype='timedelta64[D]')

```


### `all_same`

`all_same` is a gufunc (signature `(i)->()`) that tests that all the
values in the array along the given axis are the same.

(Note: handling of `datetime64`, `timedelta64` and complex data types
are not implemented yet.)

```
>>> x = np.array([[3, 2, 2, 3, 2, 2, 3, 1, 3],
...               [1, 2, 2, 2, 2, 2, 3, 1, 1],
...               [2, 3, 3, 1, 2, 3, 3, 1, 2]])

>>> all_same(x, axis=0)
array([False, False, False, False,  True, False,  True,  True, False])

>>> all_same(x, axis=1)
array([False, False, False])
```

Object arrays are handled.

```
>>> a = np.array([[None, "foo", 99], [None, "bar", "abc"]])
>>> a
array([[None, 'foo', 99],
       [None, 'bar', 'abc']], dtype=object)

>>> all_same(a, axis=0)
array([ True, False, False])
```

### `gmean`

`gmean` is a gufunc (signature `(i)->()`) that computes the
[geometric mean](https://en.wikipedia.org/wiki/Geometric_mean).

For example,

```
>>> import numpy as np
>>> from ufunclab import gmean

>>> x = np.array([1, 2, 3, 5, 8], dtype=np.uint8)
>>> gmean(x)
2.992555739477689

>>> y = np.arange(1, 16).reshape(3, 5)
>>> y
array([[ 1,  2,  3,  4,  5],
       [ 6,  7,  8,  9, 10],
       [11, 12, 13, 14, 15]])

>>> gmean(y, axis=1)
array([ 2.60517108,  7.87256685, 12.92252305])
```

### `hmean`

`hmean` is a gufunc (signature `(i)->()`) that computes the
[harmonic mean](https://en.wikipedia.org/wiki/Harmonic_mean).

For example,

```
>>> import numpy as np
>>> from ufunclab import hmean

>>> x = np.array([1, 2, 3, 5, 8], dtype=np.uint8)
>>> hmean(x)
2.316602316602317

>>> y = np.arange(1, 16).reshape(3, 5)
>>> y
array([[ 1,  2,  3,  4,  5],
       [ 6,  7,  8,  9, 10],
       [11, 12, 13, 14, 15]])

>>> hmean(y, axis=1)
array([ 2.18978102,  7.74431469, 12.84486077])
```

### `meanvar`

`meanvar` is a gufunc (signature `(n),()->(2)`) that computes both
the mean and variance in one function call.

For example,

```
>>> import numpy as np
>>> from ufunclab import meanvar

>>> meanvar([1, 2, 4, 5], 0)  # Use ddof=0.
array([3. , 2.5])
```

Apply `meanvar` with `ddof=1` to the rows of a 2-d array.
The output has shape `(4, 2)`; the first column holds the
means, and the second column holds the variances.


```
>>> x = np.array([[1, 4, 4, 2, 1, 1, 2, 7],
...               [0, 0, 9, 4, 1, 0, 0, 1],
...               [8, 3, 3, 3, 3, 3, 3, 3],
...               [5, 5, 5, 5, 5, 5, 5, 5]])

>>> meanvar(x, 1)  # Use ddof=1.
array([[ 2.75 ,  4.5  ],
       [ 1.875, 10.125],
       [ 3.625,  3.125],
       [ 5.   ,  0.   ]])
```

Compare to the results of `numpy.mean` and `numpy.var`:

```
>>> np.mean(x, axis=1)
array([2.75 , 1.875, 3.625, 5.   ])

>>> np.var(x, ddof=1, axis=1)
array([ 4.5  , 10.125,  3.125,  0.   ])
```

### `mad`

`mad(x, unbiased)` computes the [mean absolute difference](https://en.wikipedia.org/wiki/Mean_absolute_difference)
of a 1-d array (gufunc signature is `(n),()->()`).  When the second parameter
is False,  `mad` is the standard calculation (sum of the absolute differences
divided by `n**2`).  When the second parameter is True, `mad` is the unbiased
estimator (sum of the absolute differences divided by `n*(n-1)`).

For example,
```
>>> import numpy as np
>>> from ufunclab import mad

>>> x = np.array([1.0, 1.0, 2.0, 3.0, 5.0, 8.0])

>>> mad(x, False)
2.6666666666666665

>>> y = np.linspace(0, 1, 21).reshape(3, 7)**2
>>> y
array([[0.    , 0.0025, 0.01  , 0.0225, 0.04  , 0.0625, 0.09  ],
       [0.1225, 0.16  , 0.2025, 0.25  , 0.3025, 0.36  , 0.4225],
       [0.49  , 0.5625, 0.64  , 0.7225, 0.81  , 0.9025, 1.    ]])

>>> mad(y, False, axis=1)
array([0.03428571, 0.11428571, 0.19428571])
```

When the second parameter is `True`, the calculation is the unbiased
estimate of the mean absolute difference.

```
>>> mad(x, True)
3.2

>>> mad(y, True, axis=1)
array([0.04      , 0.13333333, 0.22666667])
```

### `rmad`

`rmad(x, unbiased)` computes the relative mean absolute difference (gufunc
signature is `(i),()->()`).

`rmad` is twice the [Gini coefficient](https://en.wikipedia.org/wiki/Gini_coefficient).

For example,

```
>>> import numpy as np
>>> from ufunclab import rmad

>>> x = np.array([1.0, 1.0, 2.0, 3.0, 5.0, 8.0])

>>> rmad(x, False)
0.7999999999999999

>>> y = np.linspace(0, 1, 21).reshape(3, 7)**2
>>> y
array([[0.    , 0.0025, 0.01  , 0.0225, 0.04  , 0.0625, 0.09  ],
       [0.1225, 0.16  , 0.2025, 0.25  , 0.3025, 0.36  , 0.4225],
       [0.49  , 0.5625, 0.64  , 0.7225, 0.81  , 0.9025, 1.    ]])

>>> rmad(y, False, axis=1)
array([1.05494505, 0.43956044, 0.26523647])
```

When the second parameter is `True`, the calculation is based on the
unbiased estimate of the mean absolute difference (MAD).

```
>>> rmad(x, True)
0.96

>>> rmad(y, True, axis=1)
array([1.23076923, 0.51282051, 0.30944255])
```

### `gini`

`gini(x, unbiased)` is a gufunc with signature `(n),()->()` that computes the
Gini coefficient of the data in `x`.

```
>>> from ufunclab import gini

>>> gini([1, 2, 3, 4], False)
0.25

>>> income = [20, 30, 40, 50, 60, 70, 80, 90, 120, 150]
>>> gini(income, False)
0.3028169014084507
```

When the second parameter is `True`, the calculation is based on the
unbiased estimate of the mean absolute difference (MAD).

```
>>> gini([1, 2, 3, 4], True)
0.33333333333333337

>>> income = [20, 30, 40, 50, 60, 70, 80, 90, 120, 150]
>>> gini(income, True)
0.3364632237871674
```

### `rms`

`rms(x)` computes the root-mean-square value for a collection of values.
It is a gufunc with signature `(n)->()`.  The implementation is for
float and complex types; integer types are cast to float.

```
>>> import numpy as np
>>> from ufunclab import rms
>>> x = np.array([1, 2, -1, 0, 3, 2, -1, 0, 1])
>>> rms(x)
1.5275252316519468

Compare to:

>>> np.sqrt(np.mean(x**2))
1.5275252316519468

A complex example:

>>> z = np.array([1-1j, 2+1.5j, -3-2j, 0.5+1j, 2.5j], dtype=np.complex64)
>>> rms(z)
2.3979158

An equivalent NumPy expression:

>>> np.sqrt(np.mean(z.real**2 + z.imag**2))
2.3979158

```

### `vnorm`

`vnorm(x, p)` computes the vector p-norm of 1D arrays.  It is a gufunc with
signatue `(i), () -> ()`.

For example, to compute the 2-norm of [3, 4]:
```
>>> import numpy as np
>>> from ufunclab import vnorm

>>> vnorm([3, 4], 2)
5.0
```

Compute the p-norm of [3, 4] for several values of p:

```
>>> vnorm([3, 4], [1, 2, 3, np.inf])
array([7.        , 5.        , 4.49794145, 4.        ])
```

Compute the 2-norm of four 2-d vectors:

```
>>> vnorm([[3, 4], [5, 12], [0, 1], [1, 1]], 2)
array([ 5.        , 13.        ,  1.        ,  1.41421356])
```

For the same vectors, compute the p-norm for p = [1, 2, inf]:

```
>>> vnorm([[3, 4], [5, 12], [0, 1], [1, 1]], [[1], [2], [np.inf]])
array([[ 7.        , 17.        ,  1.        ,  2.        ],
       [ 5.        , 13.        ,  1.        ,  1.41421356],
       [ 4.        , 12.        ,  1.        ,  1.        ]])
```

`vnorm` handles complex numbers. Here we compute the norm of `z`
with orders 1, 2, 3, and inf.  (Note that `abs(z)` is [2, 5, 0, 14].)

```
>>> z = np.array([-2j, 3+4j, 0, 14])
>>> vnorm(z, [1, 2, 3, np.inf])
array([21.        , 15.        , 14.22263137, 14.        ])
```

### `vdot`

`vdot(x, y)` is the vector dot product of the real floating point vectors
`x` and `y`.  It is a gufunc with signature `(n),(n)->()`.

```
>>> import numpy as np
>>> from ufunclab import vdot

>>> x = np.array([[1, -2, 3],
...               [4, 5, 6]])
>>> y = np.array([[-1, 0, 3],
                  [1, 1, 1]])

>>> vdot(x, y)  # Default axis is -1.
array([ 8., 15.])

>>> vdot(x, y, axis=0)
array([ 3.,  5., 15.])
```


### `pearson_corr`

`pearson_corr(x, y)` computes Pearson's product-moment correlation coefficient.
It is a gufunc with shape signature `(n),(n)->()`.

```
>>> import numpy as np
>>> from ufunclab import pearson_corr

>>> x = np.array([1.0, 2.0, 3.5, 7.0, 8.5, 10.0, 11.0])
>>> y = np.array([10, 11.5, 11.4, 13.6, 15.1, 16.7, 15.0])
>>> pearson_corr(x, y)
0.9506381287828245
```

In the following example, a trivial dimension is added to the array `a` before
passing it to `pearson_corr`, so the inputs are compatible for broadcasting.
The correlation coefficient of each row of `a` with each row of `b` is computed,
giving a result with shape (3, 2).

```
>>> a = np.array([[2, 3, 1, 3, 5, 8, 8, 9],
...               [3, 3, 1, 2, 2, 4, 4, 5],
...               [2, 5, 1, 2, 2, 3, 3, 8]])
>>> b = np.array([[9, 8, 8, 7, 4, 4, 1, 2],
...               [8, 9, 9, 6, 5, 7, 3, 4]])
>>> pearson_corr(np.expand_dims(a, 1), b)
array([[-0.92758645, -0.76815464],
       [-0.65015428, -0.53015896],
       [-0.43575108, -0.32925148]])
```

### `cross2`

`cross2(u, v)` is a gufunc with signature `(2),(2)->()`.  It computes
the 2-d cross product that returns a scalar.  That is, `cross2([u0, u1], [v0, v1])`
is `u0*v1 - u1*v0`.  The calculation is the same as that of `numpy.cross`,
but `cross2` is restricted to 2-d inputs.

For example,
```
>>> import numpy as np
>>> from ufunclab import cross2

>>> cross2([1, 2], [5, 3])
-7

>>> cross2([[1, 2], [6, 0]], [[5, 3], [2, 3]])
array([-7, 18])

>>> cross2([1j, 3], [-1j, 2+3j])
(-3+5j)
```

In the following, `a` and `b` are object arrays; `a` has shape (2,),
and `b` has shape (3, 2).  The result of ``cross2(a, b)`` has shape
(3,).

```
>>> from fractions import Fraction as F

>>> a = np.array([F(1, 3), F(2, 7)])
>>> b = np.array([[F(7, 4), F(6, 7)], [F(2, 5), F(-3, 7)], [1, F(1, 4)]])
>>> cross2(a, b)
array([Fraction(-3, 14), Fraction(-9, 35), Fraction(-17, 84)],
      dtype=object)
```

### `cross3`

`cross3(u, v)` is a gufunc with signature `(3),(3)->(3)`.  It computes
the 3-d vector cross product (like `numpy.cross`, but specialized to the
case of 3-d vectors only).

For example,
```
>>> import numpy as np
>>> from ufunclab import cross3

>>> u = np.array([1, 2, 3])
>>> v = np.array([2, 2, -1])

>>> cross3(u, v)
array([-8,  7, -2])
```

In the following, `x` has shape (5, 3), and `y` has shape (2, 1, 3).
The result of `cross3(x, y)` has shape (2, 5, 3).

```
>>> x = np.arange(15).reshape(5, 3)
>>> y = np.round(10*np.sin(np.linspace(0, 2, 6))).reshape(2, 1, 3)

>>> x
array([[ 0,  1,  2],
       [ 3,  4,  5],
       [ 6,  7,  8],
       [ 9, 10, 11],
       [12, 13, 14]])

>>> y
array([[[ 0.,  4.,  7.]],

       [[ 9., 10.,  9.]]])

>>> cross3(x, y)
array([[[ -1.,   0.,   0.],
        [  8., -21.,  12.],
        [ 17., -42.,  24.],
        [ 26., -63.,  36.],
        [ 35., -84.,  48.]],

       [[-11.,  18.,  -9.],
        [-14.,  18.,  -6.],
        [-17.,  18.,  -3.],
        [-20.,  18.,   0.],
        [-23.,  18.,   3.]]])
```

### `tri_area`

`tri_area(p)` is a gufunc with signature `(3, n) - > ()`.  It computes the
area of a triangle defined by three points in n-dimensional space.

```
>>> import numpy as np
>>> from ufunclab import tri_area

`p` has shape (2, 3, 4). It contains the vertices
of two triangles in 4-dimensional space.

>>> p = np.array([[[0.0, 0.0, 0.0, 6.0],
                   [1.0, 2.0, 3.0, 6.0],
                   [0.0, 2.0, 2.0, 6.0]],
                  [[1.5, 1.0, 2.5, 2.0],
                   [4.0, 1.0, 0.0, 2.5],
                   [2.0, 1.0, 2.0, 2.5]]])
>>> tri_area(p)
array([1.73205081, 0.70710678])
```

### `fillnan1d`

`fillnan1d(x)` is a gufunc with signature `(i)->(i)`.  It uses linear
interpolation to replace occurrences of `nan` in `x`.

```
>>> import numpy as np
>>> from ufunclab import fillnan1d

>>> x = np.array([1.0, 2.0, np.nan, np.nan, 3.5, 5.0, np.nan, 7.5])
>>> fillnan1d(x)
array([1.  , 2.  , 2.5 , 3.  , 3.5 , 5.  , 6.25, 7.5 ])
```

`nan` values at the ends of `x` are replaced with the nearest non-`nan`
value:

```
>>> x = np.array([np.nan, 2.0, np.nan, 5.0, np.nan, np.nan])
>>> fillnan1d(x)
array([2. , 2. , 3.5, 5. , 5. , 5. ])
```

This plot of the result of applying `fillnan1d(x)` to a bigger sample is
generated by the script `examples/fillnan1d_demo.py`:

![fillnan1d plot](https://github.com/WarrenWeckesser/ufunclab/blob/main/examples/fillnan1d_demo.png)

### `backlash`

`backlash(x, deadband, initial)`, a gufunc with signature `(i),(),()->(i)`,
computes the "backlash" response of a signal; see the Wikipedia article
[Backlash (engineering)](https://en.wikipedia.org/wiki/Backlash_(engineering)).
The function emulates the
[backlash block](https://www.mathworks.com/help/simulink/slref/backlash.html)
of Matlab's Simulink library.

For example,

```
>>> import numpy as np
>>> from ufunclab import backlash

>>> x = np.array([0, 0.5, 1, 1.1, 1.0, 1.5, 1.4, 1.2, 0.5])
>>> deadband = 0.4
>>> initial = 0

>>> backlash(x, deadband, initial)
array([0. , 0.3, 0.8, 0.9, 0.9, 1.3, 1.3, 1.3, 0.7])
```

The script `backlash_demo.py` in the `examples` directory generates
the plot

![Backlash plot](https://github.com/WarrenWeckesser/ufunclab/blob/main/examples/backlash_demo.png)


### `hysteresis_relay`

`hysteresis_relay(x, low_threshold, high_threshold, low_value, high_value, init)`,
a gufunc with signature `(i),(),(),(),(),()->(i)`, passes `x` through a relay
with hysteresis (like a Schmitt trigger). The function is similar to the
[relay block](https://www.mathworks.com/help/simulink/slref/relay.html)
of Matlab's Simulink library.

The script `hysteresis_relay_demo.py` in the `examples` directory generates
the plot

![hysteresis_replay plot](https://github.com/WarrenWeckesser/ufunclab/blob/main/examples/hysteresis_relay_demo.png)

### `sosfilter`

`sosfilter(sos, x)` is a gufunc with signature `(m,6),(n)->(n)`.
The function applies a discrete time linear filter to the input
array `x`.  The array `sos` with shape `(m,6)` represents the
linear filter using the *second order sections* format.

The function is like `scipy.signal.sosfilt`, but this version does
not accept the `zi` parameter.  See `sosfilter_ic` for a function
that accepts `zi`.

The script `sosfilter_demo.py` in the `examples` directory generates
the plot

![sosfilter plot](https://github.com/WarrenWeckesser/ufunclab/blob/main/examples/sosfilter_demo.png)

### `sosfilter_ic`

`sosfilter_ic(sos, x, zi)` is a gufunc with signature
`(m,6),(n),(m,2)->(n),(m,2)`.  Like `sosfilter`, the function applies
a discrete time linear filter to the input array `x`.  The array `sos`
with shape `(m,6)` represents the linear filter using the *second order
sections* format.

This function is like `scipy.signal.sosfilt`, but for `sosfilter_ic`,
the `zi` parameter is *required*.  Also, because `sosfilter_ic` is a gufunc,
it uses the gufunc rules for broadcasting.  `scipy.signal.sosfilt` handles
broadcasting of the `zi` parameter differently.

### `sosfilter_ic_contig`

`sosfilter_ic_contig(sos, x, zi)` is a gufunc with signature
`(m,6),(n),(m,2)->(n),(m,2)`.  This function has the same inputs and
performs the same calculation as `sosfilter_ic`, but it assumes that the
array inputs are all C-contiguous.  It does not verify this; if an array
input is *not* C-contiguous, the results will be incorrect, and the program
might crash.

### `gendot`

`gendot` creates a new gufunc (with signature `(i),(i)->()`) that is
the composition of two ufuncs.  The first ufunc must be an element-wise
ufunc with two inputs and one output.  The second must be either another
element-wise ufunc with two inputs and one output, or a gufunc with
signature `(i)->()`.

The name `gendot` is from "generalized dot product".  The standard
dot product is the composition of element-wise multiplication and
reduction with addition.  The `prodfunc` and `sumfunc` arguments of
`gendot` take the place of multiplication and addition.

For example, to take the element-wise minimum of two 1-d arrays,
and then take the maximum of the result:

```
>>> import numpy as np
>>> from ufunclab import gendot

>>> minmaxdot = gendot(np.minimum, np.maximum)

>>> a = np.array([1.0, 2.5, 0.3, 1.9, 3.0, 1.8])
>>> b = np.array([0.5, 1.1, 0.9, 2.1, 0.3, 3.0])
>>> minmaxdot(a, b)
1.9
```

`minmaxdot` is a gufunc with signature `(i),(i)->()`;  the type
signatures of the gufunc loop functions were derived by matching
the signatures of the ufunc loop functions for `np.minimum` and
`np.maximum`:

```
>>> minmaxdot.signature
'(i),(i)->()'

>>> print(minmaxdot.types)
['??->?', 'bb->b', 'BB->B', 'hh->h', 'HH->H', 'ii->i', 'II->I', 'll->l',
 'LL->L', 'qq->q', 'QQ->Q', 'ee->e', 'ff->f', 'dd->d', 'gg->g', 'FF->F',
 'DD->D', 'GG->G', 'mm->m', 'MM->M']
```

`gendot` is experimental, and might not be useful in many applications.
We could do the same calculation as `minmaxdot` with, for example,
`np.maximum.reduce(np.minimum(a, b))`, and in fact, the pure NumPy
version is faster than `minmaxdot(a, b)` for large (and even moderately
sized) 1-d arrays.  An advantage of the `gendot` gufunc is that it does
not create an intermediate array when broadcasting takes place.  For
example, with inputs `x` and `y` with shapes `(20, 10000000)` and
`(10, 1, 10000000)`, the equivalent of `minmaxdot(x, y)` can be computed
with `np.maximum.reduce(np.minimum(x, y), axis=-1)`, but `np.minimum(x, y)`
creates an array with shape `(10, 20, 10000000)`.  Computing the result
with `minmaxdot(x, y)` does not create the temporary intermediate array.

### `ufunc_inspector`

`ufunc_inspector(func)` prints information about a NumPy ufunc.

For example,

```
>>> import numpy as np
>>> from ufunclab import ufunc_inspector
>>> np.__version__
'1.24.0'
>>> ufunc_inspector(np.hypot)
'hypot' is a ufunc.
nin = 2, nout = 1
ntypes = 5
loop types:
  0: ( 23,  23) ->  23  (ee->e)  PyUFunc_ee_e_As_ff_f
  1: ( 11,  11) ->  11  (ff->f)  PyUFunc_ff_f
  2: ( 12,  12) ->  12  (dd->d)  PyUFunc_dd_d
  3: ( 13,  13) ->  13  (gg->g)  PyUFunc_gg_g
  4: ( 17,  17) ->  17  (OO->O)  PyUFunc_OO_O_method
```

(The output will likely change as the code develops.)

```
>>> ufunc_inspector(np.sqrt)
'sqrt' is a ufunc.
nin = 1, nout = 1
ntypes = 10
loop types:
  0:   23 ->  23  (e->e)  PyUFunc_e_e_As_f_f
  1:   11 ->  11  (f->f)  not generic (or not in the checked generics)
  2:   12 ->  12  (d->d)  not generic (or not in the checked generics)
  3:   11 ->  11  (f->f)  PyUFunc_f_f
  4:   12 ->  12  (d->d)  PyUFunc_d_d
  5:   13 ->  13  (g->g)  PyUFunc_g_g
  6:   14 ->  14  (F->F)  PyUFunc_F_F
  7:   15 ->  15  (D->D)  PyUFunc_D_D
  8:   16 ->  16  (G->G)  PyUFunc_G_G
  9:   17 ->  17  (O->O)  PyUFunc_O_O_method

>>> ufunc_inspector(np.add)
'add' is a ufunc.
nin = 2, nout = 1
ntypes = 22
loop types:
  0: (  0,   0) ->   0  (??->?)  not generic (or not in the checked generics)
  1: (  1,   1) ->   1  (bb->b)  not generic (or not in the checked generics)
  2: (  2,   2) ->   2  (BB->B)  not generic (or not in the checked generics)
  3: (  3,   3) ->   3  (hh->h)  not generic (or not in the checked generics)
  4: (  4,   4) ->   4  (HH->H)  not generic (or not in the checked generics)
  5: (  5,   5) ->   5  (ii->i)  not generic (or not in the checked generics)
  6: (  6,   6) ->   6  (II->I)  not generic (or not in the checked generics)
  7: (  7,   7) ->   7  (ll->l)  not generic (or not in the checked generics)
  8: (  8,   8) ->   8  (LL->L)  not generic (or not in the checked generics)
  9: (  9,   9) ->   9  (qq->q)  not generic (or not in the checked generics)
 10: ( 10,  10) ->  10  (QQ->Q)  not generic (or not in the checked generics)
 11: ( 23,  23) ->  23  (ee->e)  not generic (or not in the checked generics)
 12: ( 11,  11) ->  11  (ff->f)  not generic (or not in the checked generics)
 13: ( 12,  12) ->  12  (dd->d)  not generic (or not in the checked generics)
 14: ( 13,  13) ->  13  (gg->g)  not generic (or not in the checked generics)
 15: ( 14,  14) ->  14  (FF->F)  not generic (or not in the checked generics)
 16: ( 15,  15) ->  15  (DD->D)  not generic (or not in the checked generics)
 17: ( 16,  16) ->  16  (GG->G)  not generic (or not in the checked generics)
 18: ( 21,  22) ->  21  (Mm->M)  not generic (or not in the checked generics)
 19: ( 22,  22) ->  22  (mm->m)  not generic (or not in the checked generics)
 20: ( 22,  21) ->  21  (mM->M)  not generic (or not in the checked generics)
 21: ( 17,  17) ->  17  (OO->O)  PyUFunc_OO_O
```


### Resources

Here's a collection of resources for learning about the C API for ufuncs.

* [Universal functions (ufunc)](https://numpy.org/devdocs/reference/ufuncs.html)
* [UFunc API](https://numpy.org/devdocs/reference/c-api/ufunc.html)
* [Generalized Universal Function API](https://numpy.org/devdocs/reference/c-api/generalized-ufuncs.html)
* [NEP 5 — Generalized Universal Functions](https://numpy.org/neps/nep-0005-generalized-ufuncs.html)
* [NEP 20 — Expansion of Generalized Universal Function Signatures](https://numpy.org/neps/nep-0020-gufunc-signature-enhancement.html)
* [Universal functions](https://numpy.org/devdocs/reference/internals.code-explanations.html#universal-functions),
  part of the [NumPy C Code Explanations](https://numpy.org/devdocs/reference/internals.code-explanations.html)
  * In particular, the section
    ["Function call"](https://numpy.org/devdocs/reference/internals.code-explanations.html#function-call)
    explains when the GIL is released.
* When implementing inner loops for many NumPy dtypes, the
  [NumPy distutils](https://numpy.org/doc/stable/reference/distutils_guide.html)
  [template preprocessor](https://numpy.org/doc/stable/reference/distutils_guide.html#conversion-of-src-files-using-templates)
  is a useful tool. (See the ["Other files"](https://numpy.org/doc/stable/reference/distutils_guide.html#other-files)
  section for the syntax that would be used in, say, a C file.)
* Some relevant NumPy source code, if you want to dive deep:
  * `PyUFuncObject` along with related C types and macros are defined in
   [`numpy/numpy/core/include/numpy/ufuncobject.h`](https://github.com/numpy/numpy/blob/7214ca4688545b432c45287195e2f46c5e418ce8/numpy/core/include/numpy/ufuncobject.h).
  * `PyUFunc_FromFuncAndData` and `PyUFunc_FromFuncAndDataAndSignatureAndIdentity`
    are defined in the file [`numpy/numpy/core/src/umath/ufunc_object.c`](https://github.com/numpy/numpy/blob/7214ca4688545b432c45287195e2f46c5e418ce8/numpy/core/src/umath/ufunc_object.c).
* Section of the [SciPy Lecture Notes](https://scipy-lectures.org/index.html) on ufuncs:
  * [2.2.2 Universal Functions](https://scipy-lectures.org/advanced/advanced_numpy/index.html#universal-functions)
* [Data Type API](https://numpy.org/doc/stable/reference/c-api/dtype.html) --
  a handy reference.
