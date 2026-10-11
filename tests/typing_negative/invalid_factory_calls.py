"""Dynamic runtime factories retain native argument errors through aliases."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from tests.typing.check_make_array_type import custom_identity, point_identity

if TYPE_CHECKING:
  from numpy.typing import NDArray

integers: NDArray[np.int32] = np.ones(3, dtype=np.int32)
floats: NDArray[np.float32] = np.ones(3, dtype=np.float32)
custom_identity(integers)  # expect: argument
custom_identity([1.0, 2.0])  # expect: argument
point_identity(floats)  # expect: argument
point_identity("not an array")  # expect: argument
