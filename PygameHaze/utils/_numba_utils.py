# MIT License
#
# Copyright (c) 2021 Emc2356
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
some numba utils to make it easier to make signatures and a lot cleaner
support for only numerical types
"""

from typing import Optional, Dict

USE_NUMBA = False

try:
    # check if the user has numba installed in the current env
    import numba as nb

    USE_NUMBA = True
except ImportError:
    pass

try:
    # check if the user has numpy installed in the current env
    import numpy as np
except ImportError:
    import sys

    print(f"unable to import numpy, maybe it isn't installed?", file=sys.stderr)
    raise


class Array:
    def __init__(self, tp, dim):
        self.type = tp
        self.dim = dim

    def to_sig(self):
        return f"{TYPES[self.type]}[{', '.join(':' * self.dim)}]"


class complex128(complex):
    pass


class complex64(complex):
    pass


class float64(float):
    pass


class float32(float):
    pass


class uint64(int):
    pass


class uint32(int):
    pass


class int64(int):
    pass


class int32(int):
    pass


class void:  # cant inherit from NoneType
    pass


class array(Array):
    pass


class _TYPES:
    __TYPES: Dict[type, str] = {
        # complex types
        np.complex128: "complex128",
        np.complex64: "complex64",
        complex128: "complex128",
        complex64: "complex64",
        complex: "complex128",
        # float types
        np.float64: "float64",
        np.float32: "float32",
        float64: "float64",
        float32: "float32",
        float: "float64",
        # unsigned ints types
        np.uint64: "uint64",
        np.uint32: "uint32",
        uint64: "uint64",
        uint32: "uint32",
        # int types
        np.int64: "int64",
        np.int32: "int32",
        int64: "int64",
        int32: "int32",
        int: "int64",
        # None type
        np.void: "void",
        void: "void",
        None: "void",
    }

    # check for the optional packages
    if USE_NUMBA:
        __TYPES.update(
            {
                nb.complex128: "complex128",
                nb.complex64: "complex64",
                nb.float64: "float64",
                nb.float32: "float32",
                nb.uint64: "uint64",
                nb.uint32: "uint32",
                nb.int64: "int64",
                nb.int32: "int32",
                nb.void: "void",
            }
        )

    @classmethod
    def __getitem__(cls, item):
        if item in cls.__TYPES:
            return cls.__TYPES[item]

        if isinstance(item, Array):
            return item.to_sig()

        return item


TYPES = _TYPES()  # to access the dunder methods


def sig_from_function(func) -> Optional[str]:
    # constructing a numba signature out of the typehints of the function
    if (
        hasattr(func, "__annotations__")
        and func.__annotations__
        and "return" in func.__annotations__
    ):
        args = []
        ret = func.__annotations__.pop("return")

        for name, anno in func.__annotations__.items():
            args.append(anno)
        return f"""{TYPES[ret]}({", ".join([TYPES[anno] for anno in args])})"""
    return None


def njit(sig=None, **kwargs):
    """automatic signature creation, can be turned off if specified, with checks to see if numba exists"""
    if (
        not USE_NUMBA
    ):  # this is the only place file numba is imported so we can control it easier
        if "func" in kwargs:
            return kwargs["func"]
        return lambda func: func

    nosig = False
    if "nosig" in kwargs:
        nosig = kwargs.pop("nosig")

    if sig is None and not nosig:
        sig = sig_from_function(kwargs.get("func", None))

    nogil = True
    if "nogil" in kwargs:
        nogil = kwargs.pop("nogil")
    fm = True
    if "fastmath" in kwargs:
        fm = kwargs.pop("fastmath")

    if sig is not None and not nosig:
        if "func" in kwargs:
            func = kwargs.pop("func")
            return nb.njit(sig, fastmath=fm, nogil=nogil, **kwargs)(func)
        return nb.njit(sig, fastmath=fm, nogil=nogil, **kwargs)
    if "func" in kwargs:
        func = kwargs.pop("func")
        return nb.njit(fastmath=fm, nogil=nogil, **kwargs)(func)
    return nb.njit(fastmath=fm, nogil=nogil, **kwargs)


if USE_NUMBA:
    prange = nb.prange  # alias so we dont have to import numba again
else:
    prange = range


if USE_NUMBA:
    typed = nb.typed
else:

    class typed:
        class Dict:
            def empty(*args, **kwargs):
                return {}

        class List:
            def empty(*args, **kwargs):
                return []
