"""Additional integration checks: same bindings through late composite aliases."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pytest
from beartype import beartype
from beartype.door import is_bearable
from beartype.roar import BeartypeCallHintParamViolation

from bearshape import C, N, T, Value, check, check_context
from bearshape._memo import get_memo
from bearshape.numpy import F32
from bearshape.optree import Tree


def array(size: int) -> np.ndarray:
  return np.ones(size, dtype=np.float32)


@beartype
def composite_alias(pair: LateCompositeAlias, y: F32[N]) -> None:
  pass


@beartype
def earlier_binding(x: F32[N], pair: LateCompositeTuple) -> None:
  pass


@beartype
def nested_alias(pair: tuple[LateCompositeTuple, str], y: F32[N]) -> None:
  pass


LateCompositeAlias = tuple[F32[N], str] | tuple[F32[C], int]
LateCompositeTuple = tuple[F32[N], int]


@beartype
def value_alias(width: int, pair: LateValueAlias) -> None:
  pass


@beartype
def tree_alias(pair: LateTreeAlias, y: Tree[F32[C], T]) -> None:
  pass


LateValueAlias = tuple[F32[Value("width")], int]
LateTreeAlias = tuple[Tree[F32[N], T], int]


@pytest.mark.parametrize("mode", ["automatic", "explicit"])
def test_late_composite_success_keeps_bindings(mode: str) -> None:
  fn = check(composite_alias) if mode == "explicit" else composite_alias
  fn((array(2), 1), array(3))
  with pytest.raises(BeartypeCallHintParamViolation):
    fn((array(2), "first"), array(3))


@pytest.mark.parametrize("mode", ["automatic", "explicit"])
def test_late_composite_sees_earlier_bindings(mode: str) -> None:
  fn = check(earlier_binding) if mode == "explicit" else earlier_binding
  fn(array(2), (array(2), 1))
  with pytest.raises(BeartypeCallHintParamViolation):
    fn(array(3), (array(2), 1))


@pytest.mark.parametrize("mode", ["automatic", "explicit"])
def test_nested_composite_alias_keeps_bindings(mode: str) -> None:
  fn = check(nested_alias) if mode == "explicit" else nested_alias
  fn(((array(2), 1), "ok"), array(2))
  with pytest.raises(BeartypeCallHintParamViolation):
    fn(((array(2), 1), "ok"), array(3))


@pytest.mark.parametrize("mode", ["automatic", "explicit"])
def test_value_alias_keeps_argument_scope(mode: str) -> None:
  fn = check(value_alias) if mode == "explicit" else value_alias
  fn(3, (array(3), 1))
  with pytest.raises(BeartypeCallHintParamViolation):
    fn(4, (array(3), 1))


@pytest.mark.parametrize("mode", ["automatic", "explicit"])
def test_tree_alias_keeps_structure_scope(mode: str) -> None:
  fn = check(tree_alias) if mode == "explicit" else tree_alias
  fn(([array(2)], 1), [array(3)])
  with pytest.raises(BeartypeCallHintParamViolation):
    fn(([array(2)], 1), {"different": array(3)})


def test_nested_public_door_check_remains_independent() -> None:
  from typing import Annotated

  from beartype.vale import Is

  def independent(value: object) -> bool:
    return is_bearable(array(7), F32[N])

  @beartype
  def outer(x: Annotated[F32[N], Is[independent]], y: F32[N]) -> None:
    pass

  outer(array(2), array(2))
  with pytest.raises(BeartypeCallHintParamViolation):
    outer(array(2), array(7))


def test_failed_composite_without_union_restores_scope() -> None:
  with check_context():
    assert is_bearable(array(7), F32[C])
    assert not is_bearable((array(2), None), tuple[F32[N], str])
    assert get_memo().single == {"C": 7}


def test_delegated_alias_does_not_retain_argument() -> None:
  import gc
  import weakref

  def call() -> object:
    x = array(2)
    reference = weakref.ref(x)
    composite_alias((x, "first"), x)
    return reference

  reference = call()
  gc.collect()
  assert reference() is None


def test_independent_nested_decorated_call_does_not_share_bindings() -> None:
  from typing import Annotated

  from beartype.vale import Is

  @beartype
  def inner(x: F32[N]) -> None:
    pass

  def predicate(value: object) -> bool:
    inner(array(7))
    return True

  @beartype
  def outer(x: Annotated[F32[N], Is[predicate]], y: F32[N]) -> None:
    pass

  outer(array(2), array(2))
  with pytest.raises(BeartypeCallHintParamViolation):
    outer(array(2), array(7))


@beartype
def rejected_late(value: LateRejectingHint) -> None:
  pass


@beartype
def rejected_late_list(value: list[LateRejectingHint]) -> None:
  pass


_generic_bindings = {}


class _State:
  def snapshot(self) -> dict[str, int]:
    return _generic_bindings.copy()

  def restore(self, before: dict[str, int]) -> None:
    _generic_bindings.clear()
    _generic_bindings.update(before)


_state = _State()


def _get_state() -> _State:
  return _state


class _Meta(type):
  __beartype_state__ = staticmethod(_get_state)

  def __instancecheck__(cls, value: object) -> bool:
    if not isinstance(value, list):
      return False
    _generic_bindings[cls.__name__] = len(value)
    return cls.__name__ != "Rejected"


class First(metaclass=_Meta):
  pass


class Rejected(metaclass=_Meta):
  pass


LateRejectingHint = Rejected


@pytest.mark.parametrize("checked", [rejected_late, rejected_late_list])
def test_caught_nested_late_failure_restores_its_own_state(
  checked: Callable[..., object],
) -> None:
  from typing import Annotated

  from beartype.vale import Is

  _generic_bindings.clear()

  def catches_failure(value: object) -> bool:
    with pytest.raises(BeartypeCallHintParamViolation):
      checked([[1, 2]] if checked is rejected_late_list else [1, 2])
    return True

  @beartype
  def accepted(value: Annotated[First, Is[catches_failure]]) -> None:
    pass

  accepted([1])
  assert _generic_bindings == {"First": 1}
