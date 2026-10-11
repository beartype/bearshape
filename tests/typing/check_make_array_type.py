"""Verify make_array_type and DtypeSpec work with type checkers.

Tested with: pyright, mypy, ty and pyrefly
"""

import numpy as np

from bearshape import DtypeSpec, make_array_type

# ---------------------------------------------------------------------------
# DtypeSpec construction
# ---------------------------------------------------------------------------

float32_spec = DtypeSpec("Float32", frozenset({"float32"}))
int_spec = DtypeSpec("Int", frozenset({"int8", "int16", "int32", "int64"}))
multi_spec = DtypeSpec("Real", frozenset({"float32", "float64", "int32", "int64"}))

# Access DtypeSpec attributes
name: str = float32_spec.name
allowed: frozenset[str] = float32_spec.allowed

# ---------------------------------------------------------------------------
# make_array_type usage
# ---------------------------------------------------------------------------

MyF32 = make_array_type(np.ndarray, float32_spec)
MyInt = make_array_type(np.ndarray, int_spec)

# Repr should be available
repr_str: str = repr(MyF32)

# ---------------------------------------------------------------------------
# Structured dtype factory
# ---------------------------------------------------------------------------

from bearshape.numpy import Structured

MyStruct = Structured([("x", np.float32), ("y", np.float32)])
repr_struct: str = repr(MyStruct)

# ---------------------------------------------------------------------------
# Endianness via DtypeSpec constants
# ---------------------------------------------------------------------------

from bearshape._dtypes import FLOAT32_LE

F32LE = make_array_type(np.ndarray, FLOAT32_LE)
repr_le: str = repr(F32LE)

# Native aliases describe the complete annotation, not the dynamic factory.
from typing import TYPE_CHECKING, assert_type

from beartype import beartype
from numpy.typing import NDArray

from bearshape import N

if TYPE_CHECKING:
  CustomVector = NDArray[np.float32]
  PointVector = NDArray[np.void]
else:
  CustomVector = MyF32[N]
  PointVector = MyStruct[N]


@beartype
def custom_identity(value: CustomVector) -> CustomVector:
  return value


@beartype
def point_identity(value: PointVector) -> PointVector:
  return value


vector: NDArray[np.float32] = np.ones(3, dtype=np.float32)
points: NDArray[np.void] = np.zeros(3, dtype=[("x", np.float32), ("y", np.float32)])
assert_type(custom_identity(vector), NDArray[np.float32])
assert_type(custom_identity(vector).dtype, np.dtype[np.float32])
assert_type(point_identity(points), NDArray[np.void])
assert_type(point_identity(points).dtype, np.dtype[np.void])
