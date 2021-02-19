"""
NumPy ufuncs and utilities.
"""

from ._logfact import logfactorial
from ._peaktopeak import peaktopeak
from ._minmax import minmax, argminmax, min_argmin, max_argmax
from ._means import gmean, hmean
from ._mad import mad, mad1, rmad, rmad1
from ._backlash import backlash
from ._deadzone import deadzone
from ._all_same import all_same
from ._ufunc_inspector import ufunc_inspector
