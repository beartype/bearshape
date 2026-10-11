"""Independent public checks cannot contaminate a late union transaction."""

import sys
from typing import Annotated

import numpy as np
import pytest
from beartype import beartype
from beartype._check.forward.reference._cls.fwdrefcache import ref_proxy_cache
from beartype.door import die_if_unbearable, is_bearable
from beartype.roar import BeartypeCallHintParamViolation, BeartypeDoorHintViolation
from beartype.vale import Is

from bearshape import C, N, check
from bearshape.numpy import F32

IsolationN = F32[N]
IsolationC = F32[C]


def array(size: int) -> np.ndarray:
  return np.ones(size, dtype=np.float32)


@pytest.mark.parametrize("mode", ["automatic", "explicit"])
@pytest.mark.parametrize("kind", ["door", "raiser", "decorated"])
@pytest.mark.parametrize("nested_first", [True, False])
@pytest.mark.parametrize("nested_rejects", [True, False])
def test_nested_composite_checks_are_isolated(
  monkeypatch: pytest.MonkeyPatch,
  mode: str,
  kind: str,
  *,
  nested_first: bool,
  nested_rejects: bool,
) -> None:
  module = sys.modules[__name__]
  for name in ("IsolationN", "IsolationC"):
    monkeypatch.delattr(module, name, raising=False)
  ref_proxy_cache.clear_cache()
  calls = []
  inner_hint = tuple[F32[N], str if nested_rejects else int]

  @beartype
  def inner(value: inner_hint) -> None:
    pass

  def independent(value: object) -> bool:
    calls.append(True)
    item = (array(7), 1)
    if kind == "door":
      assert is_bearable(item, inner_hint) is not nested_rejects
    elif nested_rejects:
      exception = (
        BeartypeDoorHintViolation
        if kind == "raiser"
        else BeartypeCallHintParamViolation
      )
      with pytest.raises(exception):
        die_if_unbearable(item, inner_hint) if kind == "raiser" else inner(item)
    elif kind == "raiser":
      die_if_unbearable(item, inner_hint)
    else:
      inner(item)
    return True

  # Avoid reusing another parametrization's closure through upstream repr caches.
  independent.__qualname__ += f"_{mode}_{kind}_{nested_first}_{nested_rejects}"
  probe = Annotated[int, Is[independent]]
  hint = (
    tuple[probe, "IsolationN", str] | tuple[int, "IsolationC", int]
    if nested_first
    else tuple["IsolationN", probe, str] | tuple["IsolationC", int, int]
  )

  @beartype
  def outer(value: hint, last: F32[N]) -> None:
    pass

  fn = check(outer) if mode == "explicit" else outer
  monkeypatch.setattr(module, "IsolationN", F32[N], raising=False)
  monkeypatch.setattr(module, "IsolationC", F32[C], raising=False)
  value = (1, array(2), 1) if nested_first else (array(2), 1, 1)
  try:
    fn(value, array(3))
    assert calls
    first = (*value[:2], "accepted")
    with pytest.raises(BeartypeCallHintParamViolation):
      fn(first, array(3))
    fn(first, array(2))
  finally:
    ref_proxy_cache.clear_cache()
