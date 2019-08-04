from collections import OrderedDict
from collections.abc import Iterator

from unification.core import unify, _unify, reify, _reify

from .core import is_cons, car, cdr, ConsPair, cons


# Unfortunately, `multipledispatch` doesn't use `isinstance` on the arguments,
# so it won't use our fancy setup for `isinstance(x, ConsPair)` and we have to
# specify--and check--each `cons`-amenable type explicitly.
def _cons_unify(lcons, rcons, s):

    if not is_cons(lcons) or not is_cons(rcons):
        # One of the arguments is necessarily a `ConsPair` object,
        # but the other could be an empty iterable, which isn't a
        # `cons`-derivable object.
        return False

    s = unify(car(lcons), car(rcons), s)
    if s is not False:
        return unify(cdr(lcons), cdr(rcons), s)
    return False


_unify.add(
    (ConsPair, (ConsPair, list, tuple, Iterator, OrderedDict), dict),
    _cons_unify,
)
_unify.add(((list, tuple, Iterator, OrderedDict), ConsPair, dict), _cons_unify)


@_reify.register(OrderedDict, dict)
def reify_OrderedDict(od, s):
    return OrderedDict((k, reify(v, s)) for k, v in od.items())


@_reify.register(ConsPair, dict)
def reify_cons(lcons, s):
    rcar = reify(car(lcons), s)
    rcdr = reify(cdr(lcons), s)
    return cons(rcar, rcdr)
