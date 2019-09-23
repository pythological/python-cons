from itertools import tee
from collections import OrderedDict, Iterator

from unification.core import unify, _unify, reify, _reify

from .core import car, cdr, ConsPair, cons, MaybeCons, ConsError


def _cons_unify(lcons, rcons, s):

    lcons_ = lcons
    rcons_ = rcons

    if isinstance(lcons, Iterator):
        lcons, lcons_ = tee(lcons)

    if isinstance(rcons, Iterator):
        rcons, rcons_ = tee(rcons)

    try:
        s = unify(car(lcons), car(rcons), s)

        if s is not False:
            return unify(cdr(lcons_), cdr(rcons_), s)
    except ConsError:
        pass

    return False


_unify.add((ConsPair, (ConsPair, MaybeCons), dict), _cons_unify)
_unify.add((MaybeCons, ConsPair, dict), _cons_unify)


@_reify.register(OrderedDict, dict)
def reify_OrderedDict(od, s):
    return OrderedDict((k, reify(v, s)) for k, v in od.items())


@_reify.register(ConsPair, dict)
def reify_cons(lcons, s):
    rcar = reify(car(lcons), s)
    rcdr = reify(cdr(lcons), s)
    return cons(rcar, rcdr)
