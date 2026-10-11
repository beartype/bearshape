"""Preserve corrected Tree and strict-variadic contracts through composition."""

from typing import Annotated

import numpy as np
import pytest
from beartype import BeartypeConf, beartype
from beartype.door import is_bearable
from beartype.roar import BeartypeCallHintParamViolation
from beartype.vale import Is

from bearshape import C, N, check, check_context
from bearshape._memo import get_memo
from bearshape.numpy import F32
from bearshape.optree import Tree


@pytest.mark.parametrize("backend", ["optree", "jax"])
@pytest.mark.parametrize("mode", ["automatic", "explicit", "combined"])
def test_late_tree_alias_with_composite_leaves(
  monkeypatch: pytest.MonkeyPatch, backend: str, mode: str
) -> None:
  import sys

  tree = Tree
  if backend == "jax":
    from bearshape.jax import Tree as JaxTree

    tree = JaxTree
  alias_name = f"LateAuditTree_{backend}_{mode}"

  def consume(value: object, last: object) -> None:
    pass

  consume.__annotations__ = {"value": alias_name, "last": F32[N]}
  if mode == "automatic":
    checked = beartype(consume)
  elif mode == "explicit":
    checked = check(beartype(consume))
  else:
    checked = check(conf=BeartypeConf())(consume)
  leaf_hint = Annotated[F32[N], Is[lambda _value: False]] | F32[C]
  monkeypatch.setattr(sys.modules[__name__], alias_name, tree[leaf_hint], raising=False)
  two = np.ones(2, dtype=np.float32)
  three = np.ones(3, dtype=np.float32)
  checked([two, two], three)
  with pytest.raises(BeartypeCallHintParamViolation):
    checked([two, three], three)
  checked([three, three], two)


def test_rejected_alternative_restores_variadic_strictness() -> None:
  hint = tuple[F32[~N], str] | tuple[F32[~C], int]
  with check_context():
    assert is_bearable(np.ones(2, dtype=np.float32), F32[~+N])
    assert is_bearable((np.ones(2, dtype=np.float32), 1), hint)
    assert get_memo().variadic == {"N": (True, (2,)), "C": (False, (2,))}
    assert is_bearable(np.ones((3, 2), dtype=np.float32), F32[~+N])
