import pytest

from itertools import chain, cycle
from collections import OrderedDict, UserList
from collections.abc import Iterator

from unification import unify, reify, var

from cons import cons, car, cdr
from cons.core import ConsPair, MaybeCons, ConsNull, ConsError, NonCons


def test_noncons_type():

    with pytest.raises(TypeError):
        NonCons()

    class MyStr(object):
        pass

    NonCons.register(MyStr)

    assert issubclass(MyStr, NonCons)
    assert not isinstance(MyStr, NonCons)
    assert not issubclass(MyStr, MaybeCons)
    assert not issubclass(ConsPair, NonCons)


def test_cons_type():
    with pytest.raises(TypeError):
        MaybeCons()

    assert isinstance(cons(1, "hi"), ConsPair)
    assert isinstance((1, 2), ConsPair)
    assert isinstance([1, 2], ConsPair)
    assert isinstance(OrderedDict({1: 2}), ConsPair)
    assert isinstance(iter([1]), ConsPair)

    assert not isinstance({1: 2}, MaybeCons)
    assert not isinstance(cons(1, "hi"), MaybeCons)
    assert not isinstance({}, ConsPair)
    assert not isinstance(set(), ConsPair)
    assert not isinstance(set([1, 2]), ConsPair)
    assert not isinstance("hi", ConsPair)
    assert not isinstance("hi", ConsPair)
    assert not isinstance(1, ConsPair)
    assert not isinstance(iter([]), ConsPair)
    assert not isinstance(OrderedDict({}), ConsPair)
    assert not isinstance((), ConsPair)
    assert not isinstance([], ConsPair)


def test_cons_null():

    with pytest.raises(TypeError):
        ConsNull()

    assert isinstance(None, ConsNull)
    assert isinstance([], ConsNull)
    assert isinstance(tuple(), ConsNull)
    assert isinstance(OrderedDict(), ConsNull)
    assert isinstance(iter([]), ConsNull)
    assert not isinstance(object, ConsNull)
    assert not isinstance([1], ConsNull)
    assert not isinstance((1,), ConsNull)
    assert not isinstance(OrderedDict([(1, 2)]), ConsNull)
    assert not isinstance(iter([1]), ConsNull)
    assert not isinstance(cycle([5]), ConsNull)


def test_cons_join():

    with pytest.raises(ValueError):
        cons("a")

    assert cons(1, 2, 3, 4) == cons(1, cons(2, cons(3, 4)))
    assert cons("a", None) == cons("a", []) == ["a"]
    assert cons("a", ()) == ("a",)
    assert cons("a", []) == ["a"]
    assert cons(None, "a").car is None
    assert cons(None, "a").cdr == "a"
    assert cons((), "a") == ConsPair((), "a")
    assert cons([], "a") == ConsPair([], "a")
    assert cons("a", None) == ["a"]
    assert cons("a", ["b", "c"]) == ["a", "b", "c"]
    assert cons("a", ("b", "c")) == ("a", "b", "c")
    assert type(cons(("a", 1), {"b": 2})) == ConsPair
    assert cons(("a", 1), OrderedDict({"b": 2})) == OrderedDict(
        [("a", 1), ("b", 2)]
    )

    assert cons(["a", "b"], "c") == ConsPair(["a", "b"], "c")

    assert cons(("a", "b"), "c") == ConsPair(("a", "b"), "c")
    assert cons(["a", "b"], ["c", "d"]) == [["a", "b"], "c", "d"]
    assert cons(("a", "b"), ["c", "d"]) == [("a", "b"), "c", "d"]
    assert cons(["a", "b"], ("c", "d")) == (["a", "b"], "c", "d")
    assert type(cons(1, iter([3, 4]))) == chain
    assert list(cons([1, 2], iter([3, 4]))) == [[1, 2], 3, 4]
    assert list(cons(1, iter([2, 3]))) == [1, 2, 3]

    assert cons("a", cons("b", cons("c", None))) == ["a", "b", "c"]
    assert cons("a", cons("b", "c")).car == "a"
    assert cons("a", cons("b", "c")).cdr == cons("b", "c")

    # Make sure that an overridden "append" (via `__add__`) is used and
    # that the results are returned unadulterated
    clist_res = [1, 2, 3]

    class CustomList(UserList):
        def __add__(self, a):
            return clist_res

    assert cons(1, CustomList([2, 3])) is clist_res


def test_cons_class():
    c = cons(1, 2)
    assert {c: 1}[c] == 1
    assert repr(cons(1, 2)) == "ConsPair(1, 2)"
    assert str(cons(1, 2, 3)) == "(1 . (2 . 3))"


def test_car_cdr():

    with pytest.raises(ConsError):
        car(object())

    with pytest.raises(ConsError):
        car(None)

    with pytest.raises(ConsError):
        car(tuple())

    with pytest.raises(ConsError):
        car([])

    with pytest.raises(ConsError):
        car(iter([]))

    with pytest.raises(ConsError):
        car("ab")

    with pytest.raises(ConsError):
        cdr(object())

    with pytest.raises(ConsError):
        cdr(None)

    with pytest.raises(ConsError):
        cdr(tuple())

    with pytest.raises(ConsError):
        cdr([])

    with pytest.raises(ConsError):
        cdr(iter([]))

    with pytest.raises(ConsError):
        car(OrderedDict())

    with pytest.raises(ConsError):
        cdr(OrderedDict())

    with pytest.raises(ConsError):
        cdr("ab")

    assert car([1, 2]) == 1
    assert cdr([1, 2]) == [2]

    assert car(cons("a", "b")) == "a"

    z = car(cons(iter([]), 1))
    expected = iter([])
    assert type(z) == type(expected)
    assert list(z) == list(expected)

    li = iter([1])
    assert car(li) == 1

    with pytest.raises(ConsError):
        assert car(li) == 1

    li = iter([1])
    assert isinstance(cdr(li), Iterator)
    assert isinstance(cdr(li), Iterator)

    z = cdr(cons(1, iter([])))
    expected = iter([])
    assert isinstance(z, Iterator)
    assert list(z) == list(expected)

    assert car(iter([1])) == 1
    assert list(cdr(iter([1]))) == []
    assert list(cons(car(iter([1])), cdr(iter([1])))) == [1]
    assert list(cdr(iter([1, 2, 3]))) == [2, 3]

    assert car(cons(["a", "b"], "a")) == ["a", "b"]
    assert car(cons(("a", "b"), "a")) == ("a", "b")
    assert cdr(cons("a", "b")) == "b"
    assert cdr(cons("a", ())) == ()
    assert cdr(cons("a", [])) == []
    assert cdr(cons("a", ("b",))) == ("b",)
    assert cdr(cons("a", ["b"])) == ["b"]
    assert car(OrderedDict([(1, 2), (3, 4)])) == (1, 2)
    assert cdr(OrderedDict([(1, 2), (3, 4)])) == [(3, 4)]
    assert cdr(OrderedDict({1: 2})) == []

    assert car(cons(1, cons("a", "b"))) == 1
    assert cdr(cons(1, cons("a", "b"))) == cons("a", "b")

    # We need to make sure that `__getitem__` is actually used.
    # Also, make sure `cdr` returns the `__getitem__` result unaltered
    clist_res = [5]

    class CustomList(UserList):
        def __getitem__(self, *args):
            return clist_res

    assert cdr(CustomList([1, 2, 3])) is clist_res


def test_unification():
    car_lv, cdr_lv = var(), var()

    res = unify([1, 2], cons(car_lv, cdr_lv), {})
    assert res[car_lv] == 1
    assert res[cdr_lv] == [2]

    res = unify([], cons(car_lv, cdr_lv), {})
    assert res is False

    res = unify([1], cons(car_lv, cdr_lv), {})
    assert res[car_lv] == 1
    assert res[cdr_lv] == []

    res = unify((1, 2), cons(car_lv, cdr_lv), {})
    assert res[car_lv] == 1
    assert res[cdr_lv] == (2,)

    res = unify((), cons(car_lv, cdr_lv), {})
    assert res is False

    res = unify((1,), cons(car_lv, cdr_lv), {})
    assert res[car_lv] == 1
    assert res[cdr_lv] == ()

    res = unify(iter([1]), cons(car_lv, cdr_lv), {})
    assert res[car_lv] == 1
    assert list(res[cdr_lv]) == []

    res = unify(cons(car_lv, cdr_lv), iter([1]), {})
    assert res[car_lv] == 1
    assert list(res[cdr_lv]) == []

    res = unify(OrderedDict([("a", 1), ("b", 2)]), cons(car_lv, cdr_lv), {})
    assert res[car_lv] == ("a", 1)
    assert res[cdr_lv] == [("b", 2)]

    res = unify(OrderedDict(), cons(car_lv, cdr_lv), {})
    assert res is False

    # This is only if we allow `None` to signify all/any empty collection,
    # while--somewhat controversially--we let it default to `[]`.
    res = unify([1], cons(1, None), {})
    assert res == {}

    res = unify((1,), cons(1, None), {})
    assert res is False

    res = unify(cons(1, 2), cons(car_lv, 2), {})
    assert res == {car_lv: 1}

    res = unify(cons(1, 2), cons(1, cdr_lv), {})
    assert res == {cdr_lv: 2}

    res = unify((2,), cons(3, ()), {})
    assert res is False

    res = unify(OrderedDict({"a": 1}), cons(car_lv, cdr_lv), {})
    assert res[car_lv] == ("a", 1)
    assert res[cdr_lv] == []

    res = reify(cons(1, cdr_lv), {cdr_lv: [2, 3]})
    assert res == [1, 2, 3]

    res = reify(cons(1, cdr_lv), {cdr_lv: []})
    assert res == [1]

    res = reify(cons(1, cdr_lv), {cdr_lv: None})
    assert res == [1]

    res = reify(cons(1, cons(2, cons(3, cdr_lv))), {cdr_lv: None})
    assert res == [1, 2, 3]

    res = reify(cons(1, cdr_lv), {cdr_lv: tuple()})
    assert res == (1,)

    res = reify(cons(("a", 1), cdr_lv), {cdr_lv: OrderedDict()})
    assert res == OrderedDict({"a": 1})
