"""Execute the checker alias recipe with its actual runtime shape/dtype contract."""

import numpy as np
import pytest
from beartype.roar import BeartypeCallHintParamViolation

from tests.typing.check_make_array_type import custom_identity, point_identity


def test_native_factory_alias_recipe_runs() -> None:
  vector = np.ones(3, dtype=np.float32)
  assert custom_identity(vector) is vector
  with pytest.raises(BeartypeCallHintParamViolation):
    custom_identity(np.ones(3, dtype=np.int32))
  with pytest.raises(BeartypeCallHintParamViolation):
    custom_identity(np.ones((2, 3), dtype=np.float32))
  points = np.zeros(3, dtype=[("x", np.float32), ("y", np.float32)])
  assert point_identity(points) is points
  with pytest.raises(BeartypeCallHintParamViolation):
    point_identity(np.ones(3, dtype=np.float32))
  with pytest.raises(BeartypeCallHintParamViolation):
    point_identity(np.zeros(3, dtype=[("wrong", np.float32)]))
