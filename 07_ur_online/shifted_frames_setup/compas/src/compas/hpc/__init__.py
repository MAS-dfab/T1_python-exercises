""".. _compas.hpc:

********************************************************************************
hpc
********************************************************************************

.. module:: compas.hpc


.. warning::

    The functionality provided by this package is experimental and subject to frequent change.
    For now, don't use it for anything important :)


cuda
====

.. autosummary::
    :toctree: generated/

    cuda_diag
    cuda_eye
    cuda_get
    cuda_give
    cuda_ones
    cuda_random
    cuda_real
    cuda_reshape
    cuda_flatten
    cuda_tile
    cuda_zeros
    cuda_conj
    cuda_cross
    cuda_det
    cuda_dot
    cuda_eig
    cuda_hermitian
    cuda_inv
    cuda_normrow
    cuda_pinv
    cuda_svd
    cuda_trace
    cuda_transpose
    cuda_abs
    cuda_argmax
    cuda_argmin
    cuda_acos
    cuda_asin
    cuda_atan
    cuda_ceil
    cuda_cos
    cuda_cosh
    cuda_exp
    cuda_floor
    cuda_log
    cuda_max
    cuda_min
    cuda_mean
    cuda_sin
    cuda_sinh
    cuda_sqrt
    cuda_sum
    cuda_tan
    cuda_tanh
    cuda_device


euler
=====


geometry
========


numba
=====

.. autosummary::
    :toctree: generated/

    numba_devo
    numba_drx
    numba_cross
    numba_vdot
    numba_dot
    numba_length


opencl
======

.. autosummary::
    :toctree: generated/


"""

from .cuda import *
from .numba_ import *
from .opencl import *

from .cuda import __all__ as a
from .numba_ import __all__ as b
from .opencl import __all__ as c

__all__ = a + b + c
