"""Protect the released beartype integration used by the supported baseline."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pytest
from beartype import BeartypeConf, beartype
from beartype.roar import BeartypeCallHintParamViolation

from bearshape import N
from bearshape.numpy import F32


@beartype
@dataclass
class ArrayRecord:
  values: F32[N]

  def same(self) -> ArrayRecord:
    return self


def test_dataclass_forward_self_reference() -> None:
  values = np.ones(3, dtype=np.float32)
  record = ArrayRecord(values)
  assert record.same() is record
  with pytest.raises(BeartypeCallHintParamViolation):
    ArrayRecord(np.ones(3, dtype=np.int32))


def test_deterministic_sampling_preserves_dimension_bindings() -> None:
  @beartype(conf=BeartypeConf(is_random=False))
  def first(values: list[F32[N]], expected: F32[N]) -> F32[N]:
    return values[0]

  good = np.ones(3, dtype=np.float32)
  wrong = np.ones(4, dtype=np.float32)
  assert first([good, wrong], good) is good
  with pytest.raises(BeartypeCallHintParamViolation):
    first([wrong, good], good)
  with pytest.raises(BeartypeCallHintParamViolation):
    first([np.ones(3, dtype=np.int32), good], good)
