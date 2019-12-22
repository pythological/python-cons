from .core import cons, car, cdr  # noqa: F401

from . import unify  # noqa: F401

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
